import json

from flask import Blueprint, render_template, request, jsonify, session
import requests
import mysql.connector

# assignment4 blueprint definition
assignment_4 = Blueprint('assignment_4', __name__,
                         static_folder='static',
                         static_url_path='/pages/assignment4',
                         template_folder='templates')

# outer_source blueprint definition
outer_source = Blueprint('outer_source', __name__,
                         static_folder='static',
                         static_url_path='/pages/assignment4',
                         template_folder='templates')


# Routes
@assignment_4.route('/assignment4')
def redirect_homepage():
    return render_template('assignment4.html')


# ------------------------------------------------- #
# ------------- DATABASE CONNECTION - A1 ---------- #
# ------------------------------------------------- #


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='tyAydslyssas6',
                                         database='myflaskappdb')
    cursor = connection.cursor(named_tuple=True)

    try:
        cursor.execute(query)
    except Exception as e:
        print(e)

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value


# ------------------------------------------------- #
# -------------------- INSERT --------------------- #
# ------------------------------------------------- #
@assignment_4.route('/insert_user', methods=['POST'])
def insert_user():
    user_name = request.form['user-name']
    user_email = request.form['user-email']
    user_password = request.form['user-password']

    # select all user:
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')

    message_for_user = 'User create successfully!'
    for user in users_list:
        if user.email == user_email:
            message_for_user = 'This email is already used!'

    if message_for_user != 'This email is already used!':
        query = "INSERT INTO users(name, email, password) VALUES ('%s', '%s', '%s')" % (user_name, user_email
                                                                                        , user_password)
        interact_db(query=query, query_type='commit')

    return render_template('assignment4.html', message_for_insert=message_for_user)


# ------------------------------------------------- #
# -------------------- DELETE --------------------- #
# ------------------------------------------------- #

@assignment_4.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_email = request.form['user-email-delete']

    ## select all user:
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')

    message_for_user = 'Email not found!'

    for user in users_list:
        if user.email == user_email:
            message_for_user = 'User delete!'

    query = "DELETE FROM users WHERE email='%s';" % user_email
    interact_db(query, query_type='commit')
    return render_template('assignment4.html', message_for_delete=message_for_user)

# ------------------------------------------------- #
# -------------------- UPDATE --------------------- #
# ------------------------------------------------- #


@assignment_4.route('/update_user', methods=['POST'])
def update_user_func():
    user_password = request.form['user-password-update']
    user_name = request.form['user-name-update']
    user_email = request.form['user-email']
    if user_name != "" and user_password != "":
        query = "UPDATE users SET name='%s', password='%s' WHERE email='%s'" % (user_name, user_password, user_email)
        message_for_user1 = "User name and password update!"

    elif user_name != "" and user_password == "":
        query = "UPDATE users SET name='%s' WHERE email='%s'" % (user_name, user_email)
        message_for_user1 = "User name update!"

    elif user_name == "" and user_password != "":
        query = "UPDATE users SET password='%s' WHERE email='%s'" % (user_password, user_email)
        message_for_user1 = "Password update!"

    else:
        message_for_user1 = "No values to update!"
        return render_template('assignment4.html', message_for_user=message_for_user1)

    interact_db(query, query_type='commit')
    return render_template('assignment4.html', message_for_user=message_for_user1)

# ------------------------------------------------- #
# ------------------- SELECT ---------------------- #
# ------------------------------------------------- #


@assignment_4.route('/select-users')
def select_users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    print(users_list)
    return render_template('assignment4.html', users=users_list)

# ------------------------------------------------- #
# -------------- SELECT-JSON - B ------------------ #
# ------------------------------------------------- #


@assignment_4.route('/assignment4/users')
def select_users_json():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')

    users_object = {}
    for row in users_list:
        print(row)
        users_object[row.id] = {
            'id': row.id,
            'name': row.name,
            'email': row.email,
        }

    print(users_object)
    return jsonify(users_object)


# ------------------------------------------------- #
# ------------------ outer_source - B ------------- #
# ------------------------------------------------- #

@assignment_4.route('/assignment4/outer_source')
def index():
    session.clear()
    return render_template('outer_source.html')


@assignment_4.route('/outer_source', methods=['POST'])
def display_outer_json():
    session.clear()
    id = request.form['singleuser_id']
    uri = "https://reqres.in/api/users/%s" % (str(id),)
    print(uri)
    try:
        u_response = requests.get(uri)
    except requests.ConnectionError:
        return "Connection Error"
    jresponse = u_response.text
    data = json.loads(jresponse)
    print(data)
    session['user_data'] = json.dumps(data)
    return render_template('outer_source.html', register_text=session.get(session['user_data']))

# ------------------------------------------------- #
# ------------------ restapi_users - C ------------ #
# ------------------------------------------------- #


@assignment_4.route('/assignment4/restapi_users')
def restapi_users_without_id():
    return jsonify({
        "id": 0,
        "name": "Default",
        "email": "Default@gmail.com",
    })


@assignment_4.route('/assignment4/restapi_users/<USER_ID>')
def restapi_users(USER_ID):
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    user_exist = False
    users_object = {}

    if not USER_ID.isnumeric():
        return jsonify({
            "message": "Wrong user number!"
        })

    for row in users_list:
        if row.id == int(USER_ID):
            user_exist = True
            users_object[row.id] = {
                'id': row.id,
                'name': row.name,
                'email': row.email,
            }

    if not user_exist:
        return jsonify({
            "message": "This user is not exist!"
        })

    return jsonify(users_object)



