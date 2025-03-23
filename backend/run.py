from app import create_app
from app.middleware.logger import LoggerMiddleware

app = create_app()
app.wsgi_app = LoggerMiddleware(app.wsgi_app)

if __name__ == '__main__':
    app.run()
