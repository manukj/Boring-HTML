import pyrebase
from firebase.firebase import FirebaseApplication
import json
from flask import Flask, request, jsonify, render_template,session, escape, request, redirect, url_for

from subprocess import call
from os import urandom


app = Flask(__name__,template_folder='template')
app.debug = True
app.secret_key = urandom(24)

login_status = 0

firebaseConfig = {
  'apiKey': "AIzaSyD8N-HKhsTOmo-4IgxbTXmlVZb1ZmWpVg0",
  'authDomain': "boring-html.firebaseapp.com",
  'databaseURL': "https://boring-html.firebaseio.com",
  'projectId': "boring-html",
  'storageBucket': "boring-html.appspot.com",
  'messagingSenderId': "772540172270",
  'appId': "1:772540172270:web:aa588f06a3e9779adef0ff",
  'measurementId': "G-1T98ECTMSF"
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

data1 = {}

@app.route("/")
def renderIndexPage():
    if 'username' in session:
        return render_template('dashboard.html',result = data1)
    return render_template("index.html")

@app.route("/renderLoginAccessPage", methods = ['GET', 'POST'])
def renderLoginAccessPage():
    if request.method == 'POST':
        firebase = pyrebase.initialize_app(firebaseConfig)
        auth = firebase.auth()
        data = request.form.to_dict()
        print("JSON data: ", data)
<<<<<<< HEAD
        firstName = str(data.get("firstName"))
        password = str(data.get("password"))
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            db = firebase.database()
            data = db.child(firstName).get()
            print(data)
            render_template('dashboard.html',result = data)
=======
        print(str(data.get("email")))
        print(str(data.get("password")))
        email = str(data.get("email"))
        password = str(data.get("password"))
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            print("added")
            db = firebase.database()
            all_users = db.child("/").get()
            for user in all_users.each():
                users = user.key()
                values = user.val()
                print (values.get("email").encode('utf-8'))
                if email == values.get("email").encode('utf-8'):
                    print("found")
                    break

            data1["firstName"] = values.get("firstName").encode('utf-8')
            data1["lastName"] = values.get("lastName").encode('utf-8')
            data1["password"] = "password"
            data1["email"] = values.get("email").encode('utf-8')
            data1["project"] =  values.get("project")
            session['username'] = email
            return redirect(url_for('renderIndexPage'))
>>>>>>> 1d5e7af534a600c129ea001aa2b8b311df463eb1
        except Exception as e:
            print("error ",e)
            # e = json.loads(e.args[1])
            # e = (e["error"]["message"])
            return render_template("login.html",us = e)
    return render_template("login.html")


@app.route("/registerUser", methods = ['POST','GET'])
def registerUser():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        # username = str(data.get("userName"))
        email = str(data.get("email"))
        firstName = str(data.get("firstName"))
        lastName = str(data.get("lastName"))
        password = str(data.get("password"))
        # password = password.encode('ASCII')
        # hashed = bcrypt.hashpw(password, bcrypt.gensalt())
<<<<<<< HEAD
        data = {}
        data["firstName"] = firstName
        data["lastName"] = lastName
        data["password"] = password
        data["email"] = email
        data["project"] = {
            "total" : 0,
            "projects": 0 
        }
=======

        data1["firstName"] = firstName
        data1["lastName"] = lastName
        data1["password"] = password
        data1["email"] = email
	
	pjt = {}
	projects = {}
	pjt["Name"] = "Project1"
	pjt["disc"] = "...................."
	pjt["image"] = "image path"	
	
	projects['total'] = 0
	projects['project'] = pjt
        data1["project"] = projects
>>>>>>> 1d5e7af534a600c129ea001aa2b8b311df463eb1
        # firebase = FirebaseApplication('https://boring-html.firebaseio.com/', None)
        firebase = pyrebase.initialize_app(firebaseConfig)
        auth = firebase.auth()
        try:
            auth.create_user_with_email_and_password(email,password)
            db = firebase.database()
            db.child(firstName).set(data)
            print("added")
            return render_template('dashboard.html',result = data)
        except Exception as e:
            e = json.loads(e.args[1])
            e = (e["error"]["message"])
            return render_template("register.html",us = e)
<<<<<<< HEAD

=======
        db = firebase.database()
        db.child(firstName).set(data)
        print("added")
        session['username'] = email
        return redirect(url_for('renderIndexPage'))
>>>>>>> 1d5e7af534a600c129ea001aa2b8b311df463eb1
    else:
        return render_template("register.html")


<<<<<<< HEAD
# logout
@app.route("/edit.html")
def dashboard():
    login_status = 0
    return render_template('edit.html')
=======



@app.route("/logOut")
def logOut():
    session.pop('username')
    return redirect(url_for('renderIndexPage'))

>>>>>>> 1d5e7af534a600c129ea001aa2b8b311df463eb1

if __name__ == '__main__':
   flag_login = 0
   auth = False
   app.run(debug = True)
