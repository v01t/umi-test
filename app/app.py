import os
from datetime import datetime
import requests
from elasticsearch import Elasticsearch

es = Elasticsearch(os.environ['ES_HOST'], http_auth=(os.environ['ES_USER'],os.environ['ES_PWD']), retry_on_timeout=True)

headers = {
	'Authorization': 'token %s' % os.environ['GITHUB_TOKEN']
}

def get_commits(repo):
	commits = []
	next = True
	i = 1
	while next == True:
		commit_page = requests.get('https://api.github.com/repos/{}/commits?page={}&per_page=100'.format(repo, i), headers=headers)
		for commit in commit_page.json():
			commits.append(commit)
		if 'Link' in commit_page.headers:
			if 'rel="next"' not in commit_page.headers['Link']:
				next = False
		i = i+1
	return commits

authors_regdate = {}
def get_author_regdate(username):
	if username not in authors_regdate:
		author_regdate = requests.get('https://api.github.com/users/{}'.format(username), headers=headers).json()['created_at']
		authors_regdate[username] = author_regdate
	else:
		author_regdate = authors_regdate[username]
	return author_regdate

authors_lookups = {}
for c in get_commits(os.environ['GITHUB_REPO']):
	author = {}
	if c['author']:
		author['username'] = c['author']['login']
		author['regdate'] = get_author_regdate(author['username'])
	else:
		author = {}
		if c['commit']['committer']['email'] not in authors_lookups:
			author_search = requests.get('https://api.github.com/search/users?q={}&nbspin:email'.format(c['commit']['committer']['email'].lower()), headers=headers)
			if author_search.json()['total_count'] > 0:
				print('{} {} - Search for username using {} succesful, search return {} records'.format(datetime.now(),c['sha'],c['commit']['committer']['email'],author_search.json()['total_count']))
				author['username'] = author_search.json()['items'][0]['login']
				author['regdate'] = get_author_regdate(author['username'])
			else:
				print('{} {} - Search for username using "{}" failed, search return 0 records, inserting author name instead'.format(datetime.now(),c['sha'],c['commit']['committer']['email']))
				author['name'] = c['commit']['committer']['name']
				author['email'] = c['commit']['committer']['email']
		else:
			author['username'] = authors_lookups[c['commit']['committer']['email']]
			author_regdate = get_author_regdate(author['username'])
	
	doc = {
		'date': c['commit']['committer']['date'],
		'author': author,
		'msg': c['commit']['message']
	}
	r = es.index(index=os.environ['ES_INDEX'], id=c['sha'], body=doc)
	print("{} {} - {}".format(datetime.now(),c['sha'],r['result']))
