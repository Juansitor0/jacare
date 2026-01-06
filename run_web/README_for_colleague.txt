Jacaré Inventory — instruções para executar o EXE

Arquivos incluídos:
- run_web.exe (EXE principal)

Passos para executar:
1. Extraia/baixe o arquivo `run_web.zip` e copie `run_web.exe` para uma pasta local.
2. Se o Windows bloquear o arquivo após o download, clique com o botão direito em `run_web.exe` -> Propriedades -> e clique em "Desbloquear" (ou execute no PowerShell: `Unblock-File -Path .\\run_web.exe`).
3. Dê um duplo-clique em `run_web.exe` para iniciar a aplicação.
   - Alternativamente, abra PowerShell na pasta e execute: `Start-Process .\\run_web.exe` 
   - Para executar como Administrador: `Start-Process -FilePath .\\run_web.exe -Verb RunAs`
4. Abra o navegador em: http://127.0.0.1:8000

Observações:
- Se o Windows Defender/SmartScreen bloquear, autorize o arquivo nas configurações do Defender ou na janela de bloqueio do SmartScreen.
- Se preferir, posso enviar instruções passo-a-passo para o colega via Teams ou criar um atalho.

Contato: se houver algum erro, peça para copiar/colar a mensagem que aparece no console.
