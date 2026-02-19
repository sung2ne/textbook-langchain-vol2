class ChartProcessor:
    """차트 처리기"""

    def __init__(self):
        self.chart_types = {
            "bar": "막대 차트",
            "line": "선 그래프",
            "pie": "원형 차트",
            "flow": "플로우차트",
            "sequence": "시퀀스 다이어그램"
        }

    def detect_chart_type(self, image_path: str) -> str:
        """차트 유형 감지 (단순화된 예시)"""
        # 실제로는 이미지 분류 모델 사용
        return "flow"

    def describe_chart(self, image_path: str, chart_type: str = None) -> Document:
        """차트 설명 생성"""
        if chart_type is None:
            chart_type = self.detect_chart_type(image_path)

        # 유형별 템플릿
        templates = {
            "bar": "이 막대 차트는 {items}의 {metric}을(를) 비교합니다.",
            "line": "이 선 그래프는 {time_period} 동안의 {metric} 추이를 보여줍니다.",
            "flow": "이 플로우차트는 {process}의 진행 과정을 나타냅니다.",
        }

        # 실제로는 이미지 분석 필요
        description = f"이것은 {self.chart_types.get(chart_type, '차트')}입니다."

        return Document(
            page_content=description,
            metadata={
                "source": image_path,
                "type": "chart",
                "chart_type": chart_type
            }
        )
