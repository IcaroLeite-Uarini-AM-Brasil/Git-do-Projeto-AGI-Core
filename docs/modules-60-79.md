# Catálogo da Camada H — Módulos 60 a 79

Este catálogo descreve escopo pretendido, não afirma que todos os módulos estão implementados. Nesta branch há protótipos apenas para M60, M65, M70 e M75. Os demais são itens de planejamento.

| ID | Módulo | Linguagem prevista | Escopo / estado |
|---|---|---|---|
| M60 | Post-Quantum Crypto | Rust | Fachada KEM; exige backend real ML-KEM/FIPS 203, ainda não fornecido. |
| M61 | Homomorphic Engine | Rust/C++ | Computação homomórfica; planejamento. |
| M62 | Differential Privacy Budget | Python | Contabilidade de orçamento de privacidade; planejamento. |
| M63 | Secure MPC Controller | Rust | Orquestração de computação multipartidária; planejamento. |
| M64 | Hardware Enclave Driver | Rust | Integração com enclave de hardware; planejamento e dependente de plataforma. |
| M65 | Dynamic Graph JIT | Rust/LLVM | Validação de DAG e plano de fusão; sem geração/execução JIT. |
| M66 | Tensor Layout Auto-Tuner | Python | Exploração de layouts para tensores; planejamento. |
| M67 | Sparse Matrix Engine | Rust | Operações em matrizes esparsas; planejamento. |
| M68 | Memory Bandwidth Throttle | Rust | Controle de contenção de memória; planejamento. |
| M69 | Kernel Fusion Pipeline | Rust/CUDA | Fusão de kernels executáveis; planejamento, distinto do planejador M65. |
| M70 | Universal Protocol Translator | Rust | Normalização de JSON tipado e CAN clássico; sem transporte ou acesso a hardware. |
| M71 | Micro-NPU Dispatcher | Rust | Despacho para aceleradores; planejamento. |
| M72 | Satellite Mesh Gateway | Rust | Encaminhamento tolerante a interrupções; planejamento. |
| M73 | Drone Kinematics Controller | Rust/ROS 2 | Controle cinemático; planejamento, exige análise de segurança antes de uso físico. |
| M74 | Sensor Calibration Unit | Rust | Calibração de sensores; planejamento. |
| M75 | Epistemic Uncertainty Estimator | Python | Variância média entre amostras e entropia; protótipo com validação de entradas. |
| M76 | Dynamic Drift Detector | Rust | Detecção de mudança de distribuição; planejamento. |
| M77 | Counterfactual Simulator | Python | Avaliação de cenários contrafactuais; planejamento. |
| M78 | Cognitive Load Balancer | Rust | Escalonamento de carga; planejamento. |
| M79 | Self-Correction Proof Generator | Rust/Lean4 | Geração/verificação de provas; planejamento. |

## Limites de segurança e validação

- M60 não faz criptografia até que um backend auditado seja integrado; a fachada evita retornar segredos simulados como se fossem reais.
- M65 apenas gera um plano estrutural. A fusão deve ser validada quanto a semântica, efeitos colaterais, precisão numérica e layout de memória antes de qualquer codegen.
- M70 trata mensagens em memória. Não conecte diretamente entradas não confiáveis a atuadores; valide autenticação, autorização, replay, limites e esquema na camada de transporte.
- M75 oferece indicadores estatísticos, não uma garantia de calibração nem um critério autônomo para ações de alto impacto.
