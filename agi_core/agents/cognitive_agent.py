from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from agi_core.memory.cognitive_memory import CognitiveMemory
from agi_core.mcts.tree_search import MCTSSearchEngine
from agi_core.symbolic.safety_engine import SymbolicSafetyEngine


class CognitiveAgent:
    """Agente cognitivo composto por memória, planejamento, segurança e execução."""

    def __init__(
        self,
        obs_dim: int,
        action_dim: int,
        action_bounds: Tuple[float, float] = (-2.0, 2.0),
        memory_capacity: int = 1000,
        planner_simulations: int = 20,
    ):
        self.obs_dim = obs_dim
        self.action_dim = action_dim
        self.memory = CognitiveMemory(stm_capacity=128, ltm_capacity=memory_capacity)
        self.planner = MCTSSearchEngine(num_simulations=planner_simulations)
        self.safety = SymbolicSafetyEngine(action_dim=action_dim, action_bounds=action_bounds)
        self.history: List[Dict[str, Any]] = []

    def perceive(self, raw_obs: np.ndarray) -> str:
        return self.safety.symbolize(raw_obs)

    def decide(self, raw_obs: np.ndarray) -> Tuple[int, np.ndarray, bool]:
        symbol = self.perceive(raw_obs)
        action_index = self.planner.search(raw_obs, self.action_dim)
        action_value = np.array([(action_index - 1) * 1.0], dtype=np.float32)
        safe_action, intercepted = self.safety.apply_safety_guardrails(symbol, action_value)
        return action_index, safe_action, intercepted

    def act(self, raw_obs: np.ndarray, reward: float = 0.0, action_taken: Optional[np.ndarray] = None):
        symbol = self.perceive(raw_obs)
        action_index, safe_action, intercepted = self.decide(raw_obs)
        if action_taken is not None:
            safe_action = action_taken
        self.memory.store_episode(raw_obs.copy(), safe_action.copy(), float(reward))
        self.history.append({
            "symbol": symbol,
            "action_index": action_index,
            "safe_action": safe_action.tolist(),
            "reward": float(reward),
            "intercepted": bool(intercepted),
        })
        return {"symbol": symbol, "action_index": action_index, "safe_action": safe_action, "intercepted": intercepted}
