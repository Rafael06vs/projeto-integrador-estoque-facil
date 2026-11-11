# Estoque Fácil — Projeto Integrador (Programação Web)

Sistema acadêmico de controle de estoque com Python, Flask, SQLite, HTML e CSS.

## Como executar

1. Instale Python 3.10 ou superior.
2. Abra o terminal nesta pasta.
3. Execute `python -m pip install -r requirements.txt`.
4. Execute `python app.py`.
5. Abra `http://127.0.0.1:5000` no navegador.

No Windows, se necessário, substitua `python` por `py`.

O banco `estoque.db` é criado automaticamente na primeira execução.

## Funcionalidades

- Cadastro de produtos com categoria, quantidade e estoque mínimo;
- Pesquisa por nome ou categoria;
- Entrada e saída de produtos, com validação de saldo;
- Indicador de itens com estoque baixo;
- Histórico das oito últimas movimentações;
- Exclusão de produto com confirmação.

## Organização

- `app.py`: rotas, regras de negócio e banco SQLite;
- `templates/index.html`: página web;
- `static/style.css`: aparência;
- `requirements.txt`: dependências;
- `RELATORIO_PROJETO_INTEGRADOR.docx`: documentação acadêmica editável.

## Limitações

Aplicação demonstrativa local, sem login, autenticação ou controles de produção. Não hospedar publicamente sem adicionar segurança, CSRF, autenticação e configuração apropriada. O modo `debug=True` é apenas para desenvolvimento local.

## Entrega acadêmica

O roteiro da UNISA solicita relatório com revisão bibliográfica, escopo, documentação do código e programa executável, além de link do repositório na capa. Após subir este projeto no GitHub, inclua o endereço no relatório e complete os campos de identificação. Confira com o professor se a opção de documentação é suficiente.
