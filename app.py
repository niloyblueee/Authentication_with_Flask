from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

#mysql configuration
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# Initialize MySQL and Bcrypt
mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8') 
        cur = mysql.connection.cursor()
        cur.execute("insert into users(username,password) values (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()

        return redirect('/login')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])

def login():
    
    if request.method == 'POST': 
        username = request.form['username']
        password_input = request.form['password']

        # Fetch the hashed password from the database
        cur = mysql.connection.cursor() 
        cur.execute("select password from users where username = %s", (username,))
        user = cur.fetchone() # Fetch the user record
        cur.close()
        # Check if the user exists and verify the password
        if user and bcrypt.check_password_hash(user[0], password_input):
            session['username'] = username
            return f"Welcome {username}!"
        
        else:
            return "Invalid username or password"    
    return render_template('/login.html')

if __name__ == '__main__':
    app.run(debug=True)
# To run the app, use the command: python app.py