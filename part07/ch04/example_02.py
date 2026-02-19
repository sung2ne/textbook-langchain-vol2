from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List


class StreamingHandler(BaseCallbackHandler):
    """커스텀 스트리밍 핸들러"""

    def __init__(self, on_token=None, on_end=None):
        self.on_token = on_token
        self.on_end = on_end
        self.tokens = []

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """새 토큰 수신"""
        self.tokens.append(token)

        if self.on_token:
            self.on_token(token)

    def on_llm_end(self, response, **kwargs) -> None:
        """생성 완료"""
        if self.on_end:
            self.on_end("".join(self.tokens))


# 사용
def print_token(token):
    print(token, end="", flush=True)


def on_complete(full_text):
    print(f"\n\n[완료: {len(full_text)}자]")


handler = StreamingHandler(on_token=print_token, on_end=on_complete)

llm = OllamaLLM(model="llama4", callbacks=[handler])
llm.invoke("RAG를 설명해주세요.")
