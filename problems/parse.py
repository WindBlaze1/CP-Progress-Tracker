import requests
import os
from bs4 import BeautifulSoup

url = requests.get('https://earthshakira.github.io/a2oj-clientside/server/Ladders.html').text

url_soup = BeautifulSoup(url, 'lxml')

urls = url_soup.find_all('a')

print(len(urls))

allproblems = {}

for idx, u in enumerate(urls):

    ladder = requests.get('https://earthshakira.github.io/a2oj-clientside/server/' + u['href']).text
    ladder_soup = BeautifulSoup(ladder, 'lxml')
    prep = ladder_soup.find_all('tr')

    # filename = idx + '. ' + prep[0].td.center.text.split('-')[-1].strip() + '.txt'
    filename = os.path.join('saved', (str(1+idx) + '. ' + prep[0].td.center.text.split('-')[-1].strip() + '.txt'))

    if not (os.path.isdir('saved')):
        os.mkdir('saved')

    filename = filename.replace('<', 'L')
    filename = filename.replace('>', 'G')
    # print(filename)
    del prep[0:4]
    # print(prep)

    for tr in prep:

        temp = tr.find_all('td')
        # print(temp)
        id = temp[1].a['href'].split(
            '/')[-2] + temp[1].a['href'].split('/')[-1]

        if id not in allproblems:
            allproblems[id] = [temp[1].text,temp[3].text]
        with open(filename, 'a') as f:
            t = temp[1].find('a').get('href')
            # print(t)
            f.write(f'{temp[1].text}|{id}|{temp[3].text}|{t}\n')
        f.close()

    print(f'{filename}')

with open(os.path.join('saved','0. All Problems.txt'),'w') as f:
    for i in allproblems:
        f.write(f'{allproblems[i][0]}|{i}|{allproblems[i][1]}\n')
f.close()