from typing import List
from langchain_core.documents import Document


class ContextManager:
    """컨텍스트 관리"""

    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.chars_per_token = 4  # 근사값

    def estimate_tokens(self, text: str) -> int:
        """토큰 수 추정"""
        return len(text) // self.chars_per_token

    def truncate_context(self, contexts: List[str]) -> List[str]:
        """컨텍스트 잘라내기"""
        total_tokens = 0
        result = []

        for ctx in contexts:
            tokens = self.estimate_tokens(ctx)

            if total_tokens + tokens > self.max_tokens:
                # 남은 공간만큼만 추가
                remaining = self.max_tokens - total_tokens
                remaining_chars = remaining * self.chars_per_token
                result.append(ctx[:remaining_chars] + "...")
                break

            result.append(ctx)
            total_tokens += tokens

        return result

    def prioritize_contexts(self, contexts: List[str],
                           scores: List[float]) -> List[str]:
        """점수 기반 우선순위 정렬"""
        paired = list(zip(contexts, scores))
        paired.sort(key=lambda x: x[1], reverse=True)

        sorted_contexts = [ctx for ctx, _ in paired]
        return self.truncate_context(sorted_contexts)

    def deduplicate_contexts(self, contexts: List[str],
                            similarity_threshold: float = 0.9) -> List[str]:
        """중복 컨텍스트 제거"""
        if not contexts:
            return []

        unique = [contexts[0]]

        for ctx in contexts[1:]:
            is_duplicate = False

            for unique_ctx in unique:
                # 간단한 유사도 (Jaccard)
                set1 = set(ctx.split())
                set2 = set(unique_ctx.split())
                similarity = len(set1 & set2) / len(set1 | set2) if set1 | set2 else 0

                if similarity > similarity_threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique.append(ctx)

        return unique


# 사용
manager = ContextManager(max_tokens=1000)

contexts = [
    "LangChain은 LLM 프레임워크입니다." * 50,
    "RAG는 검색 증강 생성입니다." * 30,
    "벡터 DB는 임베딩을 저장합니다." * 20
]

truncated = manager.truncate_context(contexts)
print(f"원본: {len(contexts)}개")
print(f"잘라낸 후: {len(truncated)}개")
print(f"총 길이: {sum(len(c) for c in truncated)}자")
