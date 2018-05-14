from flask import Flask, request, Response, render_template, flash, redirect, url_for
import flask_bootstrap
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import base64
import os
import time
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from model.loadModel import *
from flask_mail import Message, Mail
import json

app = Flask(__name__)
app.secret_key = "MY_SECRET_KEY"
VALID_EXTENSIONS = ["png", "jpg", "jpeg"]
app.config.from_object('config')
mail = Mail(app)

global pmodel, pgraph, hmodel, hgraph, rmodel, rgraph, emodel, egraph, smodel, sgraph
pmodel, pgraph = initPsoriasis()
hmodel, hgraph = initHives()
rmodel, rgraph = initRingworm()
emodel, egraph = initEczema()
smodel, sgraph = initShingles()

psLink = "https://www.hse.ie/eng/health/az/p/psoriasis/symptoms-of-psoriasis.html"
hiLink = "https://www.hse.ie/eng/health/az/h/hives%20-%20acute/causes-of-urticaria.html"
rwLink = "https://www.hse.ie/eng/health/az/r/ringworm/treating-ringworm.html"
shLink = "https://www.hse.ie/eng/health/az/s/shingles/"
ecLink = "https://www.hse.ie/eng/health/az/c/contact-dermatitis/treating-eczema-contact-dermatitis-.html"
links = [psLink, hiLink, rwLink, shLink, ecLink]

androidChart = ""
androidImage = ""
resultsList = []

@app.route('/', methods=['GET', 'POST'])
def web_app():
    global androidChart
    androidChart = ""
    functToDeleteItems("static/images")
    if request.method == 'POST':
        flash('Your email has been sent!', 'success')
    return render_template('upload_page.html')


def functToDeleteItems(fullPathToDir):
    for itemsInDir in os.listdir(fullPathToDir):
        if os.path.isdir(os.path.join(fullPathToDir, itemsInDir)):
            functToDeleteItems(os.path.isdir(os.path.join(fullPathToDir, itemsInDir)))
        else:
            os.remove(os.path.join(fullPathToDir, itemsInDir))

def decodeImageFromAndroid(imgData, fname):

    f = open(fname, "wb")
    f.write(base64.b64decode(imgData))

def decodeImageFromClient(imgData, fname):
    f = open(fname, "wb")
    f.write(base64.b64decode(imgData))

def processImage(fname):
    img = load_img(fname, target_size=(224, 224))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, axis=0)
    return img

def getBarchartResult(results, bname):
    objects = ["Psoriasis", "Hives", "Ringworm", "Eczema", "Shingles"]
    y = np.arange(len(objects))
    f = list(zip(results, objects))
    f = sorted(f)
    d = list(zip(*f))
    plt.barh(y, list(d[0]), align="center", alpha=0.5)
    plt.yticks(y, d[1])
    plt.xlim(0, 100)
    plt.xlabel("Percentage Likelihood")
    plt.title = ("Results")
    plt.savefig(bname, transparent=True)
    plt.clf()

@app.route('/appChart', methods=['GET','POST'])
def appChart():
    print(androidChart)
    if not androidChart:
        return redirect(url_for('web_app'))
    return render_template('androidChart.html', androidChart=androidChart, androidImage=androidImage, results=resultsList)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    global androidChart, androidImage, resultsList
    #response = ""
    print("here for testing")
    functToDeleteItems("static/images")
    print("Data Uploading")
    print(request.headers)
    imgData = request.get_data(as_text=True)
    d = json.loads(imgData)
    imgData = d['image']
    print(imgData[:20])
    androidImage = "static/images/" + str(time.time()) + "output.png"
    androidChart = androidImage + "android.png"
    decodeImageFromAndroid(imgData, androidImage)
    #decodeImageFromClient(imgData, fname)
    img = processImage(androidImage)
    resultsList, results = getPredictions(img)
    resultsList = sorted(resultsList, reverse=True)
    getBarchartResult(results, androidChart)
    response = getResponseStringForAndroid(resultsList)
    #functToDeleteItems("static/images")
    print(response)
    return response

