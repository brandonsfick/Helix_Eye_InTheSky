import os
import os, time
import pandas as pd
import numpy as np

import sqlalchemy
from flask_pymongo import PyMongo
from flask import send_file
from flask import Flask, render_template
import dropbox
import glob




app = Flask(__name__)

#################################################
# Database Setup
#################################################

# mongo = PyMongo(app, uri="mongodb://brandonsfick:deathstar1@ds141623.mlab.com:41623/helix_eye")

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(engine, reflect=True)


global path_to_watch

path_to_watch = r"/Users/BFick/Dropbox/Apps/Camera_Images/Apps/Camera_Images/"                            # Watching Desktop
# statinfo_before = os.stat("/Users/BFick/Desktop/Camera_images/test.txt") # MAC
    # statinfo_before = os.stat("C:\Users\B\Desktop\Camera_images") # PC

# statinfo_size_before = statinfo_before.st_size                  # Get size of test.txt
before = dict ([(f, None) for f in os.listdir (path_to_watch)]) # Load 'before' dictionary
    # global statinfo_size_before

# while 1:
#     added = ''
#     time.sleep (5) # 5 sec between polling
#     after = dict ([(f, None) for f in os.listdir (path_to_watch)]) # Load 'after' dictionary
#     added = [f for f in after if not f in before]                  # Was anything added?
#     if added: 
#         print("Added: ", ", ".join (added))

#     before = after
@app.route("/")
def index():
    def newest(path):

        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        recentPath=max(paths, key=os.path.getctime)
        result = recentPath.split('/')[-1]
        return result
    NewCarpath= r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/NewCar_image/" # * means all if need specific format then *.csv
    NewPersonpath= r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/NewPerson_image/" # * means all if need specific format then *.csv
    NonAlertpath =r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/NonAlert_image/"
    
    NewCarImage=newest(NewCarpath)
    NewCarPath = "static/NewCar_image/" + NewCarImage
    print(NewCarPath)

    NewPersonImage=newest(NewPersonpath)
    NewPersonpath = "static/NewPerson_image/" + NewPersonImage
    print(NewPersonpath)

    NonAlertpath=newest(NonAlertpath)
    NonAlertpath = "static/NonAlert_image/" + NonAlertpath
    print(NonAlertpath)
    
    return render_template( "index.html", Most_Recent_Car_Image=NewCarPath, Most_Recent_Person_Image=NewPersonpath, Most_Recent_NonAlert_Image=NonAlertpath )

@app.route("/all_images.html")
def index2():

    return render_template("all_images.html")

@app.route("/about.html")
def index3():

    return render_template("about.html")

if __name__ == "__main__":
    #app.debug = True
    app.run()