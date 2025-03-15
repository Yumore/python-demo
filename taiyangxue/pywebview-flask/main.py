import webview

from app import app

if __name__ == '__main__':
    window = webview.create_window('Pywebview', app)
    webview.start()
