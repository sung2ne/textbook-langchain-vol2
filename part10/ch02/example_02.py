from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """도시의 현재 날씨를 조회합니다."""
    # 실제로는 API 호출
    return f"{city}: 맑음, 15도"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """이메일을 전송합니다."""
    # 실제로는 SMTP 전송
    return f"이메일 전송 완료: {to}"

@tool
def run_sql(query: str) -> str:
    """SQL 쿼리를 실행합니다."""
    # 실제로는 DB 연결
    return "쿼리 결과: ..."
