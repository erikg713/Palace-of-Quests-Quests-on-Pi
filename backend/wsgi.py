#!/usr/bin/env python3
"""
WSGI Configuration for Palace of Quests
Production-ready WSGI entry point with comprehensive error handling and logging.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional
import traceback


class WSGIConfigurationError(Exception):
    """Custom exception for WSGI configuration errors."""
    pass


class WSGIApplication:
    """
    WSGI application wrapper with enhanced configuration and error handling.
    """
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.project_root = self._configure_project_path()
        self.application = self._create_application()
    
    def _setup_logging(self) -> logging.Logger:
        """
        Configure production-grade logging with proper formatting.
        """
        log_format = (
            '%(asctime)s - %(name)s - %(levelname)s - '
            '[%(filename)s:%(lineno)d] - %(message)s'
        )
        
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        logger = logging.getLogger(__name__)
        
        # Add file handler for production environments
        if self._is_production():
            try:
                log_file = Path('/var/log/palace_of_quests/wsgi.log')
                log_file.parent.mkdir(parents=True, exist_ok=True)
                
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(logging.Formatter(log_format))
                logger.addHandler(file_handler)
            except (OSError, PermissionError) as e:
                logger.warning(f"Could not setup file logging: {e}")
        
        return logger
    
    def _is_production(self) -> bool:
        """Check if running in production environment."""
        return os.getenv('FLASK_ENV', '').lower() == 'production' or \
               os.getenv('PYTHONANYWHERE_DOMAIN') is not None
    
    def _configure_project_path(self) -> Path:
        """
        Dynamically configure and validate project root path.
        """
        try:
            project_root = Path(__file__).resolve().parent
            
            # Validate project structure
            if not self._validate_project_structure(project_root):
                raise WSGIConfigurationError(
                    f"Invalid project structure at {project_root}"
                )
            
            # Add to Python path if not already present
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
        """
        Validate that essential project files exist.
        """
        required_files = ['app.py', 'app/__init__.py']
        
        for file_path in required_files:
            if (project_root / file_path).exists():
                return True
        
        self.logger.warning(
            f"Could not find app.py or app/__init__.py in {project_root}"
        )
        return False
    
    def _create_application(self):
        """
        Create and configure the Flask WSGI application.
        """
        try:
            # Import with fallback strategies
            app_factory = self._import_app_factory()
            
            # Create application instance
            app = app_factory()
            
            # Configure for production if needed
            self._configure_production_settings(app)
            
            self.logger.info("WSGI application successfully initialized")
            return app
            
        except Exception as e:
            error_msg = f"Failed to create WSGI application: {e}"
            self.logger.error(error_msg, exc_info=True)
            raise WSGIConfigurationError(error_msg) from e
    
    def _import_app_factory(self):
        """
        Import application factory with multiple fallback strategies.
        """
        import_strategies = [
            ('app', 'create_app'),
            ('app', 'app'),
            ('main', 'create_app'),
            ('main', 'app'),
            ('__init__', 'create_app'),
        ]
        
        for module_name, factory_name in import_strategies:
            try:
                module = __import__(module_name, fromlist=[factory_name])
                factory = getattr(module, factory_name, None)
                
                if factory is not None:
                    self.logger.info(
                        f"Successfully imported '{factory_name}' from '{module_name}'"
                    )
                    return factory
                    
            except ImportError as e:
                self.logger.debug(
                    f"Could not import '{factory_name}' from '{module_name}': {e}"
                )
                continue
        
        raise ImportError(
            "Could not import Flask application factory. "
            "Ensure 'create_app' function exists in app.py or app/__init__.py"
        )
    
    def _configure_production_settings(self, app) -> None:
        """
        Apply production-specific configurations.
        """
        if not self._is_production():
            return
        
        try:
            # Disable debug mode in production
            app.config['DEBUG'] = False
            app.config['TESTING'] = False
            
            # Set secure session configuration
            if not app.config.get('SECRET_KEY'):
                self.logger.warning("SECRET_KEY not configured for production")
            
            # Configure security headers if using Flask-Talisman
            if hasattr(app, 'talisman'):
                app.config['TALISMAN_FORCE_HTTPS'] = True
            
            self.logger.info("Production configuration applied")
            
        except Exception as e:
            self.logger.warning(f"Could not apply production settings: {e}")
    
    def __call__(self, environ, start_response):
        """
        WSGI application callable with enhanced error handling.
        """
        try:
            return self.application(environ, start_response)
        except Exception as e:
            self.logger.error(
                f"Unhandled WSGI error: {e}\n{traceback.format_exc()}"
            )
            
            # Return a proper HTTP 500 response
            status = '500 Internal Server Error'
            headers = [('Content-Type', 'text/html; charset=utf-8')]
            start_response(status, headers)
            
            return [self._get_error_page().encode('utf-8')]
    
    def _get_error_page(self) -> str:
        """
        Generate a professional error page for production.
        """
        if self._is_production():
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Service Temporarily Unavailable</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; 
                           margin-top: 50px; background-color: #f5f5f5; }
                    .error-container { background: white; padding: 40px; 
                                     border-radius: 8px; display: inline-block;
                                     box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                </style>
            </head>
            <body>
                <div class="error-container">
                    <h1>Service Temporarily Unavailable</h1>
                    <p>We're experiencing technical difficulties. Please try again later.</p>
                </div>
            </body>
            </html>
            """
        else:
            return """
            <h1>Development Server Error</h1>
            <p>Check the console logs for detailed error information.</p>
            """


# Initialize the WSGI application
try:
    wsgi_app = WSGIApplication()
    application = wsgi_app  # PythonAnywhere expects 'application'
    
    # Also provide direct access to the Flask app for debugging
    flask_app = wsgi_app.application
    
except Exception as e:
    # Fallback error handling for critical failures
    import logging
    logging.basicConfig(level=logging.ERROR)
    logger = logging.getLogger(__name__)
    logger.error(f"Critical WSGI initialization failure: {e}", exc_info=True)
    
    # Create a minimal error application
    def error_application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'WSGI configuration error. Check server logs.']
    
    application = error_application


# Health check endpoint for monitoring
def health_check():
    """Simple health check function for monitoring tools."""
    try:
        return {
            'status': 'healthy',
            'timestamp': os.environ.get('REQUEST_TIME_FLOAT', 'unknown'),
            'python_version': sys.version,
            'project_root': str(wsgi_app.project_root) if 'wsgi_app' in locals() else 'unknown'
        }
    except Exception:
        return {'status': 'unhealthy'}


if __name__ == '__main__':
    # Development server for local testing
    print("WSGI Configuration Test")
    print("=" * 50)
    
    try:
        if 'wsgi_app' in locals():
            print(f"✓ Project root: {wsgi_app.project_root}")
            print(f"✓ Flask app: {wsgi_app.application}")
            print("✓ WSGI application configured successfully")
            
            # Test import
            test_environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/'}
            def test_start_response(status, headers): pass
            
            result = application(test_environ, test_start_response)
            print("✓ WSGI callable test passed")
            
        else:
            print("✗ WSGI application failed to initialize")
            
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        sys.exit(1)
