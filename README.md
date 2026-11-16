# Cupcakes C

Aplicação web demonstrativa desenvolvida para o Projeto Integrador Transdisciplinar II.

## Estado atual

A tela de entrada simula uma autenticação sem chamar o Google e sem pedir e-mail ou senha. O catálogo inicial usa os produtos e valores apresentados no protótipo do Projeto Integrador I. O projeto usa Flask e SQLite local.

A aplicação é apenas uma demonstração acadêmica: não solicita dados pessoais reais, não processa pagamentos reais e não solicita localização. O pedido demonstrativo guarda um nome fixo e um resumo do pedido para mostrar o histórico.

## Estrutura

- app/controllers: rotas e fluxo da aplicação
- app/models: acesso e inicialização do banco SQLite
- app/templates: páginas HTML
- app/static: CSS e outros arquivos estáticos
- app/config.py: valores de demonstração e catálogo editáveis
- instance: banco local criado durante a execução (ignorado pelo Git)

## Preparar e executar no Windows

Abra o terminal do VS Code dentro da pasta do projeto e rode os comandos, um por vez:

1. Criar o ambiente virtual:
   py -3.13 -m venv .venv
2. Ativar:
   .\.venv\Scripts\Activate.ps1
3. Instalar dependências:
   python -m pip install -r requirements.txt
4. Iniciar:
   python run.py

Depois, abra http://127.0.0.1:5000 no navegador.

Se o PowerShell bloquear a ativação, não altere a política do computador; avise para seguirmos sem ativar o ambiente.

## Testes automatizados

Com o ambiente virtual pronto, execute no terminal do VS Code:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes usam um banco temporário, separado do banco local usado durante a demonstração.
Última execução nesta etapa: 6 testes aprovados.

## Avaliação por colegas

- `docs/testes/roteiro_avaliacao_pares.md`: tarefas sugeridas para os avaliadores.
- `docs/testes/formulario_avaliacao_pares.md`: formulário com espaço para cinco avaliações e a síntese das melhorias.
- `docs/testes/formulario_avaliacao_pares.docx`: cópia editável em Word do formulário.
- `docs/testes/acesso_remoto_temporario.md`: instruções para disponibilizar o app aos avaliadores por um endereço temporário.

Para testes remotos temporários, pare o servidor local de desenvolvimento, instale as dependências atualizadas e use `run_remote.py` com o `cloudflared`. Isso mantém o banco SQLite no computador do estudante. O endereço do túnel funciona apenas enquanto os dois processos e o computador permanecerem ativos.

## Tema

O tema claro é o padrão. A preferência entre claro e escuro é escolhida no Perfil e fica salva localmente no navegador.

## Navegação

Após entrar, a barra inferior oferece acesso ao Catálogo, Meus pedidos, Carrinho e Perfil. O histórico de pedidos é filtrado pelo navegador usado no teste.
## Fluxo de seleção e carrinho

O catálogo permite adicionar cupcakes avulsos ou escolher a quantidade de cada sabor para completar as caixas de 6 e 15. O carrinho fica na sessão local do navegador, sem nome ou e-mail; cada navegador de teste mantém seu próprio carrinho.

Os valores de produtos, frete demonstrativo e tempos podem ser alterados em app/config.py. A finalização simulada grava apenas um resumo demonstrativo do pedido no SQLite local; não salva dados de pagamento nem localização. O identificador de sessão do navegador separa o histórico de cada perfil de navegador usado nos testes.

Na tela de checkout, os endereços e formas de pagamento são ilustrativos. A chave `cupcakesc123` é fictícia e serve somente para demonstrar a cópia do texto; não há QR Code nem integração Pix. O pedido guarda apenas a categoria selecionada (Crédito, Débito ou Pix), sem dados financeiros. Os estados avançam automaticamente, com consulta em segundo plano para evitar recarregar a página.
