from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

    
from palisade.ui.admin import admin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jopa'

app.register_blueprint(admin, url_prefix='/admin')

@app.route('/')
def admin_user():
    pass

if __name__ == '__main__':
#    print app.url_map
    app.run(debug=True)