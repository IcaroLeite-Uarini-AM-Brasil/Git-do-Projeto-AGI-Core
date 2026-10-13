import torch
import torch.nn as nn

class DeepPerceptionEncoder(nn.Module):
    """Mapeia vetores de estado brutos de alta dimensão em espaço latente contínuo."""
    def __init__(self, input_dim: int, latent_dim: int, hidden_dim: int = 128):
        super(DeepPerceptionEncoder, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, latent_dim),
            nn.Tanh()
        )

    def forward(self, state: torch.Tensor) -> torch.Tensor:
        return self.network(state)
