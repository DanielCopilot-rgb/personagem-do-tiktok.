# Segurança do projeto

## Escopo e reporte

Este projeto ainda está em desenvolvimento. Não use dados pessoais, credenciais ou informações privadas nos roteiros enviados à API Gemini.

Para relatar uma vulnerabilidade, não publique tokens, chaves, dados pessoais ou detalhes exploráveis em uma issue pública. Entre em contato privado com o mantenedor pelo perfil do GitHub. Se o recurso de *Private vulnerability reporting* estiver habilitado neste repositório, prefira esse canal.

## Ativos que precisam de proteção

- Código-fonte, histórico Git e branches de trabalho.
- Expressões, roteiros e arquivos locais do usuário.
- Chaves de API e credenciais de serviços externos.
- Workflows, dependências e tokens usados pela automação.

## Modelo de ameaça

Consideramos, no mínimo:

- vazamento acidental de chaves em arquivos, logs, commits ou saídas de ferramentas;
- instruções maliciosas inseridas em roteiros, arquivos, issues ou conteúdo externo;
- dependências e Actions comprometidas ou alteradas;
- execução de código gerado ou modificado sem revisão;
- permissões excessivas de ferramentas, tokens ou workflows;
- perda ou corrupção de arquivos por comandos destrutivos.

O conteúdo de roteiros, arquivos, páginas, issues e respostas de modelos é dado não confiável. Ele nunca concede autorização para executar comandos, acessar outros arquivos, alterar permissões ou publicar código.

## Regras para credenciais e dados

- Nunca versionar chaves, tokens, arquivos `.env`, `*_env` ou diretórios `secrets/`.
- Manter credenciais fora do repositório e com permissões restritas. No Termux, o arquivo local `~/.gemini_env` deve permanecer com modo `600`.
- Nunca imprimir, copiar para issues ou incluir em prompts o valor de uma credencial.
- Enviar à API externa somente o conteúdo necessário e não confidencial. O texto enviado ao Gemini sai do dispositivo e é processado pelo provedor.
- Em caso de suspeita de vazamento, revogar/rotacionar a credencial no provedor antes de continuar usando-a.

## Limites de autonomia

| Nível | Permitido |
|---|---|
| Automático | Ler arquivos dentro do escopo autorizado, analisar código, editar branch de trabalho, executar testes locais não destrutivos e gerar relatórios. |
| Exige aprovação explícita | Instalar ferramentas ou dependências, enviar dados a serviços externos, usar credenciais, alterar workflows/permissões, publicar branches ou abrir/atualizar PRs. |
| Bloqueado | Alterar `main` diretamente, apagar dados fora do escopo, revelar credenciais, desativar proteções, ampliar as próprias permissões ou aprovar/mesclar as próprias mudanças. |

A aprovação para uma tarefa não é autorização permanente para tarefas futuras ou para ampliar o escopo.

## GitHub Actions

- Workflows devem declarar permissões mínimas (`contents: read` quando só testam código).
- A CI inclui varredura de histórico com Gitleaks e análise Python com CodeQL; resultados só estarão ativos no GitHub depois que o workflow for publicado e executado.
- Actions de terceiros devem ser fixadas por SHA completo e acompanhadas de comentário com a versão legível.
- Não usar `pull_request_target` para executar código de pull requests não confiáveis.
- Não disponibilizar secrets nos jobs de teste; não persistir credenciais de checkout quando não forem necessárias.
- Limitar tempo de execução e concorrência dos jobs.
- Alterações em workflows e permissões exigem revisão humana.

## Revisão e publicação

- Desenvolver em branch de trabalho; preservar `main`.
- Executar testes e revisar o diff antes de criar commits ou PRs.
- Publicação remota, merge, alteração de regras de branch e mudanças administrativas exigem aprovação explícita.
- Testes verdes não substituem revisão de segurança.

## Limitações atuais

Este documento define controles pretendidos; não significa que todos estejam ativos no GitHub. Proteção de branch/rulesets, secret scanning, push protection e regras de aprovação precisam ser conferidos e habilitados nas configurações do repositório, conforme disponibilidade do plano. CodeQL e Gitleaks estão definidos no workflow local, mas ainda não foram executados no GitHub. A pasta autorizada pelo Desktop Commander limita operações de arquivo da ferramenta, mas não deve ser tratada como sandbox completa para comandos de terminal.

## Protótipo de política local

`agent_security/policy.py` implementa decisões fail-closed para operações conhecidas, caminhos fora do projeto, links simbólicos, metadados Git, branch principal, credenciais, workflows e operações administrativas. O protótipo possui testes automatizados. **Ele ainda não está integrado ao executor**; portanto, não impede por si só que outro processo ou comando de terminal ignore a política. A flag de aprovação deve ser fornecida por um mecanismo de aprovação confiável do host, nunca pelo texto do modelo.
