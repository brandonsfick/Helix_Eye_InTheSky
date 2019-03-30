import os
import os, time
import pandas as pd
import numpy as np
import pandas

import sqlalchemy
from flask import send_file
from flask import Flask, render_template
# import dropbox
import glob
import datetime
from shutil import copy2
import re
import fnmatch
import random
import shutil
import static
import sys
app = Flask(__name__)

global path_to_watch



@app.route("/")
def index():
    #imports logs and extracts the SSIM and XCP variable
    dfOther = pandas.read_csv('OtherphotoLog.csv')
    dfPerson = pandas.read_csv('PeopleLog.csv')
    dfVehicle = pandas.read_csv('VehicleLog.csv')
    OtherPercent=dfOther.tail(1)
    VehiclePercent =dfVehicle.tail(1)
    PersonPercent= dfPerson.tail(1)

    OtherPercent=OtherPercent.XCP.values[0]
    VehiclePercent=VehiclePercent.SSIM.values[0]
    PersonPercent=PersonPercent.SSIM.values[0]

    #finds file and the path
    def newest(path):

        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        recentPath=max(paths, key=os.path.getctime)
        result = recentPath.split('/')[-1]
        return result
    NewCarpath= r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/NewCar_image/" # UPDATE for your computer
    NewPersonpath= r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/NewPerson_image/" # UPDATE for your computer
    NonAlertpath =r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/NonAlert_image/" # UPDATE for your computer
    
    NewCarImage=newest(NewCarpath)
    NewCarPath = "static/NewCar_image/" + NewCarImage
    print(NewCarPath)

    NewPersonImage=newest(NewPersonpath)
    NewPersonpath = "static/NewPerson_image/" + NewPersonImage
    print(NewPersonpath)

    NonAlertpath=newest(NonAlertpath)
    NonAlertpath = "static/NonAlert_image/" + NonAlertpath
    print(NonAlertpath)
    
    return render_template("index.html", Most_Recent_Car_Image=NewCarPath, Most_Recent_Person_Image=NewPersonpath, Most_Recent_NonAlert_Image=NonAlertpath,OtherPercent=OtherPercent,VehiclePercent=VehiclePercent, PersonPercent=PersonPercent )

@app.route("/all_images.html")
def index2():
    
    def files(path):
        files_path = os.path.join(path, '*')
        files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True) 
        return files
    
    NewPath = r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/Last20" # UPDATE for your computer
    filePaths=files(NewPath)
    s=0
    updatedfiles=[]
    for s in range(0,20):
        filename=filePaths[s].rsplit('/',1)[1]
        updatedfiles.append(r"/static/Last20/" +filename)
    return render_template("all_images.html", files=updatedfiles)

@app.route("/about.html")
def index3():

    return render_template("about.html")

@app.route("/live_feed.html")
def index4():

    return render_template("live_feed.html")

if __name__ == "__main__":
    #app.debug = True
    app.run()