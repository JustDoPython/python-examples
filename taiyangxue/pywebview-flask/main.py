import webview
from contextlib import redirect_stdout
from io import StringIO
from app import app

if __name__ == '__main__':
    window = webview.create_window('Pywebview', app)
    webview.start()