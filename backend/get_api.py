import requests
import xmltodict
import pandas as pd
import os
import warnings
from dotenv import load_dotenv

from openai import OpenAI
import datetime


import redis
import json


# openpyxl에서 발생하는 특정 경고를 무시합니다.
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

# .env 파일에서 API 키를 로드합니다.
load_dotenv()
openkey = os.getenv("OPEN_API_KEY")
key = os.getenv("API_KEY")
redis_host = os.getenv("REDIS_HOST")
redis_pw = os.getenv("REDIS_PASSWORD")

client = OpenAI(api_key=openkey)

# 엑셀 파일을 데이터프레임으로 로드합니다.
place_data = pd.read_excel('/usr/src/app/서울시 주요 113장소명 목록(코드포함).xlsx')

# Search_data 함수를 정의합니다.
def Search_data(nm, mm, dd, keys):
    url = f'http://openapi.seoul.go.kr:8088/{keys}/xml/citydata_ppltn/{mm}/{dd}/{nm}'
    r = requests.get(url)
    file = xmltodict.parse(r.text)["Map"]['SeoulRtd.citydata_ppltn']
    origin = {k: v for k, v in file.items() if k != 'FCST_PPLTN'}
    df_origin = pd.DataFrame([origin])
    df_ppltn = pd.DataFrame()

    if "FCST_PPLTN" in file:
        df_ppltn = pd.DataFrame(file["FCST_PPLTN"]["FCST_PPLTN"])
        area_nm = origin.get("AREA_NM")
        area_cd = origin.get("AREA_CD")
        if area_nm and area_cd:
            df_ppltn["AREA_NM"] = area_nm
            df_ppltn["AREA_CD"] = area_cd

    return df_origin, df_ppltn


def Combine_data(row):
    area = row["AREA_NM"].strip()
    datetime = row["FCST_TIME"].strip()
    congest = row["FCST_CONGEST_LVL"].strip()
    
    combined = [f"시간: {datetime}",f"위치: {area}",f"붐빔정도: {congest}"]
    combined = "\n".join(combined)
    
    return f"```{combined}```"

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding




# 각 장소명에 대해 데이터를 검색하고 결과를 리스트에 추가합니다.
df_origin_list = []
df_ppltn_list = []
for nm in place_data["AREA_NM"]:
    df_origin, df_ppltn = Search_data(nm, 1, 25, key)
    df_origin_list.append(df_origin)
    df_ppltn_list.append(df_ppltn)

# 결과를 하나의 데이터프레임으로 결합합니다.
df_all_origins = pd.concat(df_origin_list, ignore_index=True)
df_all_ppltns = pd.concat(df_ppltn_list, ignore_index=True)

df_all_ppltns['combined'] = df_all_ppltns.apply(Combine_data, axis=1)
df_all_ppltns["embedding"] = df_all_ppltns["combined"].apply(get_embedding)
# 각 항목의 첫 번째 요소만 선택하여 1-D 벡터로 변환

# 임베딩 이후 redis로 저장 

# 1. json으로 변환 

json_all_origins = df_all_origins.to_json(orient='split')
json_all_ppltns = df_all_ppltns.to_json(orient='split')

# 오늘 시간 적어서 redis에 저장
todays = datetime.datetime.now().strftime("%Y-%m-%d")
r = redis.Redis(host=redis_host, port=6379, password=redis_pw, db=0)

key_all_origins = f"df_all_origins_{todays}"
key_all_ppltns = f"df_all_ppltns_{todays}"

r.set(key_all_origins, json_all_origins)
r.set(key_all_ppltns, json_all_ppltns)

