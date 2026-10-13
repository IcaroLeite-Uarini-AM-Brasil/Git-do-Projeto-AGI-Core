import collections
import numpy as np
from typing import Deque, Tuple, List

class CognitiveMemory:
    """Implementação simples de memória episódica com STM e LTM (placeholder)."""
    def __init__(self, stm_capacity: int = 100, ltm_capacity: int = 10000):
        self.stm: Deque[Tuple[np.ndarray, np.ndarray, float]] = collections.deque(maxlen=stm_capacity)
        self.ltm: Deque[Tuple[np.ndarray, np.ndarray, float]] = collections.deque(maxlen=ltm_capacity)

    def store_episode(self, state: np.ndarray, action: np.ndarray, reward: float):
        self.stm.append((state.copy(), action.copy(), float(reward)))
        self.ltm.append((state.copy(), action.copy(), float(reward)))

    def sample_recent(self, k: int = 32) -> List[Tuple[np.ndarray, np.ndarray, float]]:
        k = min(k, len(self.stm))
        return list(self.stm)[-k:]

    def sample_longterm(self, k: int = 64) -> List[Tuple[np.ndarray, np.ndarray, float]]:
        k = min(k, len(self.ltm))
        idxs = np.random.choice(len(self.ltm), size=k, replace=False)
        return [self.ltm[i] for i in idxs]
