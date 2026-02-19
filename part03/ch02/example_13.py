def analyze_chunks(chunks: List[str]):
    """청크 분석"""
    lengths = [len(chunk) for chunk in chunks]

    print(f"총 청크 수: {len(chunks)}")
    print(f"평균 길이: {sum(lengths) / len(lengths):.0f}")
    print(f"최소 길이: {min(lengths)}")
    print(f"최대 길이: {max(lengths)}")

    # 너무 짧은 청크 확인
    short_chunks = [c for c in chunks if len(c) < 50]
    if short_chunks:
        print(f"\n⚠️ 짧은 청크 ({len(short_chunks)}개):")
        for c in short_chunks[:3]:
            print(f"  '{c[:30]}...'")

    # 너무 긴 청크 확인
    long_chunks = [c for c in chunks if len(c) > 1000]
    if long_chunks:
        print(f"\n⚠️ 긴 청크 ({len(long_chunks)}개)")


# 사용
analyze_chunks(chunks)
