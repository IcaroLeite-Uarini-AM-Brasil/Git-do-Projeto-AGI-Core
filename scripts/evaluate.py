import numpy as np

from agi_core.agents.cognitive_agent import CognitiveAgent
from agi_core.eval.benchmark import Benchmark


def demo_evaluator():
    agent = CognitiveAgent(obs_dim=3, action_dim=3)
    obs = np.random.randn(3)
    result = agent.act(obs, reward=1.2)
    return 1.0 if result["safe_action"] is not None else 0.0, {"reward": 1.2}, "benchmark_exec_ok"


def main():
    benchmark = Benchmark("demo_agent")
    result = benchmark.run(demo_evaluator)
    print(result)


if __name__ == "__main__":
    main()
