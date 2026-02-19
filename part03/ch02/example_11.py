from langchain.text_splitter import TextSplitter
from typing import List


class SentenceSplitter(TextSplitter):
    """문장 단위 분할기"""

    def split_text(self, text: str) -> List[str]:
        # 문장 종결 부호로 분할
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            if current_length + len(sentence) > self._chunk_size:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_length = len(sentence)
            else:
                current_chunk.append(sentence)
                current_length += len(sentence)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks


# 사용
splitter = SentenceSplitter(chunk_size=300)
chunks = splitter.split_text(text)
