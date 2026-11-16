# Estado do projeto

Atualizado em 9 de novembro de 2026.

## Onde o projeto está

- O Cupcakes C está salvo localmente na pasta `CupcakesC`.
- A MEP 9 foi aprovada pelo estudante. Inclui catálogo, combos editáveis no carrinho, checkout demonstrativo, registro local de pedidos, escolha da categoria de pagamento, acompanhamento sem recarga da página, histórico por navegador, navegação inferior e tema claro/escuro.
- A etapa final de validação está em andamento. Os seis testes automatizados passaram na última execução.
- O roteiro e o formulário para cinco avaliadores estão em `docs/testes`.
- O formulário Word foi gerado a partir do modelo Markdown. A prévia visual automática não pôde ser feita neste ambiente porque LibreOffice não está instalado e a automação do Word foi bloqueada; abrir no Word e conferir a paginação antes de distribuir.

## Próximas ações

1. Convidar cinco colegas ou profissionais para testar o aplicativo.
2. Reunir uma avaliação preenchida por pessoa e trazer as respostas para análise.
3. Escolher e implementar as sugestões pertinentes; depois repetir os testes.
4. Organizar as cinco avaliações e a síntese das alterações em PDF.
5. Gravar o vídeo de apresentação conforme a duração pedida pelo tutor.

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

O remoto `origin` está configurado para `https://github.com/CaioTaka/cupcakesc.git`, mas o trabalho atual ainda não foi commitado nem enviado. Antes de publicar, revisar as alterações e o que será incluído no repositório.
