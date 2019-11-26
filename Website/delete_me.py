#this is enough
import pyrebase

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


db = firebase.database()

project = db.child("YxMbSi3MCZWsl3XMHRePeyM6Ojv2").child("project")
    


totalProject = project.child("total").get().val()

# code_of_project = db.child("YxMbSi3MCZWsl3XMHRePeyM6Ojv2").child("project").child("total").get().val()
print("code",totalProject)
     