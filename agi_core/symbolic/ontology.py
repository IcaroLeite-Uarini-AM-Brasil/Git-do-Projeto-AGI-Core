from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional


@dataclass
class Concept:
    name: str
    properties: Dict[str, object] = field(default_factory=dict)


class Ontology:
    """Representação simbólica e semântica de entidades e relações."""

    def __init__(self):
        self.concepts: Dict[str, Concept] = {}
        self.relations: List[Tuple[str, str, str, Dict[str, object]]] = []

    def add_concept(self, name: str, **properties):
        self.concepts[name] = Concept(name=name, properties=properties)
        return self.concepts[name]

    def add_relation(self, source: str, relation: str, target: str, **props):
        self.relations.append((source, relation, target, props))

    def query_related(self, concept_name: str, relation_name: Optional[str] = None, depth: int = 1):
        matches: List[Tuple[str, str, str, Dict[str, object]]] = []
        for source, relation, target, props in self.relations:
            if source == concept_name or target == concept_name:
                if relation_name is None or relation == relation_name:
                    matches.append((source, relation, target, props))
        if depth <= 1:
            return matches

        # Expansão simples para profundidade > 1
        next_nodes = {concept_name}
        seen = {concept_name}
        frontier = {concept_name}
        for _ in range(depth):
            new_frontier = set()
            for node in frontier:
                for source, relation, target, props in self.relations:
                    if source == node and target not in seen:
                        new_frontier.add(target)
                        seen.add(target)
                    if target == node and source not in seen:
                        new_frontier.add(source)
                        seen.add(source)
            frontier = new_frontier
        related = []
        for source, relation, target, props in self.relations:
            if source in seen or target in seen:
                related.append((source, relation, target, props))
        return related

    def to_dict(self):
        return {
            "concepts": {k: v.properties for k, v in self.concepts.items()},
            "relations": [
                {"source": s, "relation": r, "target": t, "properties": p}
                for s, r, t, p in self.relations
            ],
        }
