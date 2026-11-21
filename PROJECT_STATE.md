# Estado do Projeto — Personagem do TikTok

## Objetivo
Desenvolver um sistema para criar vídeos curtos com um personagem animado,
a partir de histórias escritas pelo usuário.

## Estrutura atual

- `expressoes/`: imagens PNG das expressões do personagem.
- `gerador/fantoche.py`: renderiza vídeos verticais e legendas SRT.
- `gerador/interpretador.py`: interpreta roteiros e associa expressões.
- `gerador/gemini.py`: utiliza a API Gemini para analisar histórias e produzir cenas em JSON.
- `gerador/story_maker.py`: permite criar e administrar histórias pelo terminal.
- `gerador/historias/`: histórias e análises em JSON.

## Funcionalidades existentes

- Geração de vídeos MP4 verticais.
- Geração de legendas SRT.
- Animação da boca com alternância de imagens.
- Sincronização aproximada da boca com áudio WAV.
- Interpretação de roteiros TXT.
- Leitura de cenas em JSON.
- Análise de histórias pela API Gemini.

## Ambiente conhecido

- Desenvolvimento inicial em Android.
- Termux e Python.
- FFmpeg, Pillow e NumPy utilizados pelo gerador.
- Repositório GitHub como histórico oficial do código.

## Limitações conhecidas

- Ainda não existe uma suíte de testes automatizados.
- O Gemini atual analisa histórias, mas não administra o desenvolvimento do software.
- Ainda não existe um agente autônomo capaz de planejar, editar, testar e revisar o projeto.
- A qualidade visual e a sincronização dos vídeos precisam de avaliação prática.

## Governança

- `main` deve permanecer estável.
- Novas funcionalidades devem ser desenvolvidas em branches separadas.
- Alterações precisam ser testadas antes de serem incorporadas à `main`.
- Nenhuma credencial deve ser armazenada no repositório.
- Backups e arquivos originais importantes devem ser preservados.

## Estado atual do desenvolvimento

Estamos preparando a infraestrutura para um agente de engenharia de software.
A branch atual é `setup/agent-foundation`.

Ainda não há agente autônomo implementado.
