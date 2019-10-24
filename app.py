import pyrebase
from firebase.firebase import FirebaseApplication


import json
from flask import Flask, request, jsonify, render_template

from subprocess import call


app = Flask(__name__,template_folder='template')

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



@app.route("/")
def renderIndexPage():
   return render_template("index.html")

@app.route("/renderLoginAccessPage", methods = ['GET', 'POST'])
def renderLoginAccessPage():
    if request.method == 'GET':
        firebase = pyrebase.initialize_app(firebaseConfig)
        auth = firebase.auth()
        data = request.form.to_dict()
        print("JSON data: ", data)
        email = str(data.get("email"))
        password = str(data.get("password"))
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            print("added")
            render_template('dashboard.html',result = data)
        except Exception as e:
            print(e)
            e = json.loads(e.args[1])
            e = (e["error"]["message"])
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
        data = {}
        data["firstName"] = firstName
        data["lastName"] = lastName
        data["password"] = password
        data["email"] = email
        data["project"] = {
            "total" : 0,
            "projects":{}
        }
        # firebase = FirebaseApplication('https://boring-html.firebaseio.com/', None)
        firebase = pyrebase.initialize_app(firebaseConfig)

        auth = firebase.auth()
        try:
            auth.create_user_with_email_and_password(email,password)
        except Exception as e:
            e = json.loads(e.args[1])
            e = (e["error"]["message"])
            return render_template("register.html",us = e)
        db = firebase.database()
        db.child(firstName).set(data)
        print("added")
        return render_template('dashboard.html',result = data)
    else:
        return render_template("register.html")


# logout
@app.route("/login")
def dashboard():
    login_status = 0
    return render_template('index.html')

if __name__ == '__main__':
   flag_login = 0
   auth = False
   app.run(debug = True)
