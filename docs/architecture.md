# Arquitetura Técnica — AGI Core Framework

Este documento descreve a arquitetura técnica detalhada, interfaces entre componentes, fluxos de dados, decisões de projeto e planos de experimentos.

1. Visão Geral Arquitetural
---------------------------
O sistema é linearmente organizado em camadas comunicantes: Sensoriamento → Representação → Memória → Planejamento → Política → Execução. Cada camada expõe interfaces bem definidas para entrada/saída (data contracts), permitindo substituição e testes unitários.

2. Componentes & Interfaces
---------------------------
2.1 Percepção
- Componentes: `DeepPerceptionEncoder`, preprocessors multimodais.
- Entrada: estados brutos (vetores, imagens, áudio).
- Saída: embeddings latentes (np.ndarray / torch.Tensor).
- Interface exemplificada:
  - encode(state: np.ndarray) -> np.ndarray / torch.Tensor

2.2 Representação Simbólica & Grafo
- Components: `DynamicKnowledgeGraph`, `Ontology`.
- Operações: MERGE nodes, CREATE transitions, query causal paths.
- Interface exemplificada:
  - record_causal_relation(s1: str, action: str, s2: str, reward: float) -> None
  - query_related(state: str, depth: int) -> List[Tuple[state,action,state]]

2.3 Memória
- `CognitiveMemory` com STM/LTM:
  - store_episode(state, action, reward)
  - sample_recent(k)
  - semantic_retrieval(query_embedding, k)

2.4 Planejamento
- `MCTSSearchEngine`:
  - search(root_state_vector, action_dim) -> action_index
- Requisitos: possibilidade de simulação determinística/estocástica, priors e heurísticas.

2.5 Política / RL
- `ActorCritic`:
  - select_action(obs_tensor) -> action_tensor
  - value(obs_tensor) -> value_estimate

2.6 Distribuição
- `DistributedEnvironmentWorker` (Ray actor):
  - collect_step(action: np.ndarray) -> (curr_obs, reward, next_obs, done, worker_id)

2.7 Agents
- `CognitiveAgent` (coordenador):
  - pipeline: observe → perceive → retrieve_memory → plan → select_action → apply_guardrails → execute → store_experience

3. Fluxo de Dados (exemplo de ciclo)
-----------------------------------
1. Sensor captura `obs_raw`.
2. `Perception.encode(obs_raw)` → `embedding`.
3. `Memory.semantic_retrieval(embedding)` → contexto.
4. `Planning` (MCTS) simula usando `embedding + contexto` → ação candidata.
5. `ActorCritic` gera distribuição/policy.
6. `SymbolicSafetyEngine` aplica guardrails → `safe_action`.
7. `DistributedEnvironmentWorker` executa a ação → retorno (obs', reward).
8. `KnowledgeGraph.record_causal_relation(...)` e `Memory.store_episode(...)`.

4. Contratos de serialização e persistência
------------------------------------------
- Use JSON/MsgPack para mensagens entre processos.
- Para grafos e histórico de experiências, suportar fallback local (pickle/SQLite) caso Neo4j esteja indisponível.
- Schema de eventos (simplificado): {timestamp, worker_id, state_embedding_ref, action, reward, done, meta}

5. Observabilidade & Telemetria
------------------------------
- Logs estruturados (JSON), com níveis e IDs de correlação.
- Métricas: reward médio, taxa de interceptações de segurança, tempo médio por decisão, throughput de workers.
- Dashboard Streamlit: exibir métricas, grafo de conhecimento (sumário), estado de nós MCTS, intervenções de segurança.

6. Segurança, Alinhamento & Testes
---------------------------------
- Testes unitários para cada módulo:
  - perception: shapes de saída, estabilidade numérica
  - safety_engine: respostas determinísticas a inputs extremos
  - mcts: propriedades de visita/seleção
  - memory: invariantes de capacidade e amostragem
- Testes de integração com ambientes simulados (gymnasium/Pendulum-v1).
- Checklist de segurança: credenciais, limites, rollback, revisão humana.

7. Escalabilidade & Deploy
--------------------------
- Deploy local (single-node) para experimentos rápidos.
- Deploy em cluster (Ray) com auto-scaling para treinos distribuídos.
- Armazenamento: Neo4j para grafo, object store (S3) para checkpoints de modelo.
- Recomenda-se containerização (Docker) e orquestração (Kubernetes) para produção.

8. Plano de Experimentos e Métricas
----------------------------------
- Experimentos iniciais:
  - Comparar MCTS puro vs MCTS + policy guide (ActorCritic) em ambientes contínuos.
  - Avaliar impacto de safety_engine em performance vs segurança.
  - Medir sample efficiency ao usar memory-replay sem vs com retrieval semântico.
- Métricas primárias:
  - Cumulative reward (média por episódio)
  - Sample efficiency (recompensa vs amostras)
  - Frequency of safety interceptions
  - Generalization tests (transfer across env variants)

9. Pistas de Implementação e Evolução
------------------------------------
- Introduzir embeddings multimodais (CLIP-like) para integrar visão e texto.
- Adicionar módulos de causal discovery para enriquecer o grafo.
- Substituir MCTS simples por variantes com redes neurais de valor/prior (AlphaZero style).
- Adotar práticas MLOps: tracking (Weights & Biases), CI, testes de regressão.

10. Conclusão
-------------
Este documento serve como referência técnica para evoluir o repositório em pesquisa e em engenharia. As interfaces são deliberadamente simples para facilitar experimentação e substituição incremental de componentes.
