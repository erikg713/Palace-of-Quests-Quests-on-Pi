def register_middlewares(app):
    from .logger import setup_logging
    from .rate_limiter import init_rate_limiter
    from .error_handler import register_error_handlers
    from .security import init_security_headers

    setup_logging(app)
    init_rate_limiter(app)
    register_error_handlers(app)
    init_security_headers(app)
