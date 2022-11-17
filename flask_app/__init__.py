from flask import Flask
from pathlib import Path
import os

from flask_app.config.flask_template_filter import * 

app = Flask(__name__)
app.secret_key = "This is a secret key that No one(1) should know!"

ini_template_filters(app)

    # UPLOAD FILES CONFIG
UPLOAD_FOLDER = f"{Path(__file__).parent}\\static\\uploaded_images\\"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


CHECK_FOLDER = os.path.isdir(UPLOAD_FOLDER)
if not CHECK_FOLDER:
    os.makedirs(UPLOAD_FOLDER)

#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
