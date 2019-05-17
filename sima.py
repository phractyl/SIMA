#change the keys and values in this section to whatever you are searching for, you can add more as needed
a_dict = {
    'Key1': ('value1','value2'),
    'Key2': ('value3','value4'),
    'Key3': ('value5','value6'),
}

def percentage(part, whole):
  return 100 * float(part)/float(whole)

#list all the tuples into a big fat list for one iteration
one_big_list = list(item for items in a_dict.values() for item in items)


#build GUI for text file selection
import PySimpleGUI as sg      
window_rows = [[sg.Text('Please select a .txt file for analysis')],      
                 [sg.InputText(), sg.FileBrowse()],      
                 [sg.Submit(), sg.Cancel()]]      
window = sg.Window('SIMA', window_rows)    
event, values = window.Read()    
window.Close()
source_filename = values[0]   

#Open selected text file and tokenize
import nltk 
from nltk import word_tokenize
f = open(source_filename, encoding = 'ISO-8859-1')
raw = f.read()
tokens = nltk.word_tokenize(raw)
tokens = nltk.wordpunct_tokenize(raw)
import string
table = str.maketrans ('', '', string.punctuation)
words = [w.translate(table) for w in tokens]
words = [word for word in tokens if word.isalpha()]

#dictionary iteration party
word_count_dict = {}
with open(source_filename, encoding='ISO-8859-1') as f:
    for line in f:
        for item in one_big_list:
            line_split = list(line.strip('\n').split(' ')) 
            if item in line_split:
                #print(f"found {item} in {line}")  #uncomment to see line context
                if item not in word_count_dict.keys():
                    word_count_dict[item] = line_split.count(item) 
                else:
                    word_count_dict[item] = word_count_dict[item] + line_split.count(item) 

#print(word_count_dict) #uncomment to see all tagged words and their counts
ideal_output = {}
for count in word_count_dict:
    for key, value in a_dict.items():
        if count in value:
            if key not in ideal_output:
                ideal_output[key] = word_count_dict.get(count) 
            else:
                ideal_output[key] = ideal_output[key] + word_count_dict.get(count) 
                
for item in ideal_output:
   string_list = [] 
   tuple_of_words = a_dict[item]
   for entry in tuple_of_words:
       get_times_said = word_count_dict.get(entry)
       if get_times_said:
           string_list.append(f"'{entry}': {get_times_said}")

   print(f"{item}: {ideal_output.get(item)} found, {round(percentage(ideal_output.get(item), len(words)), 2)}% of total words in document: {', '.join(string_list)}.")
