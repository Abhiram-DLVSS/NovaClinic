from flask import Flask

def create_app():
    app=Flask(__name__,template_folder='Frontend\\templates',static_folder='Frontend\static')
    
    app.config['SECRET_KEY']='secretKEY'
    from Application.Backend import views,auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    return app

