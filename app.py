import pyrebase
from firebase.firebase import FirebaseApplication
import bcrypt

import json
from flask import Flask, request, jsonify, render_template

from subprocess import call


app = Flask(__name__,template_folder='template')

login_status = 0

firebaseConfig = {
  'apiKey': "AIzaSyD8N-HKhsTOmo-4IgxbTXmlVZb1ZmWpVg0",
  'authDomain': "boring-html.firebaseapp.com",
  'databaseURL': "https://boring-html.firebaseio.com/",
  'projectId': "boring-html",
  'storageBucket': "boring-html.appspot.com",
  'messagingSenderId': "772540172270",
  'appId': "1:772540172270:web:aa588f06a3e9779adef0ff",
  'measurementId': "G-1T98ECTMSF"
};

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()



@app.route("/")
def renderIndexPage():
   return render_template("index.html")

@app.route("/renderLoginAccessPage", methods = ['GET', 'POST'])
def renderLoginAccessPage():
    if request.method == 'POST':
        data = request.form.to_dict()
        print("JSON data: ", data)
        email = str(data.get("userName"))
        password = str(data.get("password"))
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            print("added")
            render_template('dashboard.html',result = data)
        except:
            print("uncessful")
            render_template("login.html",us = "fail")

    # if request.method == 'POST':
    #     data = request.form.to_dict()
    #     print("JSON data: ", data)
    #     print(type(data.get("username")))
    #     result = firebase.get('/'+str(data.get("username")), None)
    #     if result!= None:
    #         hashed = result.get("password").encode('utf-8')
    #         password = data.get("password").encode('utf-8')
    #         print('hashed',hashed)
    #         print('password',password)
    #         print(result)
    #         # print('result.get("pswd")',type(result.get("password")))
    #         # print('str(data.get("password"))',type(data.get("password")))
    #         if bcrypt.checkpw(password, hashed):
    #             print("successful")
    #             # return render_template("dashboard.html")
    #             return render_template("dashboard.html",result = result)
    #         else:
    #             print("unsuccessful")
    #             return render_template("login.html" , status = "fail" )
        # else:
        #     print("unsuccessful")
        #     return render_template("login.html" , status = "fail" )

    return render_template("login.html")


@app.route("/registerUser", methods = ['POST','GET'])
def registerUser():
    error = None
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        # username = str(data.get("userName"))
        email = str(data.get("userName"))
        firstName = str(data.get("firstName"))
        lastName = str(data.get("lastName"))
        password = str(data.get("password"))
        # password = password.encode('ASCII')
        # hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        data = {}
        data["firstName"] = firstName
        data["lastName"] = lastName
        data["password"] = password
        data["project"] = 0
        # firebase = FirebaseApplication('https://boring-html.firebaseio.com/', None)
        firebase = pyrebase.initialize_app(firebaseConfig)

        auth = firebase.auth()
        try:
            auth.create_user_with_email_and_password(email,password)
        except Exception as e:
            return render_template("register.html",us = e)
        db = firebase.database()
        db.child(email).set(data)
        print("added")
        return render_template('dashboard.html',result = data)

        #result = firebase.get('/'+username, None)
    
        # if result== None:
        #     firebase = pyrebase.initialize_app(config)
        #     db = firebase.database()
        #     db.child(username).set(data)
        #     print("added")
        #     render_template('dashboard.html',result = result)
        # else:
        #     error = "User already exists"
        #     print(error)
        #     return render_template("register.html")
    else:
        return render_template("register.html")


# logout
@app.route("/login")
def dashboard():
    login_status = 0;
    return render_template('index.html')

if __name__ == '__main__':
   flag_login = 0
   auth = False
   app.run(debug = True)
