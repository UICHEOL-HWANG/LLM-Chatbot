<template>
    <div class="container">
        <main class="main-content">
            <div class="cotent">
                <h1 class="dobong">도봉이와</h1>
                <h1 class="dobong">함께하는</h1>
                <h1 class="dobong">도시정보</h1>
            </div>
            <div class="index-list max-content-width">
                <section class="nes-container is-dark">
                    <div class="title">
                        <h1 class="dobong">도봉이에게 묻기</h1>
                    </div>
                    <section class="message-list">
            <!-- 사용자와 챗봇 메시지를 위한 섹션 -->
            <section v-for="(message, index) in messages" :key="index"
                     :class="['message', message.side === 'right' ? '-right' : '-left']">
              <i class="nes-bcrikko" v-if="message.side === 'left'"></i>
              <div :class="`nes-balloon from-${message.side} is-dark`">
                <p class="botfonts">{{ message.text }}</p>
              </div>
              <i class="nes-bcrikko" v-if="message.side === 'right'"></i>
            </section>
          </section>

                    <!-- 입력 폼 -->
                    <form @submit.prevent="submitMessage" class="message-form">
                        <div class="nes-field">
                            <label for="message_field"></label>
                            <input type="text" id="message_field" class="nes-input" v-model="userInput" />
                        </div>
                        <button type="submit" class="nes-btn">보내기</button>
                    </form>
                </section>
            </div>

        </main>

    </div>
</template>

<script>
export default {
  data() {
    return {
      messages: [], // 메시지를 저장할 배열
      userInput: "", // 사용자 입력
    };
  },
  methods: {
    async submitMessage() {
      // 사용자 메시지를 배열에 추가
      const userText = this.userInput.trim();
      if (userText) {
        this.addMessage(userText, 'right');
        this.userInput = ""; // 입력 필드 초기화

        try {
          const response = await fetch("http://localhost:8000/chat", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ user_input: userText }),
          });

          if (response.ok) {
            const responseData = await response.json();
            // 서버로부터 받은 챗봇의 응답을 배열에 추가
            this.addMessage(responseData["도봉이"], 'left');
          } else {
            // 오류 처리
            console.error('Response error:', response);
          }
        } catch (error) {
          // 네트워크 오류 처리
          console.error('Network error:', error);
        }
      }
    },
    addMessage(text, side) {
      this.messages.push({ text, side });
      this.scrollToEnd();
    },
    scrollToEnd() {
      // 새 메시지가 추가되면 스크롤을 맨 아래로 이동
      this.$nextTick(() => {
        const messageList = this.$el.querySelector('.message-list');
        messageList.scrollTop = messageList.scrollHeight;
      });
    },
  },
};
</script>

<style>

.botfonts{
  font-family: 'MyWebFont', sans-serif;
  font-size: 25px;
}
.container {
    max-width: 980px;
    margin: 0 auto;
    margin-top: 150px;
}

.dobong {
    font-family: 'MyWebFont', sans-serif;
    font-size: 100px;
}

.message-form {
    display: flex;
}

.nes-field .nes-input,
.nes-field .nes-textarea {
    display: block;
    width: 800px;
}

.cotent {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    max-width: 1000px;
    width: 100%;
    height: 556px;
    margin: 0 auto
}

.index-list {
    margin: 210px auto 210px;
}

.title {
    margin: 0 auto;
    text-align: center;
    margin-bottom: 50px;
}


.max-content-width {
    max-width: 1000px;
    width: 100%;
}





.message-list>.message.-left i {
    margin-right: 2rem;
    margin-left: 2rem;
    margin-bottom: 10px;
}

.message-list>.message.-right i {
    margin-left: 2rem;
    margin-right: 2rem;
    margin-bottom: 10px;
}

.message-list>.message {
    display: flex;
    margin-top: 2rem;
}

.message-list>.message.-left {
    align-self: flex-start;
}

.message-list>.message.-right {
    align-self: flex-end;
}

.message-list {
    display: flex;
    flex-direction: column;
    max-height: 500px;
    /* 채팅창의 최대 높이 설정 */
    overflow-y: auto;
    /* 내용이 넘칠 경우 스크롤바 표시 */
}

.message-list>.message.-left,
.message-list>.message.-right {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    /* 메시지 간 간격 조정 */
}

.message-list>.message.-right {
    justify-content: flex-end;
}

.message-list>.message.-left .nes-balloon,
.message-list>.message.-right .nes-balloon {
    max-width: 70%;
    /* 메시지 최대 너비 설정 */
}

.nes-balloon.from-left {
    /* 챗봇 메시지 배경색 변경 */
    color: white;
}

.nes-balloon.from-right {
    /* 사용자 메시지 배경색 변경 */
    color: white;
    /* 사용자 메시지 글자색 변경 */
}

.nes-btn {
    background-color: #7649fe;
    /* 보내기 버튼 배경색 변경 */
    color: white;
    /* 보내기 버튼 글자색 변경 */
    border-color: #7649fe;
    /* 보내기 버튼 테두리색 변경 */
}</style>