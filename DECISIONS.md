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
- Receber apenas o contexto necessário para cada tarefa.
- Preferir alterações pequenas e verificáveis.
- Evitar chamadas desnecessárias à IA.
- Ter limites de iterações e critérios de parada.

## 7. Segurança
Credenciais serão armazenadas em variáveis de ambiente ou secrets.
Nenhuma chave de API deverá ser publicada no repositório.

## 8. Desenvolvimento incremental
A infraestrutura será construída e testada em etapas.
Nenhuma funcionalidade será considerada pronta apenas porque o código foi gerado.

## Decisões ainda pendentes
- Qual agente executor será utilizado.
- Qual modelo Gemini será utilizado.
- Qual será o limite de consumo por tarefa.
- Como será feita a aprovação das alterações.
- Como será realizada a revisão independente.
