import os
import os, time
import pandas as pd
import numpy as np

import sqlalchemy
from flask_pymongo import PyMongo
from flask import send_file
from flask import Flask, render_template
import dropbox


app = Flask(__name__)

#################################################
# Database Setup
#################################################

mongo = PyMongo(app, uri="mongodb://brandonsfick:deathstar1@ds141623.mlab.com:41623/helix_eye")

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(engine, reflect=True)



path_to_watch = "/Users/BFick/Desktop/Camera_images/"                            # Watching Desktop
statinfo_before = os.stat("/Users/BFick/Desktop/Camera_images/test.txt") # MAC
    # statinfo_before = os.stat("C:\Users\B\Desktop\Camera_images") # PC

statinfo_size_before = statinfo_before.st_size                  # Get size of test.txt

before = dict ([(f, None) for f in os.listdir (path_to_watch)]) # Load 'before' dictionary
@app.route("/")
def index():

    global before
    global statinfo_size_before
    global path_to_watch
    while 1:
        added = ''
        time.sleep (5) # 5 sec between polling
        after = dict ([(f, None) for f in os.listdir (path_to_watch)]) # Load 'after' dictionary
        added = [f for f in after if not f in before]                  # Was anything added?
        removed = [f for f in before if not f in after]                # Was anything removed?
        if added: 
            print("Added: ", ", ".join (added))
        
            # the source file
            filename = added[0]       # file name
            print(filename)
            filepath = "/Users/BFick/Desktop/Camera_images/" + filename  # path object, defining the file
            print(filepath)
            # target location in Dropbox
            target = "/Apps/Camera_Images/"              # the target folder
            targetfile = target + filename   # the target path and file name

            # Create a dropbox object using an API v2 key
            d = dropbox.Dropbox(access_token)

            # open the file and upload it
            with open(filepath, "rb") as f:
            # upload gives you metadata about the file
            # we want to overwite any previous version of the file
                meta = d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))
        if removed: print("Removed: ", ", ".join (removed))
        before = after
    
if __name__ == "__main__":
    #app.debug = True
    app.run()