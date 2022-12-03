#!venv/bin/python

if __name__ == '__main__':
    from waitress import serve
    from src.web.server import create_tables, flask_app

    create_tables()
    serve(flask_app)
    # flask_app.run()