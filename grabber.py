import os
import requests
import re
import time


url = "http://example.com" # the website you will be getting files from
login_url = "http://example.com/login" # the login website

#User login

payload = {
            'username': 'your_username',
            'password': 'your_password'
}
#the names of the keys of the payload dict must reflect the login website's source code


with requests.Session() as session:
    post = session.post(login_url, data=payload)
    response = session.get(url)

#Creating a local folder, if there isn't one

folder_location = r'E:\webscraping'
if not os.path.exists(folder_location):os.mkdir(folder_location)

#Acquiring and formatting data to get download links

"""
Originally, the file repository that I was supposed to scrape and the data
returned in the response was a hot mess and I had to download every possible
file (there were very many), so this solution is somewhat radical - it sure can
be improved upon!
"""

jsondata = response.json()

records = []
unparsed_links = []

for entry in jsondata['data']:
    records.append(entry)

for record in records:
    for elem in record:
        if isinstance(elem, str):
            if 'href' in elem: #finding links to files by hrefs, can be improved
                unparsed_links.append(elem)


parsed_links = []

for link in unparsed_links:
    parsed_links.append((re.findall(r'"(.*?)"', link))) #a regex to get the portion from between ""

path = "http://example.com" #the header of the absolute path to download files
final_links = []

for link in parsed_links:
    for elem in link:
        new_elem = path + elem[2:] #that worked in my specific case, you may need to change this
        final_links.append(new_elem)
for link in final_links[:]:
    if 'php' in link:
        final_links.remove(link)
"""
In my case, I had some dead links to php scripts that did not download any files,
so I needed to get rid of them. I am, however, preserving this snippet here,
as it contains a very nifty trick to dynamically remove elements from a list.
"""

#Download the actual files
for link in final_links:
    filename = os.path.join(folder_location, link.split('/')[-1])
    with open(filename, 'wb') as f:
            f.write(requests.get(link).content)
            time.sleep(0.500) #to avoid cluttering the server if there are many files
