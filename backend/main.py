from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import openai
from dotenv import load_dotenv
from scipy.spatial.distance import cosine
import os
from openai import OpenAI
from pydantic import BaseModel
import tiktoken

import redis

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")
redis_host = os.getenv("REDIS_HOST")
redis_pw = os.getenv("REDIS_PASSWORD")



r = redis.Redis(host=redis_host, port=6379, password=redis_pw, db=0)
client = OpenAI(api_key=api_key)

class ChatInput(BaseModel):
    user_input: Optional[str] = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 붐빔정도에 대한 임베딩 생성 함수


def find_highest_population_areas_by_age_group(df, age_groups):
    highest_areas = {}
    for age_group in age_groups:
        highest_row = df.loc[df[age_group].idxmax()]
        highest_areas[age_group] = highest_row['AREA_NM']
    return highest_areas

# 연령대별 컬럼을 수치형으로 변환하는 함수
def convert_columns_to_numeric(df, age_groups):
    for age_group in age_groups:
        df[age_group] = pd.to_numeric(df[age_group], errors='coerce')
    df.fillna(0, inplace=True)

# 연령대별 인구 비율 컨텍스트 생성 함수
def create_population_context(df_population):
    age_groups = ['PPLTN_RATE_10', 'PPLTN_RATE_20', 'PPLTN_RATE_30', 'PPLTN_RATE_40', 'PPLTN_RATE_50']
    convert_columns_to_numeric(df_population, age_groups)
    highest_areas = find_highest_population_areas_by_age_group(df_population, age_groups)
    population_context = "연령대별 인구 비율이 가장 높은 지역:\n"
    for age_group, area in highest_areas.items():
        population_context += f"{age_group}: {area}\n"
    return population_context

# 붐빔정도 컨텍스트 생성 함수
def create_context(question, df, max_len=3000):
    q_embedding = (
        client.embeddings.create(input=question, model="text-embedding-ada-002")
        .data[0]
        .embedding
    )
    tokenizer = tiktoken.get_encoding("cl100k_base")
    df["n_tokens"] = df["combined"].apply(lambda x: len(tokenizer.encode(x)))
    
    df["distances"] = df["embedding"].apply(lambda x: cosine(q_embedding, x))
    cur_len = 0
    context_parts = []
    for _, row in df.sort_values("distances", ascending=True).iterrows():
        cur_len += row["n_tokens"] + 4
        if cur_len > max_len:
            break
        context_parts.append(row["combined"])
    return "\n\n===\n\n".join(context_parts)

# 질문에 대답하는 함수
def answer_question(question, df_congest, df_population, openai_api_key, model="gpt-3.5-turbo", max_len=3000, debug=False):
    population_context = create_population_context(df_population)
    congest_context = create_context(question, df_congest, max_len)

    combined_context = population_context + "\n\n===\n\n" + congest_context
    if debug:
        print("Context:\n" + combined_context)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Answer the question based on the context below."},
                {"role": "user", "content": f"context: {combined_context}\n\n---\n\nQuestion: {question}, 한국어로 대답해줘. 자신감 있게 말해줘"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Error occurred:", e)
        return ""

@app.post("/chat")
async def chat(input_data: ChatInput):
    user_input = input_data.user_input
    origin_data = r.get("df_all_origins_2024-01-27")
    ppltns_data = r.get("df_all_ppltns_2024-01-27")
    
    df_congest = pd.read_json(ppltns_data.decode("utf-8"),orient="split")
    df_population = pd.read_json(origin_data.decode("utf-8"),orient="split")
   
    if user_input is None:
        return {"message": "입력된 메시지가 없습니다."}

    response =  answer_question(user_input, df_congest, df_population, api_key, debug=False)
    return {"User": user_input, "도봉이": response}

# Run the server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
