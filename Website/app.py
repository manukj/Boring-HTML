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


from flask_caching import Cache 
cache = Cache()


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

app = Flask(__name__,template_folder='template')
app.debug = True
app.secret_key = urandom(24)

login_status = 0


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

        data1["firstName"] = firstName
        data1["lastName"] = lastName
        data1["password"] = password
        data1["email"] = email
        data1["project"] = {"total":0}

        projects = {}
        pjt = {}
        pjt ["desc"] = "This is the first project's desciption."
        pjt ["img"] = "a.jpg"
        pjt ["code"] = "a.text"
        projects["project1"] = pjt


        pjt = {}
        pjt ["desc"] = "This is the second project's desciption."
        pjt ["img"] = "a.jpg"
        pjt ["code"] = "a.text"
        projects["project2"] = pjt
        data1["project"]["projects"] = projects
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
            auth.create_user_with_email_and_password(email,password)
        except Exception as e:
            e = json.loads(e.args[1])
            e = (e["error"]["message"])
            return render_template("register.html",us = e)
        db = firebase.database()
        db.child(firstName).set(data1)
        print("added")
        session['username'] = email
        session['data'] = data1
        return redirect(url_for('renderIndexPage'))
    else:
        return render_template("register.html")


@app.route("/MachineLearning.html" ,methods = ['POST','GET'])
def MachineLearning():
    # data = request.form.to_dict()
    # print("JSON data: displaying", data)
    # return render_template("login.html")
    # npimg = numpy.fromfile(request.files['image'], numpy.uint8)
    # # convert numpy array to image
    # img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
    # cv2.imshow('dst_rt', img)
    
    url = (request.form['custId'])
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

    # Draw the results of the detection (aka 'visulaize the results')

    vis_util.visualize_boxes_and_labels_on_image_array(
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
    return render_template('MachineLearning.html')

@app.route("/logOut")
def logOut():
    session.pop('username')
    return redirect(url_for('renderIndexPage'))

@app.route("/edit")
def edit():
    return render_template('edit.html')

@app.route("/addProject")
def renderAddProject():
    time.sleep(3)
    return render_template('dashboard.html',result = data1)



if __name__ == '__main__':
   flag_login = 0
   auth = False
   cache.init_app(app)
   app.run(debug = True)
