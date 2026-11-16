# Estado do projeto

Atualizado em 16 de novembro de 2026.

## Onde o projeto está

- O Cupcakes C está salvo localmente na pasta `CupcakesC`.
- A versão funcional aprovada foi registrada no commit local `4f2cd55`.
- As cinco avaliações por pares foram recebidas e consolidadas. A síntese e as decisões estão em `docs/testes/sintese_avaliacao_pares.md`.
- Esta rodada implementa duas melhorias: controles de quantidade do carrinho sem recarga e identificação da conta por um atalho de perfil, em vez do quadro que parecia pesquisa.
- O projeto mantém catálogo, combos editáveis, checkout demonstrativo, registro local de pedidos, acompanhamento do status, histórico por navegador, navegação inferior e tema claro/escuro.
- O README registra que seis testes automatizados passaram na execução anterior. Eles não foram executados novamente nesta rodada.

## Próximas ações

1. Revisar as melhorias desta rodada e executar a validação local antes de publicar a versão atualizada.
2. Criar o commit das melhorias e enviar os commits ao GitHub quando a autenticação do Git estiver disponível.
3. Preparar a hospedagem permanente CADY em etapa separada; nenhuma configuração de hospedagem foi alterada nesta rodada.
4. Atualizar a documentação final e anexar as cinco avaliações, respeitando a privacidade dos avaliadores.
5. Entregar o vídeo gravado e confirmar com a tutoria a divergência entre “até cinco minutos” e “pelo menos cinco minutos”.

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

O remoto `origin` aponta para `https://github.com/CaioTaka/cupcakesc.git`. O commit inicial existe localmente, mas o envio ao GitHub ainda precisa ser concluído no terminal do usuário porque o gerenciador de credenciais não iniciou nesta sessão.
