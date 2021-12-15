import os
import json
import argparse
from pprint import pprint

from github import Github

import txaio
txaio.use_twisted()


def sum_contributor_stats(s):
    additions = 0
    deletions = 0
    changes = 0
    for w in s.weeks:
        additions += w.a
        deletions += w.d
        changes += w.c
    obj = {
        'contributor': s.author.login,
        'a': additions,
        'd': deletions,
        'c': changes,
    }
    return obj

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, help='Enable logging at level "debug".')
    parser.add_argument('--output', dest='output', type=str, default=None,
                        help='Output file to write snapshot of contributors data for repositories in WEPs.')
    options = parser.parse_args()

    if options.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    RESULT = {}

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

    # https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html
    for wep_name, repo_names in REPOS.items():
        contributors_all = set()
        contributor_stats_all = {}
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
            # https://pygithub.readthedocs.io/en/latest/github_objects/StatsContributor.html

            stats = repo.get_stats_contributors()
            for s in stats:
                if s.author.login not in contributor_stats_all:
                    contributor_stats_all[s.author.login] = {
                        'a': 0,
                        'd': 0,
                        'c': 0,
                    }
                st = sum_contributor_stats(s)
                contributor_stats_all[s.author.login]['a'] += st['a']
                contributor_stats_all[s.author.login]['d'] += st['d']
                contributor_stats_all[s.author.login]['c'] += st['c']

        for s in ['NamedUser(login="dependabot[bot]")', 'NamedUser(login=None)']:
            contributors_all.discard(s)

        contributors_count = len(contributors_all)
        print('{}: {} repos with {} stars, {} forks, {} contributors and {} open issues'.format(wep_name, repos_count, stargazers_count, forks_count, contributors_count, open_issues_count))

        RESULT[wep_name] = {
            'repos_count': repos_count,
            'stargazers_count': stargazers_count,
            'forks_count': forks_count,
            'contributors_count': contributors_count,
            'open_issues_count': open_issues_count,
            'contributor_stats': contributor_stats_all,
        }

    if options.output:
        print()
        with open(options.output, 'wb') as f:
            data = json.dumps(RESULT, ensure_ascii=False, sort_keys=True).encode()
            f.write(data)
        print('Written {} bytes to output file {}'.format(len(data), options.output))
