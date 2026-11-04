# Git-do-Projeto-AGI-Core

Protótipos de engenharia para módulos desacoplados da arquitetura AGI. O conteúdo desta branch é código demonstrativo e não comprova operação global, propriedades de segurança certificadas ou desempenho de produção.

## Módulos 60–79

O catálogo está em [`docs/modules-60-79.md`](docs/modules-60-79.md). Protótipos incluídos:

- **M60:** fachada de KEM pós-quântico que exige um backend criptográfico real; não inventa chaves ou segredos.
- **M65:** validação de DAG e planejamento de fusão MatMul→ReLU; não gera código nativo nem executa kernels.
- **M70:** normalização de mensagens JSON e quadros CAN clássicos; não implementa transporte gRPC, WebSocket ou acesso ao barramento.
- **M75:** estimador de variância preditiva e entropia para distribuições de probabilidade, usando apenas a biblioteca padrão do Python.

## Executar verificações

```sh
cargo test
python -m unittest discover -s python -v
```

M60 permanece deliberadamente sem backend por padrão. Para uso real, integre uma implementação ML-KEM mantida e validada, confira a conformidade com FIPS 203, proteja o ciclo de vida das chaves e submeta o sistema a revisão criptográfica. Os exemplos não devem ser usados para proteger dados ou controlar sistemas críticos sem validação independente.
