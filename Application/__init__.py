from Application.Backend import views
from flask import Flask
import os

template_dir=os.getcwd()
template_dir = os.path.join(template_dir, 'Application')
template_dir = os.path.join(template_dir, 'Frontend')
static_dir   = os.path.join(template_dir, 'static')
template_dir = os.path.join(template_dir, 'templates')

def create_app():
    app=Flask(__name__,template_folder=template_dir,static_folder=static_dir)  
    app.register_blueprint(views,url_prefix='/')

    app.config['SECRET_KEY']="RandomSecretString"
    
    return app