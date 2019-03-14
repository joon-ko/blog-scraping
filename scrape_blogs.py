import urllib.request as urllib
from bs4 import BeautifulSoup
import os
import threading

# get the URL links to all blog posts
links = []
for n in range(1, 353):
	print('on page {}'.format(n))

	url = 'https://mitadmissions.org/blogs/page/{}/'.format(n)
	page = urllib.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')

	# each blog link is in class 'post-tease__h__link'
	for link in soup.find_all('a', class_='post-tease__h__link'):
		links.append(link.get('href'))

print('{} blog posts scraped.'.format(len(links)))

# take list of links to blogs and do relevant stuff with them
def process_links(links):
	for link in links:
		page = urllib.urlopen(link)
		soup = BeautifulSoup(page, 'html.parser')

		author = soup.find('span', class_='page-topper__title__name').text[3:]
		title = soup.head.title.text[:-17]
		body = soup.find('div', class_='article__body js-hang-punc')
		text = body.text
		date = soup.find('time', class_='page-topper__date').text

		dir_path = 'C:\\Users\\joonh\\Documents\\blogs\\{}'.format(author)
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)

		filename = str(link)[38:-1] + '.txt'
		file_path = dir_path + '\\{}'.format(filename)
		if not os.path.exists(file_path):
			with open(file_path, 'w', encoding='utf-8') as f:
				f.write('{}\n{}\n{}\n{}'.format(title, author, date, text))

		print('Processed: {} by {} ({})'.format(title, author, date))

# break up list of links into six smaller lists
# process the list several times faster? is the goal?
interval = len(links) // 6
one = links[:interval]
two = links[interval:2*interval]
three = links[2*interval:3*interval]
four = links[3*interval:4*interval]
five = links[4*interval:5*interval]
six = links[5*interval:]
threading.Thread(target=process_links, args=(one,)).start()
threading.Thread(target=process_links, args=(two,)).start()
threading.Thread(target=process_links, args=(three,)).start()
threading.Thread(target=process_links, args=(four,)).start()
threading.Thread(target=process_links, args=(five,)).start()
threading.Thread(target=process_links, args=(six,)).start()