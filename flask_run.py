#!venv/bin/python

if __name__ == '__main__':
    from src.web.server import flask_app

    from waitress import serve
    serve(flask_app, host="0.0.0.0", port=8080)
