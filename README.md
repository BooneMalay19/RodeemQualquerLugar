# Doom Chocolate Streaming Project

## Requisitos

- Python 3.10+
- Chocolate Doom (https://www.chocolate-doom.org/)
- pip install -r requirements.txt

## Como usar

1. Abra o Doom Chocolate.
2. No terminal:
```bash
cd app
python server.py
```
3. Acesse http://127.0.0.1:8080
4. Para injetar o stream em um vídeo do YouTube:
   - Abra o console do navegador (F12).
   - Cole o conteúdo de `injector/inject.js`.

## Notas
- Funciona para qualquer jogo, basta abrir em modo janela.
- Ajuste o nome da janela no `server.py` se necessário.