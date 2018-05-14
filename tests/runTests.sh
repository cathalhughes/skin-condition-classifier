cd ../web_app_and_backend/serverCode
python splinter_tests.py
adb shell am instrument -w com.example.cathal.skinconditionclassifier.test/android.support.test.runner.AndroidJUnitRunner
#python test.py


