import pandas as pd
from csv import DictWriter
#df = pd.read_csv('output.csv', error_bad_lines=False)
#df.to_csv('output.csv', mode = 'a', index=False, header=False)

field_names = ['text', 'subjectivity', 'polarity']
 
# Dictionary that we want to add as a new row
dict = {'ID': 6, 'NAME': 'William', 'RANK': 5532,
        'ARTICLE': 1, 'COUNTRY': 'UAE'}
 
# Open CSV file in append mode
# Create a file object for this file
with open('event.csv', 'a') as f_object:
 
    # Pass the file object and a list
    # of column names to DictWriter()
    # You will get a object of DictWriter
    dictwriter_object = DictWriter(f_object, fieldnames=field_names)
 
    # Pass the dictionary as an argument to the Writerow()
    dictwriter_object.writerow(dict)
 
    # Close the file object
    f_object.close()