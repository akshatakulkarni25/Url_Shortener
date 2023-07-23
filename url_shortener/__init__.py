from flask import Flask
from extensions import db
from routes import short


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
    db.init_app(app)
    app.app_context().push()

    # db.create_all()

    app.register_blueprint(short)
    return app


if __name__ == "__main__":
    App = create_app()
    App.run(debug=True)
