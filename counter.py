import csv
import string
import urllib
from bs4 import BeautifulSoup
import requests

import StringIO
import re

url = "http://www.plainsimplewebdesign.com/"
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html, 'lxml')

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

text = text.encode('ascii', 'ignore').decode('ascii')

text= filter(lambda s: not str(s).lstrip('-').isdigit(), text)

text = re.sub(r'[^\w]', ' ', text)

#translator = str.maketrans('', '', string.punctuation)

word_count = {}


words = text.split()
for word in words:
    #word = word.translate(translator).lower()
    count = word_count.get(word, 0)
    count += 1
    word_count[word] = count

word_count_list = sorted(word_count, key=word_count.get, reverse=True)
for word in word_count_list[:10]:
    print(word, word_count[word])

output_file = open('words.csv', 'w')
writer = csv.writer(output_file)
writer.writerow(['word', 'count'])
for word in word_count_list:
    writer.writerow([word, word_count[word]])
