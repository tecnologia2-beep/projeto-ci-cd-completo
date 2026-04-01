# RELATÓRIO TÉCNICO – PIPELINE CI/CD

## Introdução
Este projeto evoluiu de um pipeline apenas de CI para um fluxo completo de CI/CD.

## Etapas implementadas
- Provisionamento do ambiente Ubuntu no GitHub Actions
- Subida do MySQL para testes
- Instalação do Python e dependências
- Inicialização do banco com `init.sql`
- Execução de testes automatizados com `pytest`
- Execução de smoke test da API Flask
- Build da imagem Docker
- Publicação da imagem no GHCR
- Deploy automático em servidor Linux via SSH

## Resultado
Agora o projeto não apenas valida o código automaticamente, mas também publica e entrega a aplicação após sucesso nos testes.
