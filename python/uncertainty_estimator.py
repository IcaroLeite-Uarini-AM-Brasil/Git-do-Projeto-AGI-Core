"""M75: estatísticas de incerteza para amostras de distribuições categóricas.

As entradas devem ser vetores de probabilidades finitas, não negativas e com
soma 1. A variância entre amostras é apenas um indicador; não é uma medida
calibrada de incerteza epistêmica sem um método de amostragem apropriado.
"""
from dataclasses import dataclass
import math
from typing import Sequence


@dataclass(frozen=True)
class UncertaintyResult:
    predictive_variance: float
    shannon_entropy: float
    is_high_uncertainty: bool


class EpistemicUncertaintyEstimator:
    def __init__(self, variance_threshold: float = 0.05, entropy_threshold: float = 1.5):
        if variance_threshold < 0 or entropy_threshold < 0:
            raise ValueError("thresholds must be non-negative")
        self.variance_threshold = variance_threshold
        self.entropy_threshold = entropy_threshold

    def estimate_uncertainty(self, model_outputs: Sequence[Sequence[float]]) -> UncertaintyResult:
        if not model_outputs:
            raise ValueError("model_outputs must contain at least one sample")
        width = len(model_outputs[0])
        if width == 0 or any(len(row) != width for row in model_outputs):
            raise ValueError("all samples must have the same non-zero number of classes")

        samples = []
        for row in model_outputs:
            values = [float(value) for value in row]
            if any(not math.isfinite(value) or value < 0 for value in values):
                raise ValueError("probabilities must be finite and non-negative")
            total = sum(values)
            if not math.isclose(total, 1.0, rel_tol=1e-6, abs_tol=1e-6):
                raise ValueError("each sample must sum to 1")
            samples.append(values)

        means = [sum(row[i] for row in samples) / len(samples) for i in range(width)]
        variance = sum(
            sum((row[i] - means[i]) ** 2 for row in samples) / len(samples)
            for i in range(width)
        ) / width
        entropy = -sum(p * math.log2(p) for p in means if p > 0)
        variance = round(variance, 6)
        entropy = round(entropy, 6)
        return UncertaintyResult(
            predictive_variance=variance,
            shannon_entropy=entropy,
            is_high_uncertainty=(variance > self.variance_threshold or entropy > self.entropy_threshold),
        )


if __name__ == "__main__":
    samples = [
        [0.85, 0.10, 0.05], [0.80, 0.15, 0.05], [0.88, 0.08, 0.04],
        [0.82, 0.12, 0.06], [0.86, 0.09, 0.05],
    ]
    print(EpistemicUncertaintyEstimator().estimate_uncertainty(samples))
