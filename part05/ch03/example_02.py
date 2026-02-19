def table_to_natural_language(table_text: str, table_title: str = None) -> str:
    """표를 자연어로 변환"""
    rows = parse_markdown_table(table_text)

    if not rows:
        return ""

    headers = list(rows[0].keys())

    # 시작 문장
    if table_title:
        result = f"{table_title}에 대한 정보입니다.\n\n"
    else:
        result = f"{headers[0]}에 대한 정보입니다.\n\n"

    # 각 행 설명
    for row in rows:
        primary_value = list(row.values())[0]
        descriptions = [f"{k}은(는) {v}" for k, v in list(row.items())[1:]]

        result += f"{primary_value}의 경우, {', '.join(descriptions)}입니다.\n"

    return result


# 사용
natural = table_to_natural_language(table_md, "임베딩 모델 비교")
print(natural)
