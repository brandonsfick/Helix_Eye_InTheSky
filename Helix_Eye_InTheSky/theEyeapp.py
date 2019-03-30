#import libraries
import scipy.io as sio
import pandas as pd
import numpy as np
import os
import tensorflow as tf
import keras
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import time
import glob
from shutil import copy2
import shutil
from twilio.rest import Client  
import api_key


#preliminary model libraries
from keras import regularizers
from keras.preprocessing import image
from keras.layers import Dense, GlobalAveragePooling2D, Dropout
from keras.models import Model
from keras.applications.xception import (
    Xception, preprocess_input, decode_predictions)

#comparator libraries
from skimage import io, measure
from skimage.measure import compare_ssim
import cv2

#declare globals
path_to_watch = r"/Users/BFick/Dropbox/Apps/Camera_Images/Apps/Camera_Images/"                            # Watching Desktop
path = r"/Users/BFick/Dropbox/Apps/Camera_Images_Cropped/Apps/Camera_Images_Cropped"
before = dict ([(f, None) for f in os.listdir (path)]) # Load 'before' dictionary


def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    recentPath=max(paths, key=os.path.getctime)
    return recentPath

def files(path):
            files_path = os.path.join(path, '*')
            files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True) 
            return files

def Model(Image_path):
        Alertlist = [False,"V/P","SSIM","XCP"]

        #Load Pre-trained model
        model = Xception(
            include_top=True,
            weights='imagenet')
        image_size = (299, 299, 3)

        #load pre-trained model categories
        VID = pd.read_csv(r"/Users/BFick/Desktop/Helix_Eye_InTheSky/vehicle_categories.txt", sep='\t')
        CID = pd.read_csv(r"/Users/BFick/Desktop/Helix_Eye_InTheSky/clothing_categories.txt", sep='\t')


        #Run image through Primary Model
        data2 = []
        ismatch = 0

        image_size = (299, 299, 3)

        #image_path = newest(path)
        img = image.load_img(Image_path, target_size=image_size)

        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        predictions = model.predict(x)

        result = decode_predictions(predictions, top=3)
        topresult = result[0][0]
        result2 = result[0][1]
        result3 = result[0][2]

        if (topresult[0] in VID['Serial'].values) or (result2[0] in VID['Serial'].values) or (result3[0] in VID['Serial'].values):
            imgclass = "Vehicle"
            if (topresult[0] in VID['Serial'].values):
                classp = str((round(topresult[2]*1000))/10)
            elif (result2[0] in VID['Serial'].values):
                classp = str((round(result2[2]*1000))/10)
            else: # (result3[0] in VID['Serial'].values):
                classp = str((round(result3[2]*1000))/10)
            ismatch = 1 
        elif (topresult[0] in CID['Serial'].values) or (result2[0] in CID['Serial'].values) or (result3[0] in CID['Serial'].values):
            imgclass = "Person"
            if (topresult[0] in CID['Serial'].values):
                classp = str((round(topresult[2]*1000))/10)
            elif (result2[0] in CID['Serial'].values):
                classp = str((round(result2[2]*1000))/10)
            else: #(result3[0] in CID['Serial'].values):
                classp = str((round(result3[2]*1000))/10) 
            ismatch = 2
        else:
            imgclass = "Other"# + str((round(topresult[2]*1000))/10)
            classp = str((round(topresult[2]*1000))/10)
            Alertlist = [False,"Other","N/A",classp]
            return Alertlist

        Alertlist[3] = classp

        data2.append([topresult[0],topresult[1],(round(topresult[2]*1000))/10,imgclass, classp, ismatch])
        data2 = pd.DataFrame(data2, columns = ['Serial','Pred','Prob','Class','Class Pr','Match'])

        #load Scenario images for the comparator
        Sarray = [0]
        for scen in range(1,19):
            Sarray.append(io.imread(r'/Users/BFick/Desktop/Helix_Eye_InTheSky/Car Data/cam_base/S%s.jpg' %(scen)))

        comparray = []
        i1 =0

        #cycle through photo backlog
        for img1 in data2['Serial']:
        #for img1 in range(120,130):
            i1+=1
            # print(i1,data2[data2.Serial==img1].Match.item())
            
            #cycle through scenarios for each photo
            resultarray = []
            
            imgpathio = io.imread(Image_path)
        
            if data2[data2.Serial==img1].Match.item() ==2:
                #if photo matched to person, run against S1 & S10
                for R in (1,10):
                    scenario = Sarray[R]
                    combossim = round(compare_ssim(imgpathio,scenario,multichannel=True)*1000)/10

                    resultarray.append([R,combossim,"P"])
            else:   
                #if photo matched to vehicle, run against all
                for S in range(1,19):
                    scenario = Sarray[S]
                    combossim = round(compare_ssim(imgpathio,scenario,multichannel=True)*1000)/10

                    resultarray.append([S,combossim,"V"])
            resultdf = pd.DataFrame(resultarray, columns = ['Scenario','SSIM','Type']) 
        

            #find best match
            Y = int(str(resultdf.loc[resultdf['SSIM'].idxmax()][0]).split('.')[0])
            Bestmatch = Y
            Bestssim = resultdf.loc[resultdf['SSIM'].idxmax()][1]
            Type = resultdf.loc[resultdf['SSIM'].idxmax()][2]
            #Mark high & Low

            #Person thresholds are different from vehicle thresholds 
            if data2[data2.Serial==img1].Match.item() ==2:#Is it a person
                Alertlist[1] = "P"
                if Bestssim >76:
                    Alertlist[0] = False
                else:
                    Alertlist[0] = True
            else:  #or is it a vehicle
                Alertlist[1] = "V"  
                if Bestssim >82:
                    Alertlist[0] = False
                else:
                    Alertlist[0] = True
            Alertlist[2] = Bestssim
                  
        return Alertlist

