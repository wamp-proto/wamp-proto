from github import Github
import os
from pprint import pprint

g = Github(os.environ['GITHUB_TOKEN'])
u = g.get_user()
orgs = g.get_organizations()
o = g.get_organization('crossbario')

res = []
for r in o.get_repos(type='all'):
    res.append(r.url)

res = sorted(res)
pprint(res)
