import os
from flask import Flask, redirect, url_for
from app.db import init_db_engine, db_session, Base

def create_app(test_config=None):
    """Application Factory Pattern for Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # Ensure instance directory exists
    os.makedirs(app.instance_path, exist_ok=True)
    default_db_path = os.path.join(app.instance_path, 'student_performance.db')

    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'se-project-secret-key-jss-aiml-2026'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI', f'sqlite:///{default_db_path}'),
        ML_MODEL_PATH=os.environ.get('ML_MODEL_PATH', os.path.abspath(os.path.join(app.root_path, '..', 'ml', 'models', 'best_student_model.joblib')))
    )

    if test_config:
        app.config.from_mapping(test_config)

    # Initialize SQLAlchemy database engine
    init_db_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    # Cleanup scoped database session after each request
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.faculty import faculty_bp
    from app.routes.student import student_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(faculty_bp, url_prefix='/faculty')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app
