import numpy as np

from agi_core.agents.cognitive_agent import CognitiveAgent


def main():
    agent = CognitiveAgent(obs_dim=3, action_dim=3)
    for step in range(5):
        obs = np.random.randn(3)
        decision = agent.act(obs, reward=float(step + 1))
        print(f"step={step} symbol={decision['symbol']} action={decision['safe_action']} intercepted={decision['intercepted']}")


if __name__ == "__main__":
    main()
