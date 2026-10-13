import ray
import gymnasium as gym
import numpy as np

@ray.remote
class DistributedEnvironmentWorker:
    """Actor do Ray responsável por simulações distribuídas em paralelo."""
    def __init__(self, worker_id: int, env_name: str = "Pendulum-v1"):
        self.worker_id = worker_id
        self.env = gym.make(env_name)
        reset_result = self.env.reset()
        # gymnasium.reset() may return (obs, info)
        self.obs = reset_result[0] if isinstance(reset_result, tuple) else reset_result

    def collect_step(self, action: np.ndarray):
        step_result = self.env.step(action)
        # gymnasium.step() returns (obs, reward, terminated, truncated, info)
        if len(step_result) == 5:
            next_obs, reward, terminated, truncated, _ = step_result
            done = terminated or truncated
        else:
            # fallback for older gym APIs
            next_obs, reward, done, _ = step_result
        curr_obs = self.obs
        self.obs = self.env.reset()[0] if done else next_obs
        return curr_obs, float(reward), next_obs, done, self.worker_id