def RunModel():
    #find most recent file
    inputfile = newest(path)
    #run modle on most reent file
    ImageCheck = Model(inputfile)
    with open("ImageLog.csv", "a") as outfile:
        #add new line
        outfile.write("\n")
        #add timestamp from file
        outfile.write(datetime.utcfromtimestamp(int(os.path.getctime(inputfile))).strftime('%Y-%m-%d %H:%M:%S'))
        for entries in ImageCheck:
            outfile.write(", ")
            outfile.write(str(entries))

    if ImageCheck[1] == "V":
        with open("VehicleLog.csv", "a") as outfile:
            #add new line
            outfile.write("\n")
            #add timestamp from file
            outfile.write(datetime.utcfromtimestamp(int(os.path.getctime(inputfile))).strftime('%Y-%m-%d %H:%M:%S'))
            for entries in ImageCheck:
                outfile.write(", ")
                outfile.write(str(entries))
    elif ImageCheck[1] =="P":
        with open("PeopleLog.csv", "a") as outfile:
            #add new line
            outfile.write("\n")
            #add timestamp from file
            outfile.write(datetime.utcfromtimestamp(int(os.path.getctime(inputfile))).strftime('%Y-%m-%d %H:%M:%S'))
            for entries in ImageCheck:
                outfile.write(", ")
                outfile.write(str(entries))
    else:
        with open("OtherphotoLog.csv", "a") as outfile:
            #add new line
            outfile.write("\n")
            #add timestamp from file
            outfile.write(datetime.utcfromtimestamp(int(os.path.getctime(inputfile))).strftime('%Y-%m-%d %H:%M:%S'))
            for entries in ImageCheck:
                outfile.write(", ")
                outfile.write(str(entries))
    #send alert or not
    return ImageCheck

while 1:
    NewCarpath= r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/NewCar_image/" # * means all if need specific format then *.csv
    NewPersonpath= r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/NewPerson_image/" # * means all if need specific format then *.csv
    NonAlertpath =r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/NonAlert_image/"
    Car = None
    Person = None
    nonAlert = None
    added = ''
    after = dict ([(f, None) for f in os.listdir (path_to_watch)]) # Load 'after' dictionary
    added = [f for f in after if not f in before]                  # Was anything added?
    removed = [f for f in before if not f in after]                # Was anything removed?
    
    if added: 
        print("Added: ", ", ".join (added))
    
        filePaths=files(path_to_watch)

        NewPath = r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/Last20"
        shutil.rmtree(NewPath)
        os.makedirs(NewPath)
        s=0
        updatedfiles=[]
        for s in range(0,20):
            copy2(filePaths[s], NewPath)
    if before != after:
        before = after

        # open the file and upload it
        # with open(filepath, "rb") as f:
        
    #Run Model, receives input as a file path using newest(path)
    
        Sendtext = RunModel()

   

        
        # statVar=
        if Sendtext[0]==False:
            filelist = glob.glob(os.path.join(NonAlertpath, "*.jpg"))
            for f in filelist:
                os.remove(f)
            NonAlertpath=newest(path_to_watch)
            result = NonAlertpath.split('/')[-1]
            NewAlertpath = "static/NonAlert_image/" + result
            shutil.copyfile(NonAlertpath, NewAlertpath)
            print(NonAlertpath)
        
        elif Sendtext[1] == "V":
            filelist = glob.glob(os.path.join(NewCarpath, "*.*"))
            for f in filelist:
                os.remove(f)
            # os.mkdir(NewCarpath)
            NewCarImage=newest(path_to_watch)
            result = NewCarImage.split('/')[-1]
            NewCarpath = "static/NewCar_image/" + result
            shutil.copyfile(NewCarImage, NewCarpath)  

            print(NewCarpath)

        elif Sendtext[1] == "P":
            filelist = glob.glob(os.path.join(NewPersonpath, "*.*"))
            for f in filelist:
                os.remove(f)
            # os.mkdir(NewPersonpath)
            NewPersonImage=newest(path_to_watch)
            result = NewPersonImage.split('/')[-1]
            NewPersonpath = "static/NewPerson_image/" + result
            shutil.copyfile(NewPersonImage, NewPersonpath)  

            print(NewPersonpath)

        if Sendtext[0]:
            
            # Your Account Sid and Auth Token from twilio.com/console
            # DANGER! This is insecure. See http://twil.io/secure
            # account_sid = str(account_sid1)
            # auth_token = str(auth_token1)
            client = Client(api_key.account_sid, api_key.auth_token)
            if Sendtext[1] == "V":
                text_message = "Danger Will Robinson...We have identified an unidentified vehicle. Alert Alert. Danger." 
            else:
                text_message ="Danger Will Robinson...We have identified a Person. Alert Alert. Danger."
            message = client.messages \
                .create(
                        body= text_message,
                        from_='+13142072684',
                        to='+1314-537-5418'
                    )
            print(message.sid)     

        time.sleep (1) # 5 sec between polling
