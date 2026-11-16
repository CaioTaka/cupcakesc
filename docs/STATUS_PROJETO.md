# Estado do projeto

Atualizado em 16 de novembro de 2026.

## Onde o projeto está

- O Cupcakes C está salvo localmente na pasta `CupcakesC`.
- A versão de referência e a rodada de feedback estão publicadas em `main` até o commit `8774ba1`.
- As cinco avaliações por pares foram recebidas e consolidadas. A síntese e as decisões estão em `docs/testes/sintese_avaliacao_pares.md`.
- A rodada publicada inclui controles de quantidade do carrinho sem recarga e identificação da conta por um atalho de perfil, em vez do quadro que parecia pesquisa.
- A rodada local em andamento acrescenta imagens específicas para preparo e entrega concluída, logo do protótipo, avaliação individual de pedidos, dados fixos de endereço e cartão no Perfil, retorno à tela anterior e prazos de 15 s para preparo e 30 s para entrega.
- O projeto mantém catálogo, combos editáveis, checkout demonstrativo, registro local de pedidos, acompanhamento do status, histórico por navegador, navegação inferior e tema claro/escuro.
- O README registra que seis testes automatizados passaram na execução anterior. Eles não foram executados novamente nesta rodada.

## Próximas ações

1. Conferir o fluxo atualizado no navegador e corrigir qualquer problema visual ou funcional encontrado.
2. Executar a validação local antes de criar um novo commit; depois revisar o diff e publicar quando o estudante autorizar.
3. Preparar a hospedagem permanente CADY em etapa separada, considerando persistência do SQLite e configuração segura do Flask.
4. Atualizar a documentação final e anexar as cinco avaliações, respeitando a privacidade dos avaliadores.
5. Confirmar com a tutoria a divergência entre “até cinco minutos” e “pelo menos cinco minutos” para o vídeo.

## Como os avaliadores podem acessar

O servidor atual é local: `http://127.0.0.1:5000`. Ele só abre no computador em que o Flask está rodando. A opção mais simples é fazer os cinco testes presencialmente nesse computador, em momentos separados, usando um perfil de navegador diferente por avaliador. Para avaliação remota, será necessário preparar uma hospedagem ou outro acesso de rede antes de compartilhar um endereço.

Envie uma cópia do formulário Word para cada avaliador e peça que devolvam a cópia preenchida. Também pode imprimir o formulário. Cada avaliador deve registrar nome, data, o que funcionou, o que falhou e o que não conseguiu testar, com o motivo. Capturas de tela são opcionais; não devem conter senha nem dados financeiros.

## Comandos úteis

Iniciar o aplicativo no PowerShell, dentro da pasta do projeto:

```powershell
.\.venv\Scripts\python.exe run.py
```

Executar os testes automatizados:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## GitHub

O remoto `origin` aponta para `https://github.com/CaioTaka/cupcakesc.git`. Os commits `4f2cd55` e `8774ba1` estão publicados em `main`. As mudanças desta rodada permanecem locais até serem revisadas e autorizadas para publicação.
