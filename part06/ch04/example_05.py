from langchain_ollama import OllamaLLM
from typing import Dict, List


class PromptOptimizer:
    """프롬프트 최적화"""

    def __init__(self, model: str = "llama4"):
        self.llm = OllamaLLM(model=model)

        self.prompt_templates = {
            "basic": """컨텍스트: {context}

질문: {question}

답변:""",

            "strict": """다음 컨텍스트만 사용하여 질문에 답하세요.
컨텍스트에 없는 정보는 "알 수 없습니다"라고 답하세요.

컨텍스트:
{context}

질문: {question}

답변:""",

            "structured": """### 지시사항
주어진 컨텍스트를 바탕으로 질문에 답하세요.
- 컨텍스트에 있는 정보만 사용하세요
- 확실하지 않으면 그렇다고 말하세요
- 간결하게 답하세요

### 컨텍스트
{context}

### 질문
{question}

### 답변""",

            "cot": """컨텍스트: {context}

질문: {question}

단계별로 생각해봅시다:
1. 질문의 핵심은 무엇인가요?
2. 컨텍스트에서 관련 정보는?
3. 따라서 답은?

최종 답변:"""
        }

    def test_prompt(self, template_name: str, context: str, question: str) -> str:
        """프롬프트 테스트"""
        template = self.prompt_templates.get(template_name, self.prompt_templates["basic"])
        prompt = template.format(context=context, question=question)

        return self.llm.invoke(prompt)

    def compare_prompts(self, context: str, question: str) -> Dict[str, str]:
        """프롬프트 비교"""
        results = {}

        for name in self.prompt_templates:
            answer = self.test_prompt(name, context, question)
            results[name] = answer
            print(f"\n=== {name} ===")
            print(answer[:200])

        return results


# 사용
optimizer = PromptOptimizer()

context = "LangChain은 Harrison Chase가 2022년에 만든 LLM 프레임워크입니다."
question = "LangChain을 누가 만들었나요?"

# results = optimizer.compare_prompts(context, question)
