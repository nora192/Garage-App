from flask import Flask

def create_app():
    app = Flask(__name__)

    app.secret_key = 'a254c02dfc64e941476ea38cc3f382a3'
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app