import numpy as np
from agi_core.perception.encoder import DeepPerceptionEncoder


def test_encoder_shape():
    encoder = DeepPerceptionEncoder(input_dim=4, latent_dim=3)
    x = np.random.randn(4)
    out = encoder(torch_tensor := __import__('torch').tensor(x, dtype=__import__('torch').float32))
    assert out.shape == (3,)


def test_memory_capacity():
    from agi_core.memory.cognitive_memory import CognitiveMemory
    mem = CognitiveMemory(stm_capacity=10, ltm_capacity=20)
    for i in range(5):
        mem.store_episode(np.array([i, i + 1, i + 2], dtype=float), np.array([1.0], dtype=float), float(i))
    assert len(mem.sample_recent()) <= 5
