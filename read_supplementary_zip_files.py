from glob import glob
import re
from zipfile import ZipFile
from io import BytesIO
import os

files = glob('REStud papers/*/*ppl*.zip')

MS_ID = re.compile(r'[12][0-9]{4}')
ZIP_FILE = re.compile(r'\.zip$', flags=re.IGNORECASE)

NR_EXTENSIONS={"Python":0, "Stata":0, "R":0, "MatLab":0, "C":0, "Fortran":0, "bash":0}
#store number of used extensions

EXTENSIONS={"Python": ".py", "Stata":".do", "R": ".r", "MatLab": ".m", "C": ".c", "Fortran": ".f", "bash": ".sh"}
#extension ids

FLAGS={"Python":0, "Stata":0, "R":0, "MatLab":0, "C":0, "Fortran":0, "bash":0}
#store the flags given to zips

def count_extensions(name, extensions, nr_extensions):
        for key in nr_extensions:
            if key == "Fortran" and (os.path.splitext(name)[1][:2] == extensions[key] ):
                nr_extensions[key]+=1
               
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
    for name in zf.namelist():
    	reset_extension_nr(NR_EXTENSIONS)
    	count_extensions(name, EXTENSIONS, NR_EXTENSIONS)
        if ZIP_FILE.search(name) is not None:
            # FIXME: does it work 2-3 deep? zip in zip in zip?
            print('-Found {}'.format(name))
            yield from tree_in_zip(path+'/'+name, BytesIO(zf.read(name)))
        else:
            yield path+'/'+name

def flager(name, nr_extensions, flags):
    format_list[0]=os.path.splitext(name)[0]
    format_list[1]=max(nr_extensions, key=nr_extensions.get)
    format_list[2]=os.path.splitext(name)[1]
    name=os.rename(name,'{}_{}{}'.format(*format_list))
    #extends zip files with a flag of most used script files
    flags[max(nr_extensions, key=nr_extensions.get)]+=1 
    #counts the flags given


for name in files:
    for entry in tree_in_zip(name):
        print(entry)
    flager(name, NR_EXTENSIONS, FLAGS)