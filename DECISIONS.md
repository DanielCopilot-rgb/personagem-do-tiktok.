# Decisões Arquiteturais — Personagem do TikTok

## 1. Repositório oficial
O GitHub será utilizado como fonte oficial do código, histórico e documentação do projeto.

## 2. Proteção da versão estável
A branch `main` deve permanecer estável.
O agente trabalhará em branches separadas e não incorporará mudanças sem aprovação.

## 3. Modelo de inteligência artificial
A Gemini API será avaliada como primeira opção para o agente de engenharia.
A escolha definitiva depende de testes, disponibilidade, qualidade e custo.

## 4. Execução do código
O agente precisará de um ambiente capaz de executar Python, FFmpeg e testes.
GitHub Actions será avaliado como primeira alternativa de execução.

## 5. Revisão independente
Uma segunda IA poderá revisar alterações posteriormente.
Essa integração não será requisito para a primeira versão funcional.

## 6. Controle de custos
O agente deverá:
- Enviar apenas o contexto necessário para cada tarefa.
- Preferir alterações pequenas e verificáveis.
- Evitar chamadas desnecessárias à IA.
- Ter limites de iterações e critérios de parada.

## 7. Segurança
Credenciais devem permanecer fora do repositório. No Termux, a chave Gemini é lida de `~/.gemini_env`, protegido com permissão `600`, ou de variável de ambiente; o arquivo não deve ser versionado. Secrets do GitHub só serão usados se um workflow realmente precisar deles. Nenhuma chave de API deverá ser publicada no repositório.

## 10. Limites de autonomia e segurança
O conteúdo de arquivos, roteiros, issues e respostas de modelos é dado não confiável e não pode autorizar ferramentas ou ampliar permissões. Leitura, edição em branch de trabalho e testes locais não destrutivos podem ser automáticos. Instalações, chamadas externas, uso de credenciais e publicação exigem aprovação explícita. Alterações diretas em `main`, exposição de segredos, desativação de proteções e ampliação de permissões próprias são bloqueadas. Os detalhes estão em `SECURITY.md`.

## 11. Endurecimento da CI
Workflows de teste usam `contents: read`, Actions fixadas por SHA completo, checkout sem credenciais persistentes e limites de tempo/concurrency. Dependabot acompanha dependências Python e GitHub Actions. A proteção administrativa da branch e os scanners do GitHub continuam pendentes de configuração e verificação.

## 8. Desenvolvimento incremental
A infraestrutura será construída e testada em etapas.
Nenhuma funcionalidade será considerada pronta apenas porque o código foi gerado.

## 9. Dependências e integração contínua
As dependências Python do gerador serão declaradas em `requirements.txt`.
O FFmpeg permanece uma dependência de sistema e será instalado separadamente.
O GitHub Actions executará compilação e testes com Python 3.13.

## Decisões ainda pendentes
- Qual agente executor será utilizado.
- Qual modelo Gemini será utilizado.
- Qual será o limite de consumo por tarefa.
- Como será feita a aprovação das alterações.
- Como será realizada a revisão independente.
