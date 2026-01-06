import webbrowser
import threading
import time
import uvicorn
from web.main import app


def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:8000")


if __name__ == "__main__":
    # Abre o navegador em paralelo (não daemon)
    threading.Thread(target=open_browser).start()

    # BLOQUEIA o processo com o servidor
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
