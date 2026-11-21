# Orçamento de IA — Personagem do TikTok

## Objetivo
Evitar desperdício de tokens, chamadas desnecessárias e ciclos infinitos do agente.

## Regras de economia

- Enviar somente os arquivos relevantes para cada tarefa.
- Não reenviar o projeto inteiro quando um resumo for suficiente.
- Priorizar diffs e trechos específicos de código.
- Não usar IA para operações que podem ser feitas por scripts.
- Não repetir análises sem uma justificativa.
- Registrar erros e resultados para evitar retrabalho.

## Limites iniciais provisórios

- Máximo de 3 chamadas de IA por tarefa simples.
- Máximo de 2 ciclos de correção após uma tentativa inicial.
- Uma tarefa por vez.
- Interromper a execução se o agente não conseguir avançar.
- Solicitar aprovação humana quando houver risco de perda de dados ou alteração estrutural importante.

Esses limites serão revisados após os primeiros testes.

## Medição

Registrar em cada execução:

- Modelo utilizado.
- Quantidade de chamadas.
- Tokens de entrada, quando disponíveis.
- Tokens de saída, quando disponíveis.
- Custo estimado, quando aplicável.
- Resultado: sucesso, falha ou interrupção.

## Critérios de parada

O agente deve parar quando:

- A tarefa estiver concluída e os testes passarem.
- Atingir o limite de chamadas ou correções.
- Encontrar um erro que não consiga resolver.
- Precisar de uma credencial ou autorização não disponível.
- Identificar risco de comprometer arquivos ou dados.

## Orçamento financeiro

Ainda não definido.
Será estabelecido depois de verificar os modelos, as cotas gratuitas e os preços atuais.
