#!/usr/bin/env python3
"""
WSGI entry point for Palace of Quests.
Production-ready, robust logging, error handling, and configuration.
"""

import os
import sys
import logging
from pathlib import Path
import traceback

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

class WSGIConfigurationError(Exception):
    """Custom exception for WSGI configuration issues."""

class WSGIApplication:
    """
    WSGI application wrapper with strong configuration, logging, and error handling.
    """

    def __init__(self):
        self.logger = self._setup_logging()
        self.project_root = self._configure_project_path()
        self.application = self._create_application()

    def _setup_logging(self) -> logging.Logger:
        """Configure logging for both console and rotating file in production."""
        log_format = (
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        logger = logging.getLogger("palace_of_quests_wsgi")
        logger.setLevel(logging.INFO)

        # Console handler (always enabled)
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter(log_format))
        logger.addHandler(ch)

        # Rotating file handler (production)
        if self._is_production():
            from logging.handlers import RotatingFileHandler
            log_file = Path('/var/log/palace_of_quests/wsgi.log')
            try:
                log_file.parent.mkdir(parents=True, exist_ok=True)
                fh = RotatingFileHandler(
                    log_file, maxBytes=10 * 1024 * 1024, backupCount=3
                )
                fh.setFormatter(logging.Formatter(log_format))
                logger.addHandler(fh)
            except (OSError, PermissionError) as e:
                logger.warning(f"Could not set up file logging: {e}")

        return logger

    def _is_production(self) -> bool:
        """Detect if running in a production environment."""
        flask_env = os.getenv('FLASK_ENV', '').strip().lower()
        return (
            flask_env == 'production'
            or os.getenv('PYTHONANYWHERE_DOMAIN') is not None
        )

    def _configure_project_path(self) -> Path:
        """Configure and validate project root path."""
        try:
            project_root = Path(__file__).resolve().parent

            if not self._validate_project_structure(project_root):
                raise WSGIConfigurationError(
                    f"Invalid project structure at {project_root}"
                )

            project_str = str(project_root)
            if project_str not in sys.path:
                sys.path.insert(0, project_str)
                self.logger.info(f"Added project root to sys.path: {project_str}")

            return project_root

        except Exception as e:
            error_msg = f"Failed to configure project path: {e}"
            self.logger.error(error_msg, exc_info=True)
            raise WSGIConfigurationError(error_msg) from e

    def _validate_project_structure(self, project_root: Path) -> bool:
        """Ensure all essential project files exist."""
        required_files = ['app.py', 'app/__init__.py']
        missing = [f for f in required_files if not (project_root / f).exists()]
        if missing:
            self.logger.warning(
                f"Missing required files: {', '.join(missing)} in {project_root}"
            )
            return False
        return True

    def _create_application(self):
        """Create and configure the Flask WSGI application."""
        try:
            app_factory = self._import_app_factory()
            app = app_factory() if callable(app_factory) else app_factory

            self._configure_production_settings(app)
            self.logger.info("WSGI application successfully initialized")
            return app

        except Exception as e:
            error_msg = f"Failed to create WSGI application: {e}"
            self.logger.error(error_msg, exc_info=True)
            raise WSGIConfigurationError(error_msg) from e

    def _import_app_factory(self):
        """Try different strategies to find the Flask app or factory."""
        import_strategies = [
            ('app', 'create_app'),
            ('app', 'app'),
            ('main', 'create_app'),
            ('main', 'app'),
        ]
        for module_name, factory_name in import_strategies:
            try:
                module = __import__(module_name, fromlist=[factory_name])
                factory = getattr(module, factory_name, None)
                if factory:
                    self.logger.info(f"Imported '{factory_name}' from '{module_name}'")
                    return factory
            except ImportError as e:
                self.logger.debug(
                    f"Could not import '{factory_name}' from '{module_name}': {e}"
                )
                continue
        raise ImportError(
            "Could not import Flask application factory. "
            "Ensure 'create_app' or 'app' exists in app.py or app/__init__.py"
        )

    def _configure_production_settings(self, app):
        """Apply production-specific configurations."""
        if not self._is_production():
            return

        try:
            app.config['DEBUG'] = False
            app.config['TESTING'] = False

            if not app.config.get('SECRET_KEY'):
                self.logger.warning("SECRET_KEY not configured for production")

            # Set secure headers if not using Flask-Talisman
            @app.after_request
            def set_security_headers(response):
                response.headers.setdefault('X-Content-Type-Options', 'nosniff')
                response.headers.setdefault('X-Frame-Options', 'DENY')
                response.headers.setdefault('Content-Security-Policy', "default-src 'self'")
                return response

            self.logger.info("Production configuration applied")
        except Exception as e:
            self.logger.warning(f"Could not apply production settings: {e}")

    def __call__(self, environ, start_response):
        """WSGI application callable with error handling."""
        try:
            return self.application(environ, start_response)
        except Exception as e:
            self.logger.error(
                f"Unhandled WSGI error: {e}\n{traceback.format_exc()}"
            )
            status = '500 Internal Server Error'
            headers = [('Content-Type', 'text/html; charset=utf-8')]
            start_response(status, headers)
            return [self._get_error_page().encode('utf-8')]

    def _get_error_page(self) -> str:
        """Return a professional error page (inline for now)."""
        if self._is_production():
            return (
                "<!DOCTYPE html>"
                "<html><head><title>Service Temporarily Unavailable</title>"
                "<style>"
                "body{font-family:Arial,sans-serif;text-align:center;margin-top:50px;background:#f5f5f5;}"
                ".error-container{background:#fff;padding:40px;border-radius:8px;display:inline-block;box-shadow:0 2px 10px rgba(0,0,0,0.1);}"
                "</style></head><body>"
                '<div class="error-container">'
                "<h1>Service Temporarily Unavailable</h1>"
                "<p>We're experiencing technical difficulties. Please try again later.</p>"
                "</div></body></html>"
            )
        return (
            "<h1>Development Server Error</h1>"
            "<p>Check the server logs for detailed error information.</p>"
        )

try:
    wsgi_app = WSGIApplication()
    application = wsgi_app  # PythonAnywhere expects 'application'
    flask_app = wsgi_app.application  # For direct Flask access in dev
except Exception as e:
    import logging
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger("palace_of_quests_wsgi")
    logger.error(f"Critical WSGI initialization failure: {e}", exc_info=True)

    def error_application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'WSGI configuration error. Check server logs.']

    application = error_application

def health_check() -> dict:
    """Simple health check for monitoring tools."""
    try:
        db_status = "unknown"
        return {
            'status': 'healthy',
            'timestamp': os.environ.get('REQUEST_TIME_FLOAT', 'unknown'),
            'python_version': sys.version,
            'project_root': str(getattr(wsgi_app, "project_root", "unknown")),
            'db_status': db_status,
        }
    except Exception as e:
        logging.error(f"Health check error: {e}")
        return {'status': 'unhealthy', 'error': str(e)}

if __name__ == '__main__':
    print("WSGI Configuration Test")
    print("=" * 50)
    try:
        if 'wsgi_app' in locals():
            print(f"✓ Project root: {wsgi_app.project_root}")
            print(f"✓ Flask app: {wsgi_app.application}")
            print("✓ WSGI application configured successfully")
            test_environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}
            def test_start_response(status, headers): pass
            result = application(test_environ, test_start_response)
            print("✓ WSGI callable test passed")
        else:
            print("✗ WSGI application failed to initialize")
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        sys.exit(1)
