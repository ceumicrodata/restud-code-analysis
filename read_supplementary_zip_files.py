from glob import glob
import re
from zipfile import ZipFile
from io import BytesIO

files = glob('REStud papers/*/*ppl*.zip')
#use all zip files

MS_ID = re.compile(r'[12][0-9]{4}')
ZIP_FILE = re.compile(r'\.zip$', flags=re.IGNORECASE)
#compile ID number & .zip name

def tree_in_zip(path, stream=None):
    print('Trying {}'.format(path))
    if stream is not None:
        zf = ZipFile(stream)
    else:
        zf = ZipFile(path)
    for name in zf.namelist():
        if ZIP_FILE.search(name) is not None:
            # FIXME: does it work 2-3 deep? zip in zip in zip?
            print('-Found {}'.format(name))
            yield from tree_in_zip(path+'/'+name, BytesIO(zf.read(name)))
        else:
            yield path+'/'+name


for name in files:
    for entry in tree_in_zip(name):
        print(entry)