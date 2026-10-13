import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple

class GaussianPolicy(nn.Module):
    def __init__(self, obs_dim: int, action_dim: int, hidden: int = 128):
        super().__init__()
        self.fc1 = nn.Linear(obs_dim, hidden)
        self.fc2 = nn.Linear(hidden, hidden)
        self.mean = nn.Linear(hidden, action_dim)
        self.log_std = nn.Parameter(torch.zeros(action_dim))

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        mean = self.mean(x)
        std = torch.exp(self.log_std)
        return mean, std

class Critic(nn.Module):
    def __init__(self, obs_dim: int, hidden: int = 128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 1)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(-1)

class ActorCritic:
    """Placeholder actor-critic wrapper para prototipagem."""
    def __init__(self, obs_dim: int, action_dim: int, device: str = "cpu"):
        self.device = device
        self.policy = GaussianPolicy(obs_dim, action_dim).to(device)
        self.critic = Critic(obs_dim).to(device)

    def select_action(self, obs: torch.Tensor) -> torch.Tensor:
        mean, std = self.policy(obs)
        return mean + std * torch.randn_like(mean)

    def value(self, obs: torch.Tensor) -> torch.Tensor:
        return self.critic(obs)
