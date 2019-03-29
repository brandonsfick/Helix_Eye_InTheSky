import os, time
import glob
from shutil import copy2
import shutil
from twilio.rest import Client  
path_to_watch = r"/Users/BFick/Dropbox/Apps/Camera_Images/Apps/Camera_Images/"                            # Watching Desktop
path = r"/Users/BFick/Dropbox/Apps/Camera_Images_Cropped/Apps/Camera_Images_Cropped"
before = dict ([(f, None) for f in os.listdir (path)]) # Load 'before' dictionary

while 1:
    Car = None
    Person = None
    nonAlert = None
    added = ''
    after = dict ([(f, None) for f in os.listdir (path_to_watch)]) # Load 'after' dictionary
    added = [f for f in after if not f in before]                  # Was anything added?
    removed = [f for f in before if not f in after]                # Was anything removed?
    
    if added: 
        print("Added: ", ", ".join (added))
    
        def files(path):
            files_path = os.path.join(path, '*')
            files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True) 
            return files
        filePaths=files(path_to_watch)

        NewPath = r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/Last20"
        shutil.rmtree(NewPath)
        os.makedirs(NewPath)
        s=0
        updatedfiles=[]
        for s in range(0,20):
            copy2(filePaths[s], NewPath)

            # i = 0
      
            # for filename in os.listdir("xyz"): 
            #     dst ="Hostel" + str(i) + ".jpg"
            #     src ='xyz'+ filename 
            #     dst ='xyz'+ dst 
                
            #     # rename() function will 
            #     # rename all the files 
            #     os.rename(src, dst) 
            #     i += 1
            #  copy2(filePaths[s], NewPath)
        # filename = added       # file name
        # # print(filename)
        # filepath = path + "/" + filename[0]  # path object, defining the file
        # print(filepath)

    before = after
        # open the file and upload it
        # with open(filepath, "rb") as f:
        
            # INSERT MODEL HERE


        # Person, vechile, nonAlert

    if Car or Person:
           
        # Your Account Sid and Auth Token from twilio.com/console
        # DANGER! This is insecure. See http://twil.io/secure

        client = Client(account_sid, auth_token)
        text_message = "Your Text Here"
        message = client.messages \
        .create(
                body= text_message,
                from_='+13142072684',
                to='+1314-537-5418'
            )
        print(message.sid)    
    def newest(path):

        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        recentPath=max(paths, key=os.path.getctime)
        result = recentPath.split('/')[-1]
        return result
    
    NewCarpath= r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/NewCar_image/" # * means all if need specific format then *.csv
    NewPersonpath= r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/NewPerson_image/" # * means all if need specific format then *.csv
    NonAlertpath =r"/Users/BFick/Desktop/Helix_Eye_InTheSky/Helix_Eye_InTheSky/static/NonAlert_image/"
    
    # statVar=

    if Car:
        shutil.rmtree(NewCarpath)
        NewCarImage=newest(Car)
        NewCarPath = "static/NewCar_image/" + NewCarImage
        print(NewCarPath)

    if Person:
        shutil.rmtree(NewPersonpath)
        NewPersonImage=newest(Person)
        NewPersonpath = "static/NewPerson_image/" + NewPersonImage
        print(NewPersonpath)

    if nonAlert:
        shutil.rmtree(NonAlertpath)
        NonAlertpath=newest(NonAlert)
        NonAlertpath = "static/NonAlert_image/" + NonAlertpath
        print(NonAlertpath)
        

    time.sleep (1) # 5 sec between polling
