# hn-digest

## um agregador de notícias do Hacker News via CLI

Objetivo: um comando hn-digest --limit 20 que busca as top N histórias do Hacker News de forma concorrente, exibe título, score e URL, e compara o tempo de execução entre modo sequencial e concorrente.

Propósito: revisar conceitos e atualizar o conhecimento sobre novas bibliotecas e boas práticas.

Endpoints:

- https://hacker-news.firebaseio.com/v0/topstories.json → lista de IDs
- https://hacker-news.firebaseio.com/v0/item/{id}.json → detalhes de cada item

