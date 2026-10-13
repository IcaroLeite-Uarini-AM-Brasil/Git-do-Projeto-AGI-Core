import math
import numpy as np

class MCTSNode:
    def __init__(self, state_vector: np.ndarray, parent=None, action_taken=None, prior: float = 0.0):
        self.state_vector = state_vector
        self.parent = parent
        self.action_taken = action_taken
        self.prior = prior
        self.children = {}
        self.visit_count = 0
        self.value_sum = 0.0

    @property
    def value(self) -> float:
        return self.value_sum / self.visit_count if self.visit_count > 0 else 0.0

class MCTSSearchEngine:
    """Motor de Planejamento Tipo-2 (Monte Carlo Tree Search)."""
    def __init__(self, c_puct: float = 1.4, num_simulations: int = 20):
        self.c_puct = c_puct
        self.num_simulations = num_simulations

    def search(self, root_state: np.ndarray, action_dim: int) -> int:
        root = MCTSNode(state_vector=root_state)
        for _ in range(self.num_simulations):
            node = root
            # Seleção
            while node.children:
                best_score, best_child = -float('inf'), None
                for a_idx, child in node.children.items():
                    score = child.value + self.c_puct * child.prior * (math.sqrt(node.visit_count) / (1 + child.visit_count))
                    if score > best_score:
                        best_score, best_child = score, child
                node = best_child

            # Expansão
            for a_idx in range(action_dim):
                if a_idx not in node.children:
                    node.children[a_idx] = MCTSNode(
                        state_vector=node.state_vector + np.random.randn(*node.state_vector.shape) * 0.05,
                        parent=node, action_taken=a_idx, prior=1.0 / action_dim
                    )
            # Simulação (aleatória simplificada)
            leaf_val = float(np.random.randn() * 0.1)
            # Retropropagação
            curr = node
            while curr is not None:
                curr.visit_count += 1
                curr.value_sum += leaf_val
                curr = curr.parent

        visits = [root.children[a].visit_count if a in root.children else 0 for a in range(action_dim)]
        return int(np.argmax(visits))
