from flask import Flask

def create_app():
    app = Flask(__name__)
    with app.app_context():
        from . import routes
    return app


from flask import Flask
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__)

    # Конфигурация для почты
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Почтовый сервер (например, Gmail)
    app.config['MAIL_PORT'] = 587  # Порт для TLS
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Ваша почта
    app.config['MAIL_PASSWORD'] = 'your_password'  # Пароль или App Password

    mail.init_app(app)

    with app.app_context():
        from . import routes
    return app