from app import create_app
from app.middleware.logger import LoggerMiddleware
from app.middleware.rate_limiter import RateLimiterMiddleware

app = create_app()
app.wsgi_app = LoggerMiddleware(app.wsgi_app)
app.wsgi_app = RateLimiterMiddleware(app.wsgi_app, limit=100, period=60)

if __name__ == '__main__':
    app.run()
