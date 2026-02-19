import random
from typing import List, Dict, Tuple


class TestSetSplitter:
    """테스트셋 분할기"""

    def __init__(self, seed: int = 42):
        self.seed = seed

    def split(self, test_cases: List[Dict],
             train_ratio: float = 0.7,
             val_ratio: float = 0.15,
             test_ratio: float = 0.15) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """데이터 분할"""
        assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 0.01, "비율 합이 1이어야 합니다"

        random.seed(self.seed)
        shuffled = test_cases.copy()
        random.shuffle(shuffled)

        n = len(shuffled)
        train_end = int(n * train_ratio)
        val_end = train_end + int(n * val_ratio)

        train_set = shuffled[:train_end]
        val_set = shuffled[train_end:val_end]
        test_set = shuffled[val_end:]

        return train_set, val_set, test_set

    def stratified_split(self, test_cases: List[Dict],
                        stratify_key: str = "difficulty",
                        train_ratio: float = 0.7,
                        val_ratio: float = 0.15,
                        test_ratio: float = 0.15) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """층화 분할 (카테고리별 비율 유지)"""
        from collections import defaultdict

        # 카테고리별 그룹화
        groups = defaultdict(list)
        for case in test_cases:
            key = case.get(stratify_key, "unknown")
            groups[key].append(case)

        train_set, val_set, test_set = [], [], []

        # 각 그룹에서 비율대로 분할
        for group_cases in groups.values():
            t, v, ts = self.split(group_cases, train_ratio, val_ratio, test_ratio)
            train_set.extend(t)
            val_set.extend(v)
            test_set.extend(ts)

        return train_set, val_set, test_set


# 사용
splitter = TestSetSplitter(seed=42)

# 테스트 케이스 (난이도 포함)
test_cases = [
    {"question": "Q1", "difficulty": "easy"},
    {"question": "Q2", "difficulty": "easy"},
    {"question": "Q3", "difficulty": "medium"},
    {"question": "Q4", "difficulty": "medium"},
    {"question": "Q5", "difficulty": "medium"},
    {"question": "Q6", "difficulty": "hard"},
    {"question": "Q7", "difficulty": "hard"},
    {"question": "Q8", "difficulty": "easy"},
    {"question": "Q9", "difficulty": "medium"},
    {"question": "Q10", "difficulty": "hard"},
]

# 층화 분할
train, val, test = splitter.stratified_split(
    test_cases,
    stratify_key="difficulty",
    train_ratio=0.6,
    val_ratio=0.2,
    test_ratio=0.2
)

print(f"Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")
