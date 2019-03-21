from docx import Document
import glob, csv

def get_text_fields(doc):
	return[i.text.strip(' :') for i in doc.element.xpath('//w:t')]
	# create a list from text fields

def get_value(doc,key):
	cells = get_text_fields(doc)
    if key in cells:
        return cells[cells.index(key.strip(' :'))+1]
    else:
        return ''
    #return the part of text appropiate to the key
    #key=which parameter is needed, returns the next element of the list

def get_between(doc, start, end):
    cells = get_text_fields(doc)
    if start not in cells:
        return ''
    i = cells.index(start)
    if end not in cells[i+1:]:
        return cells[i+1]
    j = cells[i+1:].index(end)+i+1
    return '\n'.join(cells[i+1:j])
    #give all elements of the list between the start and end values

FIELDS = dict(ms_number=(get_value, 'Number'), title=(get_between, 'Article Title', 'Manuscript'), 
              author=(get_value, 'Last Name'), email=(get_value, 'E-mail Address'),
             editor=(get_value, 'Accepting Editor'), accepted_date=(get_value, 'Accepted Date'))
	#add a dictionary of needed metadata parameters

def get_fields(doc, fields):
    return {key:fields[key][0](doc, *fields[key][1:]) for key in fields}
    # returns with the neeeded metadata

forms = glob.glob('REStud papers/????? */*.docx')
# use all the paper forms

writer = csv.DictWriter(open('manuscripts.csv', 'w'), fieldnames=list(FIELDS.keys()))
writer.writeheader()
# output file

i = 0
for form in forms:
    i += 1
    print(i, form)
    try:
        writer.writerow(get_fields(Document(form), FIELDS))
    except:
        print('{} failed.'.format(form))
        get_fields(Document(form), FIELDS)
# write every submissions metadata into output, signaling any problems