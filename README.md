# Cupcakes C

Aplicação web demonstrativa criada para o Projeto Integrador Transdisciplinar em Engenharia de Software II. O projeto apresenta um fluxo de pedido de cupcakes, do catálogo ao acompanhamento, e registra as melhorias feitas após avaliação por colegas.

**Aplicação publicada:** https://takacaio.pythonanywhere.com/

## O que dá para demonstrar

- Catálogo com cupcakes avulsos e combos de 6 e 15 unidades.
- Montagem e edição de sabores dos combos.
- Carrinho, faixas de frete e checkout demonstrativo.
- Acompanhamento de pedido, histórico por sessão do navegador e avaliação após a entrega.
- Perfil com dados fixos de demonstração e preferência de tema claro/escuro.

A entrada não autentica com o Google. Não há cobrança, dados bancários, localização ou endereço real do cliente. Endereços, método de pagamento e chave Pix são exemplos fixos.

## Tecnologias

Python 3.13, Flask, SQLite, HTML, CSS e JavaScript. O código separa as rotas e o fluxo de controle, os modelos de acesso ao banco e os templates das telas.

## Rodar no Windows

Com Python 3.13 instalado, abra o terminal na pasta do projeto e execute, um comando por vez:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

Acesse http://127.0.0.1:5000. Para executar os testes automatizados:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Na execução registrada em 16/11/2026, os oito testes passaram. O banco local é criado em `instance/cupcakesc.sqlite3`; os testes usam um banco temporário.

## Documentação do projeto

- `docs/MANUAL_USO_CUPCAKESC.md`: roteiro rápido para usar o aplicativo.
- `docs/engenharia/Documentacao_Tecnica_Atualizada_CupcakesC.pdf`: escopo técnico, diagramas e modelos de dados.
- `docs/engenharia/Dicionario_Dados_CupcakesC.pdf`: campos da tabela SQLite atual e proposta lógica separada.
- `docs/engenharia/Especificacao_IHC_CupcakesC.pdf`: fluxo, telas e interações.
- `docs/testes/Laudo_Testes_Automatizados_CupcakesC.pdf`: execução e resultado dos testes.
- `docs/testes/sintese_avaliacao_pares.md`: síntese anônima dos comentários e decisões sobre melhorias.

A pasta `docs/testes` também contém o formulário e o roteiro usados na rodada de avaliação por pares.
