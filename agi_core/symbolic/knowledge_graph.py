from typing import List, Tuple
from neo4j import GraphDatabase

class DynamicKnowledgeGraph:
    """Interface de persistência e consulta semântica em banco de dados Neo4j."""
    def __init__(self, uri: str = "bolt://localhost:7687", auth: Tuple[str, str] = ("neo4j", "password")):
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(uri, auth=auth)
        except Exception:
            # fallback para armazenamento local caso o Neo4j não esteja disponível
            self.driver = None
        self.local_store = []

    def close(self):
        if self.driver:
            self.driver.close()

    def record_causal_relation(self, state_symbol: str, action: str, next_symbol: str, reward: float):
        if self.driver:
            query = (
                "MERGE (s1:State {name: $s1})\n"
                "MERGE (s2:State {name: $s2})\n"
                "CREATE (s1)-[r:TRANSITION {action: $act, reward: $rew, timestamp: timestamp()}]->(s2)"
            )
            with self.driver.session() as session:
                session.run(query, s1=state_symbol, s2=next_symbol, act=action, rew=reward)
        else:
            self.local_store.append((state_symbol, action, next_symbol, reward))
