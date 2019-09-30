import pyrebase
from firebase.firebase import FirebaseApplication
import bcrypt

import json
from flask import Flask, request, jsonify, render_template

from subprocess import call


app = Flask(__name__,template_folder='template')


config = {
  "apiKey": "AIzaSyA7UUJVAOEjWSaP6uezJRx-OJPLX-n8-kU",
"authDomain": "boringhtml-a6697.firebaseapp.com",
"databaseURL": "https://boringhtml-a6697.firebaseio.com",
"projectId": "boringhtml-a6697",
"storageBucket": "boringhtml-a6697.appspot.com",
"serviceAccount": "firebase.json"
}

firebase = pyrebase.initialize_app(config)
firebase = FirebaseApplication('https://boringhtml-a6697.firebaseio.com', None)


@app.route("/")
def renderIndexPage():
   return render_template("index.html")

@app.route("/renderLoginAccessPage", methods = ['GET', 'POST'])
def renderLoginAccessPage():
    if request.method == 'POST':
        data = request.form.to_dict()
        print("JSON data: ", data)
        print(type(data.get("username")))
        result = firebase.get('/'+str(data.get("username")), None)
        if result!= None:
            hashed = result.get("password").encode('utf-8')
            password = data.get("password").encode('utf-8')
            print('hashed',hashed)
            print('password',password)
            # print('result.get("pswd")',type(result.get("password")))
            # print('str(data.get("password"))',type(data.get("password")))
            if bcrypt.checkpw(password, hashed):
                print("successful")
                # return render_template("dashboard.html")
                call(["php","dashboard.php"])
            else:
                print("unsuccessful")
                return render_template("login.html" , status = "fail" )
        else:
            print("unsuccessful")
            return render_template("login.html" , status = "fail" )

    return render_template("login.html")


@app.route("/registerUser", methods = ['POST','GET'])
def registerUser():
    error = None
    if request.method == 'POST':
        data = request.form.to_dict()
        print("data = " ,data)
        username = str(data.get("userName"))
        firstName = str(data.get("firstName"))
        lastName = str(data.get("lastName"))
        password = str(data.get("password"))
        password = password.encode('ASCII')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        data = {}
        data["firstName"] = firstName
        data["lastName"] = lastName
        data["password"] = hashed
        
        firebase = pyrebase.initialize_app(config)
        firebase = FirebaseApplication('https://boringhtml-a6697.firebaseio.com', None)
        result = firebase.get('/'+username, None)
        print ("result = ",result)
        if result== None:
            print("adding new user")
            firebase = pyrebase.initialize_app(config)
            db = firebase.database()
            db.child(username).set(data)
            print("added")
            return render_template("dashboard.html")
        else:
            error = "User already exists"
            print(error)
            return render_template("register.html")
    return render_template("register.html")



# dashboard rendering 
@app.route("/renderDashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == '__main__':
   flag_login = 0
   auth = False
   app.run(debug = True)
