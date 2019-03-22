from glob import glob
import re, csv
from zipfile import ZipFile, BadZipFile
from io import BytesIO
import os, os.path

files = glob('REStud papers/*/*ppl*.zip')

MS_ID = re.compile(r'[12][0-9]{4}')
ZIP_FILE = re.compile(r'\.zip$', flags=re.IGNORECASE)

NR_EXTENSIONS={"Python":0, "Stata":0, "R":0, "MatLab":0, "C":0, "Fortran":0, "bash":0}
#store number of used extensions

EXTENSIONS={"Python": ".py", "Stata":".do", "R": ".r", "MatLab": ".m", "C": ".c", "Fortran": ".f", "bash": ".sh"}
#extension ids

FLAGS={"Python":0, "Stata":0, "R":0, "MatLab":0, "C":0, "Fortran":0, "bash":0}
#store the flags given to zips

LANGUAGE={"ms_number":"","Python":False, "Stata":False, "R":False, "MatLab":False, "C":False, "Fortran":False,"Bash":False}
#support dictionary to write rows

def count_extensions(name, extensions, nr_extensions):
        for key in nr_extensions:
            if key == "Fortran" and (os.path.splitext(name)[1][:2] == extensions[key] ):
                nr_extensions[key]+=1
            #count problems if there are any .f* extensions except fortran
            elif os.path.splitext(name)[1] == extensions[key] :
                nr_extensions[key]+=1
#stock extensions in nr_extensions

def reset_extension_nr(extensions):
    for key in extensions:
        extensions[key]=0

def tree_in_zip(path, stream=None):
    print('Trying {}'.format(path))
    if stream is not None:
        zf = ZipFile(stream)
    else:
        zf = ZipFile(path)
    reset_extension_nr(NR_EXTENSIONS)
    try:
        for name in zf.namelist(): 
            count_extensions(name, EXTENSIONS, NR_EXTENSIONS)
            if ZIP_FILE.search(name) is not None:
                # FIXME: does it work 2-3 deep? zip in zip in zip? | FIXED!(maybe)
                print('-Found {}'.format(name))
                yield from tree_in_zip(path+'/'+name, BytesIO(zf.read(name)))
            else:
                yield path+'/'+name
    except BadZipFile :
        pass

def flager(name, nr_extensions, flags):
	format_list=['','','']
    format_list[0]=os.path.splitext(name)[0]
    format_list[2]=os.path.splitext(name)[1]
    if max(nr_extensions.values()) == 0 :
        name=os.rename(name,name) 
        #leaves the name unchanged if there's no script
    else :
        i=0
        sort=(sorted(nr_extensions, key=nr_extensions.__getitem__, reverse=True))
        while nr_extensions[sort[i]]!=0 :
            format_list[1]=format_list[1]+'_'+sort[i]
            flags[sort[i]]+=1 
            #count flags given
            language[sort[i]]=True 
            #set for the row to wirte out
            i+=1
        name=os.rename(name,'{}{}{}'.format(format_list[0],format_list[1],format_list[2])) 
        #flags zip with every used script

for name in files:
    for entry in tree_in_zip(name):
        print(entry)
    flager(name, NR_EXTENSIONS, FLAGS)
################################################################################################
####LANGUAGE["ms_number"]=MS_ID.match(name)
####writer = csv.DictWriter(open('MS_language.csv', 'w'), fieldnames=list(LANGUAGE.keys()))
####writer.writeheader()
####writer.writerow(LANGUAGE)
# under construction