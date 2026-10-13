import numpy as np
from typing import Tuple

class SymbolicSafetyEngine:
    """Aplica o Symbol Grounding e executa guardrails determinísticos de segurança."""
    def __init__(self, action_dim: int, action_bounds: Tuple[float, float]):
        self.action_dim = action_dim
        self.min_action, self.max_action = action_bounds

    def symbolize(self, raw_obs: np.ndarray) -> str:
        val = float(raw_obs[0]) if len(raw_obs) > 0 else 0.0
        if abs(val) < 0.8:
            return "ESTADO_ESTÁVEL"
        elif val >= 0.8:
            return "LIMITE_CRÍTICO_POSITIVO"
        else:
            return "LIMITE_CRÍTICO_NEGATIVO"

    def apply_safety_guardrails(self, symbol: str, raw_action: np.ndarray) -> Tuple[np.ndarray, bool]:
        clamped_action = np.clip(raw_action, self.min_action, self.max_action)
        intercepted = False

        if symbol == "LIMITE_CRÍTICO_POSITIVO" and clamped_action[0] > 0:
            clamped_action[0] *= -0.5
            intercepted = True
        elif symbol == "LIMITE_CRÍTICO_NEGATIVO" and clamped_action[0] < 0:
            clamped_action[0] *= -0.5
            intercepted = True

        return clamped_action, intercepted
