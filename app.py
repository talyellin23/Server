from flask import Flask, redirect
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session
from data import users

app = Flask(__name__)
app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)


@app.route('/')
def main_page():
    return redirect('/Home screen')


@app.route('/Home screen')
def homepage():
    return render_template('Home Screen.html')


@app.route('/Contact us')
def contact_page():
    return render_template('Contact us.html')


@app.route('/assignment3_1')
def assignment3_1():  # put application's code here
    items = {'#1': 'Maccabi shirt', '#2': 'Maccabi pajamas', '#3': 'Maccabi pants', '#4': 'Maccabi shoes',
             '#5': 'Maccabi scarf'}
    size = ['small', 'medium', 'large']
    additional_products = ('Official ball', 'Maccabi hat', 'Maccabi bottle', 'Maccabi bag')
    return render_template('assignment3_1.html',
                           items=items,
                           size=size,
                           additional_products=additional_products)


@app.route('/assignment3_2', methods=['GET', 'POST'])
def assignment3_2():
    results_users = {}
    registration_data = {}

    if 'search' in request.args:
        search_data = request.args['search']
        if search_data == '':
            results_users = users
        else:
            for user, data in users.items():
                if search_data == data["name"] or search_data == data["email"]:
                    results_users.update({
                        user: users[user]
                    })

    if request.method == 'POST' and len(request.form) > 0:
        user_name = request.form['userName']
        user_email = request.form['email']
        session['username'] = user_name
        session['login'] = True

        num_of_users = len(users) + 1
        new_user_key = 'user{user_number}'.format(user_number=num_of_users)

        users.update({
            new_user_key: {
                'name': user_name,
                'email': user_email
            }
        })

        print(users)

    return render_template('assignment3_2.html',
                           results_users=results_users,
                           registration_data=registration_data)


@app.route('/log_out', methods=['GET', 'POST'])
def logout_func():
    print(1)
    session['login'] = False
    session.clear()
    return redirect(url_for('assignment3_2'))


if __name__ == '__main__':
    app.run(debug=True)
