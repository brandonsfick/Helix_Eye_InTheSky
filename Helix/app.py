import os
import os, time
import pandas as pd
import numpy as np
from pw import *  
import sqlalchemy
from flask_pymongo import PyMongo
from flask import send_file
import dropbox

from flask import Flask, render_template, redirect
from flask import send_from_directory

app = Flask(__name__)



dbx = dropbox.Dropbox(access_token)
k=0
global before 
before = dict ([(f, None) for f in dbx.files_list_folder('/Apps/Camera_Images/Test/').entries])
@app.route("/")
def home():
    global k
    global dbx
    global before
    while 1:
        added = ''
        
        after = dict ([(f, None) for f in dbx.files_list_folder('/Apps/Camera_Images/Test').entries]) # Load 'after' dictionary
        added = [f for f in after if not f in before]                  # Was anything added?
        removed = [f for f in before if not f in after]                # Was anything removed?
        k=k+1
        before = after
        print(before)
        print(after)
        print(added)
        time.sleep (60) # 5 sec between polling
        # if added: 
        #     print(added)
        
            
            # target = "/Apps/Camera_Images/"              # the target folder
            # targetfile = target + filename   # the target path and file name

            # f, metadata = client.get_file_and_metadata(target+ added)
            
            # out = open(j)
            # out.write(f.read())
            # out.close()
            # print metadata

  

if __name__ == "__main__":
    app.run(debug=True)