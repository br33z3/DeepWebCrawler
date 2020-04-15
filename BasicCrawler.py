import requests
from bs4 import BeautifulSoup


session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050' #proxies for tor connection
session.proxies['https'] = 'socks5h://localhost:9050'
links = [] #all href links inside this list
base_url = "<.onion site>"
counter = 0

r = session.get(base_url)
response = r.content
soup = BeautifulSoup(response, "html.parser")
for link in soup.findAll('a'):
	if link.get('href') != "<.onion site>" and  link.get('href') != "/" and link.get('href') is not None:
		links.append(link.get('href'))

for i  in range(0, len(links)):
	if(links[i].startswith('http://')):
		new_url = links[i]
	else:
		new_url = base_url+links[i]
		links[i] = new_url
	r = session.get(new_url)
	response = r.content
	soup = BeautifulSoup(response, "html.parser")
	for link in soup.findAll('a'):
		if link.get('href') != "<.onion site>" and  link.get('href') != "/" and link.get('href') is not None:
			for a in range(0, len(links)): #search for duplicate links
				if(link.get('href') is links[i]): #if new link not inside links append new link to list
					counter+=1
			if(counter > 0):
				links.append(link.get('href'))
				counter = 0
#----------------------------------------------------------------
#Eliminate Duplicate Links Last Time

result_links = []

for item in links:
	if item not in result_links:
        	result_links.append(item)

#Final Result
for b in range(0, len(result_links)):
	print(result_links[b])

print("Number of links => "+str(len(result_links)))
