from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from config.config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app(config_name='development'):
    """
    Application factory pattern
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from app.routes import auth, patients, providers, appointments, medical_records, telemed, omnicognitor, m23m_research, genomic_data, microbiome_data, wearable_data, blood_test_results, nutrition_plans
    
    app.register_blueprint(auth.auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patients.bp, url_prefix='/api/patients')
    app.register_blueprint(providers.bp, url_prefix='/api/providers')
    app.register_blueprint(appointments.appointments_bp, url_prefix='/api/appointments')
    app.register_blueprint(medical_records.medical_records_bp, url_prefix='/api/medical-records')
    app.register_blueprint(telemed.telemed_bp, url_prefix='/api/telemed')
    app.register_blueprint(omnicognitor.omnicognitor_bp, url_prefix='/api/omnicognitor')
    app.register_blueprint(m23m_research.m23m_research_bp, url_prefix='/api/m23m-research')
    app.register_blueprint(genomic_data.genomic_data_bp, url_prefix='/api/genomic-data')
    app.register_blueprint(microbiome_data.microbiome_data_bp, url_prefix='/api/microbiome-data')
    app.register_blueprint(wearable_data.wearable_data_bp, url_prefix='/api/wearable-data')
    app.register_blueprint(blood_test_results.blood_test_results_bp, url_prefix='/api/blood-test-results')
    app.register_blueprint(nutrition_plans.nutrition_plans_bp, url_prefix='/api/nutrition-plans')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'Healthcare Hub API'}, 200
    
    # Root endpoint
    @app.route('/')
    def index():
        return {
            'message': 'Healthcare Technology Park API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'auth': '/api/auth',
                'patients': '/api/patients',
                'providers': '/api/providers',
                'appointments': '/api/appointments',
                'medical_records': '/api/medical-records',
                'telemed': '/api/telemed',
                'omnicognitor': '/api/omnicognitor',
                'm23m_research': '/api/m23m-research',
                'genomic_data': '/api/genomic-data',
                'microbiome_data': '/api/microbiome-data',
                'wearable_data': '/api/wearable-data',
                'blood_test_results': '/api/blood-test-results',
                'nutrition_plans': '/api/nutrition-plans'
            }
        }, 200
    
    return app
