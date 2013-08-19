from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

from palisade.db.schema import SQ_User
from palisade.db.conn import Session

from forms import LoginForm
    
from palisade.ui.admin import admin
from palisade.ui.user import user

from jinja_filters import tomegabyte
from decorators import login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jopa'

#Register custome Jinja filters
app.jinja_env.filters['tomegabyte'] = tomegabyte

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')

def check_credential(user, form):
    if user.password == form['password']:
        return True
    else:
        return False

@app.route('/login', methods=['GET', 'POST'])
def login():    
    db = Session()
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = db.query(SQ_User).filter(SQ_User.login==request.form['login']).first()
        if check_credential(user, request.form):
            session['logged_in'] = True
            session['current_user'] = user.login   
            session['is_admin'] = user.is_admin                           
            return redirect(url_for('user.show_user'))
        else:
            flash('Invalid login or password!')
            return redirect(url_for('login'))
    else:        
        return render_template('login.html', form=form, next=next) 

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)
    session.pop('current_user', None)
    session.pop('is_admin', None)
    flash('You are were logged out!')
    return redirect(url_for('login'))

if __name__ == '__main__':
#    print app.url_map
    app.run(debug=True)