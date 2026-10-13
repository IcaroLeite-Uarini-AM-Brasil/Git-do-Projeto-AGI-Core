from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class BenchmarkResult:
    name: str
    score: float
    metrics: Dict[str, float] = field(default_factory=dict)
    notes: str = ""


class Benchmark:
    """Harness simples para avaliação de agentes e políticas."""

    def __init__(self, name: str):
        self.name = name
        self.results: List[BenchmarkResult] = []

    def run(self, evaluator_fn, *args, **kwargs):
        score, metrics, notes = evaluator_fn(*args, **kwargs)
        result = BenchmarkResult(name=self.name, score=float(score), metrics=dict(metrics), notes=str(notes))
        self.results.append(result)
        return result

    def summary(self):
        if not self.results:
            return {"name": self.name, "count": 0, "average_score": 0.0}
        avg = sum(r.score for r in self.results) / len(self.results)
        return {
            "name": self.name,
            "count": len(self.results),
            "average_score": avg,
            "results": [r.__dict__ for r in self.results],
        }