def getResponseStringForAndroid(resultsList):
    responseStr = ""
    for result in resultsList:
        responseStr += result[1] + "-" + str(result[0]) + "%\n"
    return responseStr


def getPredictions(img):
    resList = []
    results = []
    global links
    with pgraph.as_default():
        result = pmodel.predict(img)[0][0]
        percentage = round((1 - result) * 100, 3)
        results.append(percentage)
        print(result)
        result = round(result)
        #if result == 0:
        resList.append((percentage, "Psoriasis", links[0]))
        #else:
        #resultsList.append("Not Psoriasis")
    with hgraph.as_default():
        result = hmodel.predict(img)[0][0]
        print(result)
        percentage = round((1 - result) * 100, 3)
        results.append(percentage)

        result = round(result)
        #if result == 0:
        resList.append((percentage, "Hives", links[1]))
        #else:
        #resultsList.append("Not Hives")
    with rgraph.as_default():
        result = rmodel.predict(img)[0][0]
        print(result)
        percentage = round((result) * 100, 3)
        results.append(percentage)
        result = round(result)
        #if result == 1:
        resList.append((percentage, "Ringworm", links[2]))
        #else:
        #resultsList.append("Not Ring Worm")
    with egraph.as_default():
        result = emodel.predict(img)[0][0]
        percentage = round((1 - result) * 100, 3)
        results.append(percentage)
        print(result)
        result = round(result)
        resList.append((percentage, "Eczema", links[4]))
    with sgraph.as_default():
        result = smodel.predict(img)[0][0]
        percentage = round((result) * 100, 3)
        results.append(percentage)
        print(result)
        result = round(result)
        resList.append((percentage, "Shingles", links[3]))
    return resList, results

def allowed_file(filename):
    return  "." in filename and filename.split(".")[1].lower() in VALID_EXTENSIONS

@app.route('/predictClient', methods=['GET', 'POST'])
def predictClient():
    global resultsList, androidChart
    androidChart = ""
    if request.method == "GET":
        return redirect(url_for('web_app'))
    response = ""

    print("Data Uploading")
    print(request.headers)

    if 'image' not in request.files:
        flash('Please choose an image!', 'warning')
        return render_template('upload_page.html')
    imgData = request.files['image']

    if not imgData or not allowed_file(imgData.filename):
        flash("Please choose an image!", 'warning')
        return render_template("upload_page.html")

    fname = "static/images/" + str(time.time()) + "output.png"
    bname = fname + "foo.png"
    imgData.save(fname)
    print("saved")
    #print(imgData.getvalue())
    img = processImage(fname)
    print("done")
    resultsList, results = getPredictions(img)
    resultsList = sorted(resultsList, reverse=True)
    getBarchartResult(results, bname)

    flash('Image Uploaded', 'success')
    return render_template('upload_page.html', results=resultsList, fname=fname, bname=bname)

@app.route('/email', methods=['GET', 'POST'])
def email():
    if request.method == 'GET':
        return redirect(url_for('web_app'))
    recipient = request.form.get("email")
    image = request.form.get("image")
    barchart = request.form.get("barchart")
    print(resultsList)
    print(type(resultsList))
    msg = Message('Skin Classification Results', sender="skinconditionclassifier@gmail.com", recipients=[recipient])
    msg.html = render_template("email.html", results=resultsList, image=image, barchart=barchart)
    with app.open_resource(image) as fp:
        msg.attach("image.png", "image/png", fp.read())
    with app.open_resource(barchart) as fp:
        msg.attach("barchart.png", "image/png", fp.read())
    mail.send(msg)
    if androidChart:
        flash('Your email has been sent!', 'success')
        return render_template("androidChart.html", androidChart=androidChart, androidImage=androidImage, results=resultsList)
    flash('Your email has been sent!', 'success')
    return render_template('upload_page.html')

app.run(host='127.0.0.0', threaded=True)