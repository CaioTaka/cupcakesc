# Acesso remoto temporário para avaliadores

Para uma rodada de avaliação, use um Cloudflare Quick Tunnel. Ele publica temporariamente o servidor local em um endereço `trycloudflare.com`, sem exigir domínio ou conta Cloudflare. O banco SQLite continua no computador do estudante.

## Antes de começar

- Instale o pacote de dependências do projeto, que inclui o servidor WSGI Waitress.
- Baixe o `cloudflared` para Windows pelo site oficial da Cloudflare.
- O endereço temporário pode ser aberto por qualquer pessoa que receba o link. Envie-o somente aos avaliadores e ao tutor; não o publique no GitHub ou em redes sociais.
- O computador precisa permanecer ligado, conectado à internet e sem entrar em suspensão durante os testes.

## Iniciar a aplicação

1. No terminal que está executando `run.py`, pressione `Ctrl+C` para encerrar o servidor local de desenvolvimento.
2. Abra um terminal na pasta do projeto e instale as dependências atualizadas:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Inicie o servidor remoto, que usa Waitress e não ativa o depurador:

   ```powershell
   .\.venv\Scripts\python.exe run_remote.py
   ```

4. Abra outro terminal e inicie o túnel:

   ```powershell
   cloudflared tunnel --url http://127.0.0.1:5000
   ```

5. Copie o endereço `https://...trycloudflare.com` exibido no terminal e envie-o aos avaliadores.

## Encerrar

Quando a rodada terminar, pressione `Ctrl+C` no terminal do `cloudflared` e no terminal do `run_remote.py`. O endereço temporário deixa de funcionar quando o túnel é encerrado. Se iniciar outra vez, será criado um endereço diferente.

## Observações

- Quick Tunnels são destinados a testes e desenvolvimento, não a hospedagem permanente.
- O aplicativo e o SQLite ficam no computador local. Os pedidos permanecem separados por sessão de navegador.
- Não use dados pessoais, credenciais ou pagamentos reais. O aplicativo continua sendo uma demonstração acadêmica.
- Se `cloudflared` não for reconhecido no PowerShell, use o caminho completo para o arquivo `cloudflared.exe` que foi baixado.
