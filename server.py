from flask import Flask, render_template, redirect, request, session
from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key="my#mySQL$querries#arekicking#my&tail"

@app.route('/users')
def index():
    mySQL = connectToMySQL('users')
    users = mySQL.query_db('SELECT * FROM friends;')
    print('*'*90)
    print('Printing users')
    print(users)
    return render_template('index.html', users = users)

@app.route('/users/new')
def add_user():
    print('*'*90)
    print('Rendering add page')
    return render_template('add.html')

#creating a user
@app.route('/users/create', methods=['POST'])
def create_user():
    mysql = connectToMySQL('users')
    query = ('INSERT INTO friends(first_name, last_name, email) VALUES(%(f)s, %(l)s, %(e)s);')
    data = {
        'f': request.form['first_name'],
        'l': request.form['last_name'],
        'e': request.form['email']
    }
    db = connectToMySQL('users')
    db.query_db(query, data)
    #get id from the database to pass variable for unique user
    mysql = connectToMySQL('users')
    query = ('SELECT id FROM friends where email =%(e)s;')
    data = {
        'e': request.form['email']
    }
    get_id = mysql.query_db(query, data)
    print(get_id)
    id = get_id[0]['id']
    #removing SQL injection possibilites
    return redirect(f'/users/{id}')
    #return redirect('/users/<id>')

#Show User
@app.route('/users/<id>')
def show_user(id):
    mysql = connectToMySQL('users')
    #removing {id} from Where clause
    #new_user = mysql.query_db('SELECT id, first_name, last_name, email, created_at, updated_at FROM friends WHERE id = %(id)s;')
    #adding data here
    query = 'SELECT id, first_name, last_name, email, created_at, updated_at FROM friends WHERE id = %(id)s;'
    data = {'id': id}
    new_user = mysql.query_db(query, data)
    print('*'*90)
    print('Rendering show page')
    print(new_user)
    return render_template('show.html',
    user = new_user
    )

#Edit User
@app.route('/users/<id>/edit')
def edit_user(id):
    mysql = connectToMySQL('users')
    #Removing SQL Injection possibilties
    #edit_user = mysql.query_db(f'SELECT id, first_name, last_name, email FROM friends WHERE id = {id}')
    query = 'SELECT id, first_name, last_name, email FROM friends WHERE id = %(id)s;'
    data = {'id': id}
    edit_user = mysql.query_db(query, data)
    print('*'*90)
    print('Rendering edit page')
    print(edit_user)
    e_id = edit_user[0]['id']
    e_fname = edit_user[0]['first_name']
    e_lname = edit_user[0]['last_name']
    e_email = edit_user[0]['email']
    return render_template('edit.html',
    id = e_id,
    fname = e_fname,
    lname = e_lname,
    email = e_email
    )

@app.route('/users/<id>/update', methods=['POST'])
def user_update(id):
    mysql = connectToMySQL('users')
    #query = (f'UPDATE friends SET first_name = %(f)s, last_name = %(l)s, email = %(e)s WHERE id = {id};')
    query = 'UPDATE friends SET first_name = %(f)s, last_name = %(l)s, email = %(e)s WHERE id = %(id)s;'
    data = {
        'f': request.form['first_name'],
        'l': request.form['last_name'],
        'e': request.form['email'],
        'id': id
    }
    db = connectToMySQL('users')
    db.query_db(query, data)
    print('Query sucessfully updated')
    return redirect(f'users/{id}')

@app.route('/users/<id>/destroy')
def delete_user(id):
    mysql = connectToMySQL('users')
    #query = mysql.query_db(f'DELETE FROM friends WHERE id = {id}')
    query = 'DELETE FROM friends WHERE id = %(id)s;'
    data = {'id': id}
    mysql.query_db(query, data)
    print('User record deleted sucessfully')
    return redirect('/users')

if __name__=="__main__":
    app.run(debug=True)
#converting the date
#SELECT CONVERT(varchar, getdate(), 7)
#converting date and time
#select convert(varchar, getdate(), 0)
