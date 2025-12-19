from flask import Flask
from config import SECRET_KEY

from routes.user_routes import user_bp
from routes.hospital_routes import hospital_bp
from routes.doctor_routes import doctor_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.register_blueprint(user_bp)
app.register_blueprint(hospital_bp)
app.register_blueprint(doctor_bp)

if __name__ == "__main__":
    app.run(debug=True)
