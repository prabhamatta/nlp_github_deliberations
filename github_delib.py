__author__ = 'Prabhavathi Matta'
__Project__= 'GitHub Deliberations Data Extraction Module'

from urllib2 import urlopen
import json
import re
from datetime import datetime
import time

#ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
ISO8601 = "%Y-%m-%dT %H:%M:%SZ"
github_token = "e072092b2d381eb6e828f954a2b75a6c148fc57a"


def getCoreCollaborators(main_url):
    #GET /repos/:owner/:repo/collaborators
    url = main_url + '/collaborators?access_token={0}'.format(github_token)
    #coreCollaborators = open("core_collaborators.json", 'w')
    #coreCollaborators.write(json.dumps(getPagedRequest(url)))
    #coreCollaborators.close()
    
    coreCollaboratorsFormatted = open("core_collaborators_formatted.txt", 'w')
    for user in getPagedRequest(url):
        coreCollaboratorsFormatted.write(user["login"] +"\t"+ str(user["id"]) +"\t"+ user["url"] + "\n")
    coreCollaboratorsFormatted.close()
    
    

def getContributors(main_url):
    """
    # Get contributors list with additions, deletions, and commit counts
    # GET /repos/:owner/:repo/stats/contributors
    # format of the output http://developer.github.com/v3/repos/statistics/#get-contributors-list-with-additions-deletions-and-commit-counts
    """
    url = main_url + '/stats/contributors?access_token={0}'.format(github_token)
    print url
    summary = open("contributors_summary.txt", 'w')
    details = open("contributors_all.json", 'w')

    data = getPagedRequest(url)
    for user in data:
        summary.write(str(user["author"]["login"])+"\t" + str(user["author"]["id"]) +"\t"+ str(user["author"]["url"]) + "\t" + str(user["total"]) + "\n")
        #details.write(user["id"]+"\t" + user["id"] +"\t"+ user["url"] + "\t" + user["total"]
    details.write(json.dumps(data))

    summary.close()
    details.close()
    return



def getIssues( main_url, state='all'):
    url = main_url + '/issues?access_token={0}&state={1}'.format(github_token,state)
    return getPagedRequest(url)

def getIssueComments( main_url, issue_id):
    # GET /repos/:owner/:repo/issues/:number/comments
    url = main_url + '/issues/{0}/comments?access_token={1}'.format( issue_id, github_token)
    return getPagedRequest(url)

def getCommits( main_url):
    # GET /repos/:owner/:repo/commits
    url = main_url + '/commits?access_token={0}'.format(github_token)
    return getPagedRequest(url)

def getCommitInfo( main_url, sha):
    # GET /repos/:owner/:repo/commits/:sha
    url = main_url + '/commits/{0}?access_token={1}'.format(sha, github_token)
    #print json.load(urlopen(url))
    return getPagedRequest(url)

def getReleases( project_url):
    # GET /repos/:owner/:repo/releases
    pass

# from https://github.com/nipy/dipy/blob/master/tools/github_stats.py
element_pat = re.compile(r'<(.+?)>')
rel_pat = re.compile(r'rel=[\'"](\w+)[\'"]')

def parseLinkHeaders(headers):
    link_s = headers.get('link', '')
    urls = element_pat.findall(link_s)
    rels = rel_pat.findall(link_s)
    d = {}
    for rel,url in zip(rels, urls):
        d[rel] = url
    return d

def getPagedRequest(url):
    """get a full list, handling APIv3's paging"""
    results = []
    while url:
        print("fetching %s" % url)
        f = urlopen(url)
        results_json = json.load(f)
        if type(results_json) == list:
            results.extend(results_json)
        else:
            results.extend([results_json])

        links = parseLinkHeaders(f.headers)
        url = links.get('next')
        time.sleep(0.25)
    return results


if __name__ == '__main__':
    project = "bitcoin"
    repo = "bitcoin"
    main_url = "https://api.github.com/repos/"+ project+"/"+repo
    print main_url
    getContributors(main_url)
    #getCoreCollaborators(main_url)
    #print getCommits(main_url)



    #getCommitInfo(settings, project_url, 'd31f0a266863e23ddfb5f68d48059a5d67f6d683')[0]

    #open_issues = getIssues(settings, project_url, state='open')

    #open_issues[0]

    #closed_issues = getIssues(project_url, state='closed')

    ##  Note issues have ONLY a comments_url, not the actual comments
    #closed_issues[0]


    #print len(open_issues)
    #print len(closed_issues)


    #issue_meta = ['title', 'created_at', 'labels', 'closed_at', 'user', 'id', 'number', 'comments']
    #iclosed = pd.DataFrame(closed_issues, columns=issue_meta)
    #iclosed['user'] = iclosed.user.map(lambda user: user['login'])


    #iclosed.number[0]

    #getIssueComments(settings, project_url, 4490)



