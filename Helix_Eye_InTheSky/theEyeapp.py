    
path_to_watch = r"/Users/BFick/Dropbox/Apps/Camera_Images/Apps/Camera_Images/"                            # Watching Desktop

before = dict ([(f, None) for f in os.listdir (path_to_watch)]) # Load 'before' dictionary

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
    filename=filePaths[s].rsplit('/',1)[1]
    updatedfiles.append(r"/static/Last20/" +filename)
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
            