import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit

from apps.config import config_dict
from apps import configure_database, create_app, db, register_blueprints, register_extensions

import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

# # WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
UPLOAD_FOLDER = 'apps/static/uploads/'


# # The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
# app = Flask(__name__, template_folder="/Users/tranlephuongthao/Documents/event2022-HealthHackathon/AIDIA-Rehabilitation-Management/apps/templates")
# app.secret_key = "secret key"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024
# app.config.from_object(app_config)
# register_extensions(app)
# register_blueprints(app)
# configure_database(app)
Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)
    
if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('FLASK_ENV        = ' + os.getenv('FLASK_ENV') )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT )


@app.route('/')
def upload_form():
	return render_template('home/ui-input-inputs.html')

@app.route('/', methods=['POST'])
def upload_video():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	else:
		filename = secure_filename(file.filename)
		file.save(os.path.join('apps/static/uploads/', filename))
		#print('upload_video filename: ' + filename)
		flash('Video successfully uploaded and displayed below')
		return render_template('home/ui-input-inputs.html', filename=filename)

@app.route('/display/<filename>')
def display_video(filename):
	#print('display_video filename: ' + filename)
	return redirect(url_for('apps/static/', filename='uploads/' + filename), code=302)


@app.errorhandler(413)
def largefile_error(filename):
 return redirect(url_for('apps/static/', filename='uploads/' + filename)), 413


if __name__ == "__main__":
    app.run()