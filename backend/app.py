from flask import Flask
from core.config import Config
from core.extensions import db,bcrypt,jwt,cors
from core.models.models import create_admin
from core.routes.auth_routes import auth_bp
from core.routes.admin_routes import admin_bp
from core.routes.doctor_routes import doctor_bp
from core.routes.patient_routes import patient_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app,origins=["http://localhost:5173"])

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(doctor_bp, url_prefix="/api/doctor")
    app.register_blueprint(patient_bp, url_prefix="/api/patient")

    with app.app_context():
        db.create_all()
        create_admin()
    return app

if __name__ ==  '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)