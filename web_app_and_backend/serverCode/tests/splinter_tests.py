from splinter import Browser
import time
import os

'''
Test 1: Upload a photo successfully for classification. 
Test 2: Upload nothing and try to classify image. 
Test 3: Upload something which isn't an image and try to classify it. 
Test 4: Send an email after classification
'''

executable_path = {'executable_path':'static/testing/chromedriver.exe'}
#executable_path = {'executable_path':'static/testing/geckodriver.exe'}

browser = Browser('chrome', **executable_path) ##chrome
#browser = Browser(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.2.8 (KHTML, like Gecko) Version/11.0 Mobile/15B57 Safari/604.1", **executable_path) ## iPhone
#browser = Browser('firefox', **executable_path) ##firefox

#Test Case 1
print("=========================================================")
print("Running Test Case 1: Upload photo for Classification")
browser.visit('http://54.191.193.7:5000/')
print("Visiting browser...")
time.sleep(2)
element = browser.driver.find_element_by_id("imageFile")
pathToImage = os.path.abspath("static/testing/Capture5.JPG")
element.send_keys(pathToImage)
print("Image chosen...")
time.sleep(2)
browser.click_link_by_id('submit')
print("Image submitted for classification...")
time.sleep(2)
assert browser.is_text_present('Image Uploaded') == True
print("=========================================================")

#Test Case 2
print("Running Test Case 2: Upload nothing and try to submit for classification")
browser.visit('http://54.191.193.7:5000/')
print("Visiting browser...")
time.sleep(2)
browser.click_link_by_id('submit')
print("Submit button pressed...")
time.sleep(2)
assert browser.is_text_present('Please choose an image!') == True
print("=========================================================")

#Test Case 3
print("Running Test Case 3: Try to classify non-image file")
browser.visit('http://54.191.193.7:5000/')
print("Visiting browser...")
time.sleep(2)
element = browser.driver.find_element_by_id("imageFile")
pathToFile = os.path.abspath("static/testing/pointers.doc")
element.send_keys(pathToFile)
print("file chosen...")
time.sleep(2)
browser.click_link_by_id('submit')
print("File submitted for classification...")
time.sleep(2)
assert browser.is_text_present('Please choose an image!') == True
print("=========================================================")

#Test Case 4
print("Running Test Case 4: Classify image and send email")
browser.visit('http://54.191.193.7:5000/')
print("Visiting browser...")
time.sleep(2)
element = browser.driver.find_element_by_id("imageFile")
pathToImage = os.path.abspath("static/testing/Capture5.JPG")
element.send_keys(pathToImage)
print("Image chosen...")
time.sleep(2)
browser.click_link_by_id('submit')
print("Image submitted for classification...")
time.sleep(2)
browser.find_by_id('email').fill('cathal.hughes56@mail.dcu.ie')
print("Email field filled...")
browser.click_link_by_id('email_submit')
print("Email submit button pressed...")
time.sleep(5)
assert browser.is_text_present('Your email has been sent!') == True
print("=========================================================")

#Test Case 5
print("Running Test Case 5: Classify image and enter invalid string in email box and click submit")
browser.visit('http://54.191.193.7:5000/')
print("Visiting browser...")
time.sleep(2)
element = browser.driver.find_element_by_id("imageFile")
pathToImage = os.path.abspath("static/testing/Capture5.JPG")
element.send_keys(pathToImage)
print("Image chosen...")
time.sleep(2)
browser.click_link_by_id('submit')
print("Image submitted for classification...")
time.sleep(2)
browser.find_by_id('email').fill('cathal')
print("Email field filled with invalid input...")
browser.click_link_by_id('email_submit')
print("Email submit button pressed...")
time.sleep(5)
assert browser.is_text_present('Your email has been sent!') == False
assert browser.url != "http://54.191.193.7:5000/email"
print("=========================================================")

#Test Case 6
print("Running Test Case 6: Classify image and click on link for more information")
browser.visit('http://54.191.193.7:5000/')
print("Visiting browser...")
time.sleep(2)
element = browser.driver.find_element_by_id("imageFile")
pathToImage = os.path.abspath("static/testing/Capture5.JPG")
element.send_keys(pathToImage)
print("Image chosen...")
time.sleep(2)
browser.click_link_by_id('submit')
assert browser.is_text_present('Image Uploaded') == True
browser.click_link_by_href("https://www.hse.ie/eng/health/az/h/hives%20-%20acute/causes-of-urticaria.html")
print("Link clicked...")
time.sleep(2)
browser.windows.current = browser.windows[1]
assert browser.url == "https://www.hse.ie/eng/health/az/h/hives%20-%20acute/causes-of-urticaria.html"
browser.windows[1].close()
browser.windows.current = browser.windows[0]
print("=========================================================")

#Test Case 7
print("Running Test Case 7: Classify image and click on both links for more information")
browser.visit('http://54.191.193.7:5000/')
print("Visiting browser...")
time.sleep(2)
element = browser.driver.find_element_by_id("imageFile")
pathToImage = os.path.abspath("static/testing/Capture5.JPG")
element.send_keys(pathToImage)
print("Image chosen...")
time.sleep(2)
browser.click_link_by_id('submit')
assert browser.is_text_present('Image Uploaded') == True
browser.click_link_by_href("https://www.hse.ie/eng/health/az/h/hives%20-%20acute/causes-of-urticaria.html")
print("Link clicked...")
time.sleep(2)
browser.windows.current = browser.windows[1]
assert browser.url == "https://www.hse.ie/eng/health/az/h/hives%20-%20acute/causes-of-urticaria.html"
print("First page visit, close tab...")
browser.windows[1].close()
browser.windows.current = browser.windows[0]
assert browser.url == "http://54.191.193.7:5000/predictClient"
print("Visit second link...")
browser.click_link_by_href("https://www.hse.ie/eng/health/az/c/contact-dermatitis/treating-eczema-contact-dermatitis-.html")
time.sleep(2)
browser.windows.current = browser.windows[1]
assert browser.url == "https://www.hse.ie/eng/health/az/c/contact-dermatitis/treating-eczema-contact-dermatitis-.html"
print("=========================================================")

print("Tests Finished, All Passed 7/7, 12/12 assertions, Clean up")
print("Deleting test photos")
browser.visit("http://54.191.193.7:5000/")
print("=========================================================")

browser.quit()
