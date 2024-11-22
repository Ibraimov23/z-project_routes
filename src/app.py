from flask import Flask, redirect, url_for, session
from routes import auth_bp, dashboard_bp
from datetime import timedelta
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.permanent_session_lifetime = timedelta(hours=1)

app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('dashboard.dashboard')) 
    return redirect(url_for('auth.login')) 

if __name__ == "__main__":
    app.run(debug=True)
