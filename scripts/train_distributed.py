import time
import numpy as np
import ray
from agi_core.symbolic.safety_engine import SymbolicSafetyEngine
from agi_core.symbolic.knowledge_graph import DynamicKnowledgeGraph
from agi_core.mcts.tree_search import MCTSSearchEngine
from agi_core.distributed.ray_workers import DistributedEnvironmentWorker

def main():
    print("=== INICIANDO EXECUTOR PRINCIPAL AGI CORE ===")
    ray.init(ignore_reinit_error=True, logging_level="error")
    
    kg = DynamicKnowledgeGraph()
    mcts = MCTSSearchEngine(num_simulations=20)
    safety = SymbolicSafetyEngine(action_dim=1, action_bounds=(-2.0, 2.0))
    
    workers = [DistributedEnvironmentWorker.remote(i) for i in range(2)]
    
    for step in range(5):
        raw_obs = np.random.randn(3)
        symbol = safety.symbolize(raw_obs)
        best_action_idx = mcts.search(raw_obs, action_dim=3)
        raw_action = np.array([(best_action_idx - 1) * 1.0], dtype=np.float32)
        
        safe_action, intercepted = safety.apply_safety_guardrails(symbol, raw_action)
        
        futures = [w.collect_step.remote(safe_action) for w in workers]
        results = ray.get(futures)
        
        for curr_obs, reward, next_obs, done, w_id in results:
            next_sym = safety.symbolize(next_obs)
            kg.record_causal_relation(symbol, f"ACT_{best_action_idx}", next_sym, float(reward))
            print(f"Passo {step+1} | Worker {w_id} | Símbolo: {symbol} | Ação Segura: {safe_action[0]:.2f} | Interceptado: {intercepted}")
            
    kg.close()
    ray.shutdown()
    print("=== EXECUÇÃO CONCLUÍDA ===")

if __name__ == "__main__":
    main()
