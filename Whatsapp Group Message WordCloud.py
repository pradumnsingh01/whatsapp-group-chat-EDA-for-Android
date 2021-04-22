# Importing necessary libraries:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def read_file(file):
    open_file = open(file, "r", encoding = "utf-8")
    read_file = open_file.read()
    content_list = read_file.splitlines()
    return content_list

# Importing the file:

chat = read_file("WhatsApp Chat with DSEFT GGN Aug 20.txt")



for i in chat:
    print(i)
    
# It can be noticed that there are certain lines, where line is not
    # starting with the date. It is so because, the message on the 
    # date-time of previous line is continuing in the next line.
    
check = []
check_f = []

for i in chat:
    if i[:1].isdigit():
        check.append(i)
    else:
        check_f.append(i)
        

# Above, "check" list includes the messeges which are starting from a
    # date.
# the "check_f" list includes those parts of the whatsapp message, 
    # which used 'enter' to continue the message on a new line in the
    #same message block.
    
    
###############################################################################

# Now we will update the list and remove the items which are present
    # in the check_f part from the chat list
    
for i in range(len(chat)):
    if chat[i][:1].isdigit():
        chat[i] = "$$$" + chat[i]
        
# Above, the 'chat' list is updated and each item in the list is 
    # prefixed with "$$$". This "$$$" will be used as a seperator
    # later on.
    
text = ""


for i in range(len(chat)):
    text = text + chat[i]
    
chat_updated = text.split("$$$")

chat_updated = chat_updated[1:]

# Now the problem of usage of "enter" used in message is solved
    # in the chat list.
    

# We will now exract the data from chat_updated and segregagte them
    # into date, contact and message feature.

from datetime import datetime
    
date = []

for i in chat_updated:
    date.append(i[:8] + i[9:15])
    
    
dataset = pd.DataFrame()    

dataset["Date"] = date

for i in date:
    i = datetime.strptime(i, '%d/%m/%y %H:%M')


dataset["Date"].dtypes

dataset["Date"] = pd.to_datetime(dataset["Date"], format = '%d/%m/%y %H:%M')

dataset["Date"].dtypes

# Now, the date column is added in the dataset.

content = []

for i in chat_updated:
    content.append(i[18:])
    
content_seperated = []

for i in content:
    content_seperated.append(i.split(":"))
    
contact = []
    
for i in content_seperated:
    contact.append(i[0])
    
dataset["Contact"] = contact

message = []

for i in content_seperated:
    if len(i) == 2:
        message.append(i[1])
    else:
        message.append(np.nan)
        
dataset["Message"] = message

from wordcloud import WordCloud

words = ""

for i in content_seperated:
    if len(i) == 2:
        words = words + i[1]

########## SAVING THE FINAL DATASET AS CSV ##############

dataset.to_csv("Whatsapp_chat_data.csv")
    

################# WORDCLOUD VISUALIZATION ##############

wc = WordCloud().generate(words)

plt.imshow(wc)
plt.show()