//! M65: valida um DAG e produz um plano de kernels com fusões seguras limitadas.
//!
//! Isto é planejamento, não JIT: nenhum código nativo é gerado ou executado.

use std::collections::{HashMap, HashSet, VecDeque};
use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum OpType {
    MatrixMultiply,
    VectorAdd,
    ReLU,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GraphNode {
    pub id: usize,
    pub op: OpType,
    pub inputs: Vec<usize>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum KernelPlan {
    FusedMatMulRelu { matmul: usize, relu: usize },
    Single { node: usize, op: OpType },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum GraphError {
    DuplicateNode(usize),
    MissingInput { node: usize, input: usize },
    Cycle,
}

impl fmt::Display for GraphError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::DuplicateNode(id) => write!(f, "ID de nó duplicado: {id}"),
            Self::MissingInput { node, input } => write!(f, "nó {node} referencia entrada ausente {input}"),
            Self::Cycle => write!(f, "o grafo contém um ciclo"),
        }
    }
}

impl std::error::Error for GraphError {}

pub struct GraphJitCompiler {
    pub optimization_level: u8,
}

impl GraphJitCompiler {
    pub fn new(optimization_level: u8) -> Self {
        Self { optimization_level }
    }

    /// Valida as dependências e planeja MatMul→ReLU se a saída da MatMul só for
    /// consumida pela ReLU. O nível 0 desativa fusões; níveis acima de 0 usam a regra.
    pub fn compile_and_fuse(&self, nodes: &[GraphNode]) -> Result<Vec<KernelPlan>, GraphError> {
        let mut by_id = HashMap::with_capacity(nodes.len());
        for (index, node) in nodes.iter().enumerate() {
            if by_id.insert(node.id, index).is_some() {
                return Err(GraphError::DuplicateNode(node.id));
            }
        }

        let mut indegree = vec![0usize; nodes.len()];
        let mut children = vec![Vec::new(); nodes.len()];
        let mut consumers: HashMap<usize, usize> = HashMap::new();
        for (index, node) in nodes.iter().enumerate() {
            for input_id in &node.inputs {
                let Some(&parent) = by_id.get(input_id) else {
                    return Err(GraphError::MissingInput { node: node.id, input: *input_id });
                };
                indegree[index] += 1;
                children[parent].push(index);
                *consumers.entry(*input_id).or_default() += 1;
            }
        }

        let mut ready: VecDeque<usize> = indegree.iter().enumerate()
            .filter_map(|(i, degree)| (*degree == 0).then_some(i)).collect();
        let mut order = Vec::with_capacity(nodes.len());
        while let Some(index) = ready.pop_front() {
            order.push(index);
            for child in &children[index] {
                indegree[*child] -= 1;
                if indegree[*child] == 0 {
                    ready.push_back(*child);
                }
            }
        }
        if order.len() != nodes.len() {
            return Err(GraphError::Cycle);
        }

        let mut fused = HashSet::new();
        let mut plan = Vec::new();
        for &index in &order {
            let node = &nodes[index];
            if fused.contains(&node.id) {
                continue;
            }
            let eligible = self.optimization_level > 0 && node.op == OpType::MatrixMultiply
                && consumers.get(&node.id).copied().unwrap_or(0) == 1;
            let relu = if eligible {
                order.iter().find_map(|&candidate| {
                    let next = &nodes[candidate];
                    (next.op == OpType::ReLU && next.inputs.as_slice() == [node.id]).then_some(next)
                })
            } else { None };

            if let Some(relu) = relu {
                fused.insert(relu.id);
                plan.push(KernelPlan::FusedMatMulRelu { matmul: node.id, relu: relu.id });
            } else {
                plan.push(KernelPlan::Single { node: node.id, op: node.op.clone() });
            }
        }
        Ok(plan)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fuses_only_single_consumer_matmul_relu() {
        let graph = vec![
            GraphNode { id: 1, op: OpType::MatrixMultiply, inputs: vec![] },
            GraphNode { id: 2, op: OpType::ReLU, inputs: vec![1] },
            GraphNode { id: 3, op: OpType::VectorAdd, inputs: vec![2] },
        ];
        let plan = GraphJitCompiler::new(1).compile_and_fuse(&graph).unwrap();
        assert_eq!(plan[0], KernelPlan::FusedMatMulRelu { matmul: 1, relu: 2 });
        assert_eq!(plan.len(), 2);
    }

    #[test]
    fn rejects_missing_inputs_and_cycles() {
        let missing = vec![GraphNode { id: 1, op: OpType::ReLU, inputs: vec![9] }];
        assert!(matches!(GraphJitCompiler::new(1).compile_and_fuse(&missing), Err(GraphError::MissingInput { .. })));
        let cycle = vec![
            GraphNode { id: 1, op: OpType::ReLU, inputs: vec![2] },
            GraphNode { id: 2, op: OpType::ReLU, inputs: vec![1] },
        ];
        assert_eq!(GraphJitCompiler::new(1).compile_and_fuse(&cycle), Err(GraphError::Cycle));
    }
}
