from glob import glob
import re, csv
from zipfile import ZipFile, BadZipFile
from gzip import GzipFile
from tarfile import TarFile, ReadError
from io import BytesIO
import os

files = glob('REStud papers/*/*ppl*.zip')

MS_ID = re.compile(r'[12][0-9]{4}')
ZIP_FILE = re.compile(r'\.zip$', flags=re.IGNORECASE)
TAR_FILE=re.compile(r'\.tar', flags=re.IGNORECASE)

NR_EXTENSIONS={ "ms_number": 0,"Python":0, "Stata":0, "R":0, "MatLab":0, "C":0, "Fortran":0, "Bash":0, "LaTeX": 0, "C++": 0, "SAS":0}
#store number of used extensions

EXTENSIONS={"ms_number": "0", "Python": ".py", "Stata":".do", "R": ".R", "MatLab": ".m", "C": ".c", "Fortran": re.compile(r'[.][f][0-9]{2}'), "Bash": ".sh", "LaTeX": ".tex", "C++": ".cpp", "SAS": ".sas"}
#extension ids

MANIFESTO={"ms_number": 0, "file_name": 0, "file_type": 0, "file_size": 0}
#dictionary to help writing in csv


def count_extensions(name, extensions, nr_extensions):
    ext=os.path.splitext(name)[1]
    for key in nr_extensions:
        if key == "Fortran" and extensions["Fortran"].search(ext) is not None:
            nr_extensions[key]+=1
        elif ext == extensions[key] :
            nr_extensions[key]+=1
#stock extensions in nr_extensions

def reset_extension_nr(extensions):
    for key in extensions:
        extensions[key]=0

def manifesto_maker(file, name, manifesto_dict): 
    manifesto_dict["file_name"]=os.path.split(name)[1]
    manifesto_dict["file_type"]=os.path.splitext(name)[1]
    if type(file)==ZipFile:
        manifesto_dict["file_size"]=file.getinfo(name).file_size
    elif type(file)==TarFile:
        manifesto_dict["file_size"]=file.getmember(name).size
        #write filename, extesion and file size of files in the zip into dictionary

def tree_in_zip(path, stream=None):
    print('Trying {}'.format(path))
    if stream is not None and ZIP_FILE.search(path) is not None:
        zf = ZipFile(stream)
        #Check if the file is not the first in the loop and wheter it is a .zip.

    elif stream is None and ZIP_FILE.search(path) is not None:
        zf = ZipFile(path)
        #Check if the first file is .zip.
    else:
        if stream is not None and TAR_FILE.search(path) is not None :
            try: 
                zf=TarFile.open(fileobj=stream, encoding="utf-8",mode='r:*')
            except ReadError:
                pass
            #If the file is not the first in the loop and it is a .tar(.xx) tries to read it as an archive.
        elif stream is None and TAR_FILE.search(path) is not None:
            try:
                zf=TarFile.open(path, mode='r:*')
            except ReadError:
                pass
            #If the first file is a .tar(.xx) tries to read it as an archive.
    try:
        
        if type(zf)==ZipFile:
            try:
                for name in zf.namelist(): 
                    count_extensions(name, EXTENSIONS, NR_EXTENSIONS)
                    #Count extensions of interest in the archive.
                    manifesto_maker(zf, name, MANIFESTO)
                    #fills in the dictionary
                    if ZIP_FILE.search(name) is not None:
                        print('-Found {}'.format(name))
                        yield from tree_in_zip(path+'/'+name, BytesIO(zf.read(name)))
                    elif TAR_FILE.search(name) is not None:
                        print('-Found {}'.format(name))
                        yield from tree_in_zip(path+'/'+name, BytesIO(zf.read(name)))
                    else:
                        yield path+'/'+name
            except BadZipFile:
                pass
            #Search for further archives (.zip/.tar). Exception needed to not to stop at a corrupted archive.
        elif type(zf)==TarFile:
            #No need for try checked the file at the begining.
                for name in zf.getnames():
                    count_extensions(name, EXTENSIONS, NR_EXTENSIONS)
                    manifesto_maker(zf, name, MANIFESTO)
                    if ZIP_FILE.search(name) is not None:
                        print('-Found {}'.format(name))
                        yield from tree_in_zip(path+'/'+name, BytesIO(zf.read(name)))
                    elif TAR_FILE.search(name) is not None:
                        print('- Found {}'.format(name))
                        yield from tree_in_zip(path+'/'+name, BytesIO(zf.read(name)))    
                    else:
                        yield path+'/'+name
        else:
            pass
        #if file is not .tar/.zip skip it
    except UnboundLocalError:
        pass
    #Because of the .tar checks at the begining could happen that there's no zf defined. This way the loop goes on if found a corrupted archive.

ms_language = csv.DictWriter(open('MS_language.csv', 'w'), fieldnames=list(NR_EXTENSIONS.keys()))
ms_language.writeheader()
ms_files=csv.DictWriter(open('MS_manifesto.csv', 'w'), fieldnames=list(MANIFESTO.keys()))
ms_files.writeheader()
#create 2 separate csvs for the extensions and manifesto

for name in files:
    reset_dictionary(NR_EXTENSIONS)
    #Must reset counting outside the functions, because we write in this loop.
    for entry in tree_in_zip(name):
        MANIFESTO["ms_number"]=MS_ID.search(entry).group()
        ms_files.writerow(MANIFESTO)
        print(MANIFESTO)
        #show the row written in ms_manifesto.csv
    NR_EXTENSIONS["ms_number"]=MS_ID.search(name).group()
    print(NR_EXTENSIONS)
    #Show the row written in ms_language.csv.
    ms_language.writerow(NR_EXTENSIONS)