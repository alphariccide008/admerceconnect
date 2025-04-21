from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


csrf=CSRFProtect()
"""Create app"""
def create_app():
    """Keep all imports that may casue conflict within this function so that anytime we write from pkg... imports.. none of these satements will be executed"""
    from package.models import db
    app= Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile("config.py",silent=True)
    db.init_app(app)
    migrate=Migrate(app,db)
    csrf.init_app(app)
    return app
app=create_app()

from package import user_routes,admin_routes
