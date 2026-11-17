# Estado do projeto

Atualizado em 17 de novembro de 2026.

## Versão atual

O Cupcakes C está publicado em https://takacaio.pythonanywhere.com/ e pode ser acessado por HTTPS. A aplicação foi conferida no computador e no celular. A hospedagem é o PythonAnywhere, em conta gratuita Beginner.

A versão publicada oferece catálogo de cupcakes e combos, carrinho com edição de sabores, checkout de demonstração, acompanhamento do pedido, histórico por sessão de navegador, avaliação por pedido, perfil e tema claro/escuro. O horário dos pedidos é exibido no fuso de São Paulo, no formato DD/MM/AAAA HH:MM.

Os limites da demonstração permanecem claros: a conta, os endereços e os pagamentos são fictícios; não há cobrança, autenticação Google, coleta de localização nem rastreamento real.

## Avaliação e qualidade

Cinco colegas testaram o fluxo em 09/11/2026. As observações e decisões estão documentadas em `docs/testes/sintese_avaliacao_pares.md`. Entre as melhorias adotadas estão editar combos no carrinho, preservar a posição da tela ao atualizar quantidades, diferenciar as formas de pagamento de demonstração, rever mensagens e ilustrações e permitir avaliar o pedido entregue. Busca no catálogo, avaliação pública por sabor e compartilhamento da entrega ficaram fora do escopo desta versão.

A suíte automatizada foi executada localmente em 16/11/2026: 8 testes aprovados. O laudo registra o comando, a versão do código e o ambiente usados.

## Documentação disponível

- Manual rápido de uso em `docs/MANUAL_USO_CUPCAKESC.md`.
- Diagramas UML, arquitetura e modelos de dados em `docs/engenharia/Documentacao_Tecnica_Atualizada_CupcakesC.pdf`.
- Dicionário da tabela SQLite atual em `docs/engenharia/Dicionario_Dados_CupcakesC.pdf`.
- Especificação de IHC em `docs/engenharia/Especificacao_IHC_CupcakesC.pdf`.
- Síntese anônima dos testes por pares e laudo automatizado em `docs/testes/`.

O formulário preenchido com identificação dos avaliadores e os vídeos são mantidos nos materiais de submissão da disciplina; a síntese pública do repositório não expõe nomes dos colegas.

## Rodar localmente

No Windows, com Python 3.13 instalado, execute na pasta do projeto:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

Acesse http://127.0.0.1:5000. Para executar os testes:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

O banco SQLite local é criado em `instance/cupcakesc.sqlite3`. O arquivo é ignorado pelo Git. A hospedagem possui seu próprio banco; registros entre ambientes não são sincronizados.
