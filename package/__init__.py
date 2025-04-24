from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail


csrf=CSRFProtect()
mail = Mail() 
"""Create app"""
def create_app():
    """Keep all imports that may casue conflict within this function so that anytime we write from pkg... imports.. none of these satements will be executed"""
    from package.models import db
    app= Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile("config.py",silent=True)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Update if using a different provider
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'goldcapitalfinance@gmail.com'  # Your email
    app.config['MAIL_PASSWORD'] = 'mcuh srmx ktve kphq'  # Your email password or app password
    app.config['MAIL_DEFAULT_SENDER'] = 'noreply@goldcapitalinvestment.pythonanywhere.com'
    db.init_app(app)
    migrate=Migrate(app,db)
    csrf.init_app(app)

    mail.init_app(app)
    return app
app=create_app()




from package import user_routes,admin_routes
