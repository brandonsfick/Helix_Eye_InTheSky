import os
import os, time
import pandas as pd
import numpy as np

import sqlalchemy
from flask_pymongo import PyMongo
from flask import send_file
from flask import Flask, render_template


app = Flask(__name__)

#################################################
# Database Setup
#################################################

mongo = PyMongo(app, uri="mongodb://brandonsfick:deathstar1@ds141623.mlab.com:41623/helix_eye")

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(engine, reflect=True)

def insert_image(request):
        with open(request.GET["image_name"], "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            print encoded_string
            mongo.db.insert({"image":encoded_string})
            return HttpResponse("inserted")

@app.route("/")
def index():
    """Return the homepage."""
    added=mongo.db.collection.find()
    path_to_watch = r"C:\Users\B\Desktop\Camera_images"
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    while 1:
        time.sleep (10)
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        print(added)
        # Update the Mongo database using update and upsert=True
    
    insert_image(request)
    # Return template and data
    return 
    # return render_template("index.html", Mars=mars_data) 
    
if __name__ == "__main__":
    #app.debug = True
    app.run()