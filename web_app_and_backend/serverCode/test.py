from app import *
import unittest
import os
from flask_testing import TestCase
import numpy
import base64
import json

class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass

class FlaskTestCase(BaseTestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that homepage was rendered correctly
    def test_homepage_loads(self):
        response = self.client.get('/', content_type='html/text')
        self.assertTrue(b'Skin Condition Classifier' in response.data)

    # Ensure that images folder is empty on start-up of app
    def test_image_folder_empty(self):
        path = 'static/images'
        self.assertEqual(os.listdir(path), [])

    # Ensure correct behaviour on skin classification when passed an image
    def test_skin_classification(self):
        response = self.client.post(
            '/',
            data=dict(imageFile='static/testing/Capture5.JPG'),
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

    def test_predict_client_with_image(self):
        image = open("static/testing/Capture5.JPG", "rb")
        response = self.client.post(
            '/predictClient',
            data={'image' : image},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Psoriasis' in response.data)

    def test_predict_client_with_no_image(self):
        response = self.client.post(
            '/predictClient',
            data="Hi",
            follow_redirects=True
        )
        self.assertEqual(b'Please choose an image!' in response.data, True)

    def test_predict_client_with_incorrect_filetype(self):
        file = open("static/testing/pointers1.txt", "rb")
        response = self.client.post(
           '/predictClient',
            data={'image': file}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Please choose an image!' in response.data)

    def test_predict_client_get_request(self):
        response = self.client.get("/predictClient", content_type="html/text")
        self.assertEqual(b'Psoriasis' not in response.data, True)

    # Ensure correct behaviour when using email route
    def test_email(self):
        response = self.client.post(
            '/email',
            data=dict(email='cathal.hughes56@mail.dcu.ie', image='static/testing/Capture5.JPG', barchart='static/testing/Capture5.JPG'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    '''Test /predict'''
    def test_predict_with_image(self):
        f = open("static/testing/Capture5.JPG", "rb")
        string = f.read()
        data = base64.encodestring(string)
        data = data.decode("ascii")
        d = {}
        d["image"] = data
        d = json.dumps(d)
        d = str.encode(d)
        response = self.client.post(
            '/predict',
            data=d
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data != "", True)


    # Ensure correct behaviour on skin classification when passed no image
    def test_skin_classification_no_image(self):
        response = self.client.post(
            '/',
            data=dict(imageFile=''),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        # self.assertMessageFlashed(message='Please choose an image!', category='message')

    # Ensure correct behaviour on skin classification when passed a file that isn't an image
    def test_skin_condition_file(self):
        response = self.client.post(
            '/',
            data=dict(imageFile='static/testing/pointers.doc'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

   # Unit testing backend functions for generating results etc.

    #Ensure processImage works and returns correct type
    def test_processImage_method(self):
        img = processImage("static/testing/Capture5.JPG")
        self.assertEqual(type(img), numpy.ndarray)

    #Ensure getPredictions method woks coreectly
    def test_getPredictions_method(self):
        conditions = ["Eczema", "Psoriasis", "Hives", "Shingles", "Ringworm"]
        img = processImage("static/testing/Capture5.JPG")

    #Ensure getPredictions method woks correctly
    def test_getPredictions_method(self):
        conditions = ["Eczema", "Psoriasis", "Hives", "Shingles", "Ringworm"]
        img = processImage("static/testing/Capture5.JPG")
        resultsData, results = getPredictions(img)
        self.assertEqual(len(results), 5)
        self.assertEqual(len(resultsData), 5)
        for res in resultsData:
            self.assertEqual(res[1] in conditions, True)

    #Ensure response generator for android works
    def test_getResponseStringForAndroid_method(self):
        results = [(51.333, "Eczema"),(55.555, "Shingles"),(66.666, "Ringworm"),(99.999, "Psoriasis"),(100.00, "Hives")]
        responseStr = getResponseStringForAndroid(results)
        self.assertNotEqual(responseStr, "")

    #Ensure barchart is being saved
    def test_getBarchartResults_Method(self):
        res = [11,9,44,77,33]
        getBarchartResult(res, "static/testing/barcharts/test.png")
        self.assertEqual(os.path.isfile("static/testing/barcharts/test.png"), True)

    def test_decodeImageFromClient_method(self):
        f = open("static/testing/Capture5.JPG", "rb")
        string = f.read()
        data = base64.encodestring(string)
        decodeImageFromClient(data, "static/testing/barcharts/test1.png")
        self.assertEqual(os.path.isfile("static/testing/barcharts/test1.png"), True)

    #Ensure evrything in folder is deleted
    def test_funcToDeleteItems_method(self):
        f = open("static/testing/barcharts/test.txt", "w+")
        f.close()
        functToDeleteItems("static/testing/barcharts")
        self.assertEqual(os.listdir("static/testing/barcharts"), [])


    #Test Psoriasis model loads and works correctly
    def test_initPsoriasis(self):
        img = processImage("static/testing/Capture5.JPG")
        with pgraph.as_default():
            result = pmodel.predict(img)

        self.assertEqual(type(result[0][0]), numpy.float32)

    # Test Ringworm model loads and works correctly
    def test_initRingworm(self):
        img = processImage("static/testing/Capture5.JPG")
        with rgraph.as_default():
            result = rmodel.predict(img)

        self.assertEqual(type(result[0][0]), numpy.float32)

    # Test Hives model loads and works correctly
    def test_initHives(self):
        img = processImage("static/testing/Capture5.JPG")
        with hgraph.as_default():
            result = hmodel.predict(img)

        self.assertEqual(type(result[0][0]), numpy.float32)

    # Test Shingles model loads and works correctly
    def test_initShingles(self):
        img = processImage("static/testing/Capture5.JPG")
        with sgraph.as_default():
            result = smodel.predict(img)
        self.assertEqual(type(result[0][0]), numpy.float32)

    # Test Eczema model loads and works correctly
    def test_initEczema(self):
        img = processImage("static/testing/Capture5.JPG")
        with egraph.as_default():
            result = emodel.predict(img)
        self.assertEqual(type(result[0][0]), numpy.float32)

if __name__ == '__main__':
    unittest.main()


'''
1. Flask set up correct
2. Check Homepage
3. Ensure image folder is empty at start
4. Ensure correct behaviour when passed an image for classification
5. Ensure correct behaviour when passed nothing for classification
6. Ensure correct behaviour when passed incorrect file type for classification
7. Check barchart upon classification
8. Check email is working
'''