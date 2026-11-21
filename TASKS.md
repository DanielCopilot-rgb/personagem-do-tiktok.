# Backlog — Personagem do TikTok

## Prioridade 1 — Preparar a base

- [x] Revisar a estrutura atual do repositório.
- [x] Confirmar dependências e instruções de instalação.
- [x] Criar testes automatizados básicos.
- [x] Configurar verificação automática com GitHub Actions.

## Prioridade 2 — Criar o ciclo do agente

- [ ] Definir como o agente recebe tarefas.
- [ ] Permitir que o agente leia os arquivos necessários.
- [ ] Permitir que o agente proponha e aplique alterações.
- [ ] Executar testes automaticamente após alterações.
- [ ] Gerar um relatório do trabalho realizado.

## Prioridade 3 — Integrar inteligência artificial

- [ ] Avaliar a Gemini API para atuar como modelo principal.
- [ ] Controlar o consumo de tokens e chamadas.
- [ ] Implementar limites de execução e critérios de parada.
- [ ] Preparar uma etapa de revisão independente.

## Prioridade 4 — Segurança e autonomia

- [x] Definir modelo inicial de ameaça e níveis de autonomia em `SECURITY.md`.
- [x] Manter credenciais locais fora do repositório e proteger `~/.gemini_env` com permissão `600`.
- [x] Restringir o workflow de CI a `contents: read`, fixar Actions por SHA e desativar credenciais persistentes no checkout.
- [x] Configurar Dependabot para dependências Python e GitHub Actions.
- [x] Manter o desenvolvimento na branch `setup/agent-foundation`, sem alterações diretas em `main`.
- [ ] Configurar ruleset/branch protection em `main` (aprovação humana necessária).
- [ ] Verificar e habilitar secret scanning e push protection, conforme disponibilidade do repositório/plano.
- [ ] Avaliar Gitleaks e CodeQL e integrar verificações de segurança à CI.
- [ ] Criar sandbox de execução e controlador de permissões independente do agente.
- [ ] Definir procedimento de aprovação para publicação remota e merge.

## Fora do escopo inicial

- [ ] Execução contínua ou noturna sem supervisão.
- [ ] Múltiplos agentes editando arquivos simultaneamente.
- [ ] Sistema multi-IA complexo antes de validar o ciclo básico.
