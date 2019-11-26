import pyrebase
import scipy.misc
from firebase.firebase import FirebaseApplication
import json
from flask import Flask, request, jsonify, render_template,session, escape, request, redirect, url_for
from subprocess import call
from os import urandom
import numpy as np
import urllib.request
import cv2
import os
import tensorflow as tf
import sys
import time
from subprocess import call
from os import urandom
import collections




app = Flask(__name__,template_folder='template')
app.debug = True
app.secret_key = urandom(24)

login_status = 0
code = ""





#--------------------MachineLearning---------------------------------------- 
# This is needed since the notebook is stored in the object_detection folder.

sys.path.append("models")
sys.path.append("models/research")
sys.path.append("models/research/slim")
sys.path.append("models/research/object_detection")
# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# Name of the directory containing the object detection module we're using
MODEL_NAME = 'models/research/object_detection/trained_model'
# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,'labelmap.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 6

# Load the label map.
# Label maps map indices to category names, so that when our convolution
# network predicts `5`, we know that this corresponds to `king`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the model

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)
# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# --------------------------End MachineLearning-------------------------------








#this is enough
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
    if 'userId' in session:
        return render_template('dashboard.html',result = data1)
    return render_template("index.html")

@app.route("/dashboard")
def renderDashboard():
    if 'userId' in session:
        db = firebase.database()
        values = db.child(session["userId"]).get().val()
        data1["firstName"] = values.get("firstName")
        data1["lastName"] = values.get("lastName")
        data1["password"] = "password"
        data1["email"] = values.get("email")
        data1["project"] = convert(values.get("project"))
        return render_template('dashboard.html',result = data1)
    return render_template("index.html")


@app.route("/renderLoginAccessPage", methods = ['GET', 'POST'])
def renderLoginAccessPage():
    if request.method == 'POST':
        firebase = pyrebase.initialize_app(firebaseConfig)
        auth = firebase.auth()
        data = request.form.to_dict()
        print("JSON data: ", data)
        print(str(data.get("email")))
        print(str(data.get("password")))
        email = str(data.get("email"))
        password = str(data.get("password"))
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            print("added",user)
            db = firebase.database()
            values = db.child(user['localId']).get().val()
            data1["firstName"] = values.get("firstName")
            data1["lastName"] = values.get("lastName")
            data1["password"] = "password"
            data1["email"] = values.get("email")
            data1["project"] = convert(values.get("project"))
            session['userId'] = user['localId']

            return redirect(url_for('renderIndexPage'))
        except Exception as e:
            print("error ",e)
            e = json.loads(e.args[1])
            e = (e["error"]["message"])
            # e = json.loads(e.args[1])
            # e = (e["error"]["message"])
            return render_template("login.html",us = e)
    return render_template("login.html")


def convert(data):
    if isinstance(data, str):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data



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

        data1["firstName"] = firstName
        data1["lastName"] = lastName
        data1["password"] = password
        data1["email"] = email
        data1["project"] = {"total":0}

        # projects = {}
        # pjt = {}
        # pjt ["desc"] = "This is the first project's desciption."
        # pjt ["img"] = "a.jpg"
        # pjt ["code"] = "a.text"
        # projects["project1"] = pjt


        # pjt = {}
        # pjt ["desc"] = "This is the second project's desciption."
        # pjt ["img"] = "a.jpg"
        # pjt ["code"] = "a.text"
        # projects["project2"] = pjt
        # data1["project"]["projects"] = projects
    #
	# pjt = {}
	# projects = {}
	# pjt["Name"] = "Project1"
	# pjt["disc"] = "...................."
	# pjt["image"] = "image path"

	# projects['total'] = 0
	# projects['project'] = pjt
    #     data1["project"] = projects
        # firebase = FirebaseApplication('https://boring-html.firebaseio.com/', None)

        firebase = pyrebase.initialize_app(firebaseConfig)

        auth = firebase.auth()
        try:
            user = auth.create_user_with_email_and_password(email,password)
        except Exception as e:
            e = json.loads(e.args[1])
            e = (e["error"]["message"])
            return render_template("register.html",us = e)
        db = firebase.database()
        db.child(user['localId']).set(data1)
        print("added")
        return redirect(url_for('renderIndexPage'))
    else:
        return render_template("register.html")





        

@app.route("/MachineLearning.html" ,methods = ['POST','GET'])
def MachineLearning():
    global code
    url = (request.form['custId'])
    projectName = (request.form['projectName'])
    session["projectName"]=projectName
    resp = urllib.request.urlopen(url)
    input_image = np.asarray(bytearray(resp.read()), dtype="uint8")
    input_image = cv2.imdecode(input_image, cv2.IMREAD_COLOR)
    cv2.imwrite('static/Input.jpg', input_image)
    output_image = input_image
    image_expanded = np.expand_dims(output_image, axis=0)

    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})
    #print([category_index.get(i) for i in classes[0]])
    # Draw the results of the detection (aka 'visulaize the results')

    image,code = vis_util.visualize_boxes_and_labels_on_image_array(
        output_image,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.60)

    # All the results have been drawn on image. Now display the image.
    
    time.sleep(1)
    cv2.imwrite('static/Output.jpg', output_image)
    
    return render_template('MachineLearning.html',display_code = code)

@app.route("/logOut")
def logOut():
    session.pop('userId')
    return redirect(url_for('renderIndexPage'))

@app.route("/edit",methods = ['POST','GET'])
def edit():
    if('userId' in session):
        db = firebase.database()
        project_name = request.form['project_name']
        print(project_name)
        code_of_project = db.child(session['userId']).child("project").child("projects").child(project_name).child("code").get().val()
        print("code",code_of_project)
        return render_template('edit.html',code = code_of_project)
    return render_template('index.html')

@app.route("/addProject")
def renderAddProject():
    if("projectName" in session and 'userId' in session):
        print("name exisist")
        projectName = session["projectName"]
        firebase = pyrebase.initialize_app(firebaseConfig)
        storage = firebase.storage()
        print(code)
        # print(type(data1["firstName"]))
        # print(type(projectName))
        # print(type("/Input.jpg"))
        # print(type("/"))


        inputImagePAth = data1["firstName"]+"/"+projectName+"/Input.jpg"
        oututImagePAth = data1["firstName"]+"/"+projectName+"/Output.jpg"
        storage.child(inputImagePAth).put("static/Input.jpg")
        storage.child(oututImagePAth).put("static/Output.jpg")

        pjt = {}
        pjt ["name"] = projectName
        pjt ["desc"] = projectName+" project's desciption."
        pjt ["imgOut"] = storage.child(oututImagePAth).get_url(None)
        pjt ["imgInp"] = storage.child(inputImagePAth).get_url(None)
        pjt ["code"] = code


        db = firebase.database()
        
        db.child(session['userId']).child("project").child("projects").child(projectName).set(pjt)
    

        print(session['userId'])

        totalProject = db.child(session['userId']).child("project").child("total").get().val()
        print("total",totalProject)
        totalProject = totalProject + 1
        print(totalProject)
        
        db.child(session['userId']).child("project").child("total").set(totalProject)
        return redirect(url_for('renderDashboard'))
    return render_template('index.html')



if __name__ == '__main__':
   flag_login = 0
   auth = False
   app.run(debug = True)
