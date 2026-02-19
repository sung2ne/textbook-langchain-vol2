def euclidean_distance(vec1, vec2):
    """유클리드 거리"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    return np.linalg.norm(vec1 - vec2)


# 거리가 작을수록 유사
dist = euclidean_distance(vectors[0], vectors[1])
print(f"거리: {dist:.4f}")
