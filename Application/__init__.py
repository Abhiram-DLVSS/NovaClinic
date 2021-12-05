from flask import Flask
import os

# template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir=os.getcwd()
template_dir = os.path.join(template_dir, 'Application')
template_dir = os.path.join(template_dir, 'Frontend')
static_dir=os.path.join(template_dir, 'static')
template_dir = os.path.join(template_dir, 'templates')
def create_app():
    app=Flask(__name__,template_folder=template_dir,static_folder=static_dir)
    
    
    app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
    # app.config['SECRET_KEY']="secretKEY"
    from Application.Backend import auth
    
    app.register_blueprint(auth,url_prefix='/')

    return app