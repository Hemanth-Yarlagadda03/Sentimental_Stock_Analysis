from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'flask_app/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'html'}

from flask_app import routes
