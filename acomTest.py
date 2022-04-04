from flask import Flask,render_template,request, url_for, redirect, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import json
from sqlbox import acomManager
import time


'''
flask
'''

app=Flask(__name__)
app.secret_key = 'write your secret key'

'''
web manager
'''

manager = acomManager()
manager.sqlpassword = 'Chu0622.'
manager.acomdb = 'acom'
manager.acomtable = 'dns'
manager.logindb = 'web'


'''
Login items
'''

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(name):
    userbox = manager.get(name)
    if userbox is None:
        return

    user = User()
    user.id = name
    return user


@login_manager.request_loader
def request_loader(request):
    name = request.form.get('username')

    userbox = manager.get(name)
    if userbox is None:
        return

    user = User()
    user.id = name

    user.is_authenticated = request.form['password'] == userbox['password']

    return user


'''
Web items
'''

@app.route('/', methods=['POST', 'GET'])
def home():

    manager.import_db()

    dns_dict = manager.get_dns()


    if request.method == 'GET':
        return render_template('home.html', header_items = header_items, dns_header = dns_header, dns_dict = dns_dict)

    sourceip = request.form['sourceip']
    fromTime = request.form['from-time']
    toTime = request.form['to-time']
    fqdn = request.form['fqdn']
    if (sourceip is not None) and (fromTime is not None) and (toTime is not None) and (fqdn is not None):

        manager.dns_sort = manager.check_dns(sourceip, fromTime, toTime, fqdn)

        return redirect(url_for('search'))

    return render_template('home.html', header_items = header_items, dns_header = dns_header, dns_dict = dns_dict)


@app.route('/search', methods=['GET', 'POST'])
def search():

    return render_template('search.html', header_items = header_items, dns_header = dns_header, dns_dict = manager.dns_sort)


@app.route('/login',methods=['POST','GET'])
def login():

    if request.method == 'GET':
        return render_template('login.html', header_items = header_items)

    name = request.form['username']
    userbox = manager.get(name)
    if (name is not None) and (request.form['password'] == userbox['password']):
        user = User()
        user.id = name
        login_user(user)
        return redirect(url_for('actress')) # redirect: 填入def函式名稱

    return render_template('login.html', header_items = header_items, userbox = userbox)


@app.route('/logout', methods=['POST','GET'])
def logout():
    logout_user()
    return redirect(url_for('actress'))


@app.route('/register', methods=['POST','GET'])
def register():

    if request.method == 'GET':
        return render_template('register.html', header_items = header_items)

    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    isUsed = manager.push(email, username, password)
    if isUsed:
        return redirect(url_for('login'))

    return render_template('register.html', header_items = header_items, isUsed = isUsed)


'''
Input items
'''

header_items = [{'name': 'Home', 'url': '/'}, 
                {'name': 'Login', 'url': '../login'},
                {'name': 'Register', 'url': '../register'}]

dns_header = ['date', 'time', 'usec', 'sourceip','sourceport', 'destinationip', 'destimationport', 'fqdn']


'''
Start
'''

if __name__ == '__main__':
	app.run(host='0.0.0.0',port='5000',debug=True)


