import os
from pprint import pprint
from github import Github


def sum_contributor_stats(s):
    weeks = 0
    additions = 0
    deletions = 0
    changes = 0
    for w in s.weeks:
        weeks += 1
        additions += w.a
        deletions += w.d
        changes += w.c
    obj = {
        'contributor': s.author.login,
        'weeks': weeks,
        'additions': additions,
        'deletions': deletions,
        'changes': changes,
    }
    return obj


REPOS = {
    'WEP002': ['wamp-proto/wamp-proto'],
    'WEP010': ['crossbario/crossbar',
               'crossbario/txaio',
               'crossbario/autobahn-python',
               'crossbario/zlmdb',
               'crossbario/cfxdb'],
    'WEP011': ['crossbario/autobahn-js',
               'crossbario/autobahn-java',
               'crossbario/autobahn-cpp',],
}

g = Github(os.environ['GITHUB_TOKEN'])

if False:
    for repo in g.get_user().get_repos():
        print(repo.name, repo.stargazers_count)

# https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html
for wep_name, repo_names in REPOS.items():
    contributors_all = set()

    stargazers_count = 0
    forks_count = 0
    open_issues_count = 0
    repos_count = 0
    contributors_count = 0

    for repo_name in repo_names:
        repo = g.get_repo(repo_name)

        repos_count += 1
        stargazers_count += repo.stargazers_count
        forks_count += repo.forks_count
        open_issues_count += repo.open_issues_count
        print('   {} @ {} ..'.format(repo.default_branch, repo.full_name))

        # repo contributors
        # https://stackoverflow.com/questions/36410357/github-v3-api-list-contributors
        # https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository.get_contributors
        # https://pygithub.readthedocs.io/en/latest/github_objects/NamedUser.html#github.NamedUser.NamedUser
        # https://docs.github.com/en/rest/reference/repos#list-repository-contributors

        contributors = []
        for c in repo.get_contributors(anon=False):
            contributors.append(str(c))

        #print(type(contributors))
        #print(contributors)
        contributors_all.update(contributors)
        if False:
            for c in contributors:
                #print(c, dir(c))
                #print(c.login)
                #if c.login and c.login not in ['dependabot[bot]']:
                print(c)
                contributors_count += 1

        # https://pygithub.readthedocs.io/en/latest/github_objects/StatsContributor.html
        stats = repo.get_stats_contributors()
        res = []
        for s in stats:
            res.append((s.total, s.author.login, sum_contributor_stats(s)))
        res = list(reversed(sorted(res)))
        pprint(res)

        if False:
            pprint([#repo.name,
                    repo.full_name,
                    #repo.id,
                    #repo.name,
                    #repo.owner,
                    #repo.created_at,
                    #repo.homepage,
                    repo.default_branch,
                    repo.description,
                    repo.stargazers_count,
                    repo.forks_count,
                    ])

    for s in ['NamedUser(login="dependabot[bot]")', 'NamedUser(login=None)']:
        contributors_all.discard(s)

    contributors_count = len(contributors_all)
    print('{}: {} repos with {} stars, {} forks, {} contributors and {} open issues'.format(wep_name, repos_count, stargazers_count, forks_count, contributors_count, open_issues_count))

    # pprint(contributors_all)
    print()
