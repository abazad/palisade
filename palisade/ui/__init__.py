from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
    

app = Flask(__name__)


@app.route('/admin/user')
def admin_user():
    pass

if __name__ == '__main__':
    app.run()