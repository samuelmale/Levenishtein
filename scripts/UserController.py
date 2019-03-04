from flask import Flask ,flash,render_template , redirect ,request,session
from flask_login import  LoginManager , login_user, logout_user,login_required , UserMixin
from flask.templating import render_template_string
from flask.signals import template_rendered

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'login' # the login view of your application
app.config['SECRET_KEY'] = "lkkajdghdadkglajkgah" # Secret key for app

class User(UserMixin):
    def __init__(self,id):
        self.id = id
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def home():
    return render_template("login.html")
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/protected')
@login_required
def protected():
    return "This page is protected"

@app.route('/login', methods=['POST'])
def login():
    login_user(User(1))
    if request.form['password'] == 'password'  and request.form['username'] == 'admin':
        session['logged_in'] = True
        return render_template("index.html")
    else:
        flash('Sorry You Provided The Wrong Password ,Try again')
    return flash('Sorry You Provided The Wrong Password ,Try again')

@app.route('/logout/')
@login_required
def logout():
    session['logged_in']=False
    logout_user()
    return home()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1212, debug=True)