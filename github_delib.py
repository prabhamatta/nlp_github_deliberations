__author__ = 'Prabhavathi Matta'
__Project__= 'GitHub Deliberations Data Extraction Module'

from urllib2 import urlopen
import json
import sys
import re,codecs
from datetime import datetime
import time
from pprint import pprint


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
    # format of the output http://developer.github.com/v3/repos/statistics/
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

def getIssuesList(main_url, state='open'):
    """
    Imp Note: all pull-requests are "issues" - some are closed/merged and some are still open. 
    When you query pull-requests from api, we get only "open" pull-reuests
    The ideal way would be to get the closed pull-requests from "issues". 
    
    Therefore, I am re-writing the code to get issues. 
    Prabha - Nov14,2013
    
    
    How to get comments from issues:
    *************************
    Issue: https://github.com/GeoNode/geonode/issues/1263
    
    This is the issue: https://api.github.com/repos/GeoNode/geonode/issues/1263
    It has 2 comments: 
    comments url:    https://api.github.com/repos/GeoNode/geonode/issues/1263/comments
    
    Every issue will have its own body/text and each comment will have its own body/text
    """        
    #GET /repos/:owner/:repo/issues
    
    #url = main_url + '/issues?access_token={0}'.format(github_token)
    url = main_url + '/issues?access_token={0}&state={1}'.format(github_token,state)
    
    print url  
    
    data = getPagedRequest(url)
    fname1 = "issues_all_" +state +".tsv"
    fname2 = "issues_conversation_urls_" +state + ".tsv"
    fname3 = "issues_text_" +state + ".tsv"
    
    issues_all = codecs.open(fname1, 'w',  "UTF-8") 
    issues_conversation_urls = codecs.open(fname2, 'w',  "UTF-8") 
    issues_text = codecs.open(fname3, 'w',  "UTF-8") 
    
    
    pulls ={}
    print len(data)
    for pull in data:
        try:
            pull_num = pull["number"]
            pull_state = pull["state"]        
            pull_title = pull["title"]
            pull_url = pull["url"]
            text = pull["body"]
            comments_num = pull["comments"]
            comments_url = pull["comments_url"]
            pull_created_at = pull["created_at"]
            pull_closed_at = pull["closed_at"]
            user_login  = pull["user"]["login"]
            
            #print pull_num
            issues_all.write(str(pull_num)+"\t" + str(pull_state)+"\t" +str(user_login)+"\t"+str(text)+"\t" + str(pull_url)+"\t"  +str(comments_num)+"\t" +str(comments_url)+"\t"+ str(pull_created_at)+"\t" + str(pull_closed_at) +"\n")
            issues_conversation_urls.write(
                 str(pull_num)+"\t" + str(pull_state)+"\t"+str(comments_num)+"\t" +str(comments_url) +"\n" )
            issues_text.write( str(pull_num)+"\t" +str(text)+ "\n" )
        except Exception, e:        
            #print "Error : ", e        
            pass
                        
    issues_all.close()
    issues_conversation_urls.close()
    issues_text.close()

def getIssuesConversations(main_url):
    
    #issues_conversation_text = codecs.open("issues_conversation_text.tsv", 'w',  "UTF-8") 
    issues_conversation_details_all = codecs.open("issues_conversation_details_all.tsv", 'w',  "UTF-8")     


    fnames = ["issues_conversation_urls_open.tsv" ,"issues_conversation_urls_closed.tsv" ]  
    for fname in fnames:
        with codecs.open(fname, 'r',  "UTF-8") as fin:
            for line in fin:
                main_url = line.split("\t")[3].strip()
                issue_id = line.split("\t")[0].strip()
                url = main_url + '?access_token={0}'.format( github_token)
                data = getPagedRequest(url)
                for comment in data:
                    try:
                        comment_id = comment["id"]
                        comment_url = comment["url"]
                        comment_user = comment["user"]["login"]
                        comment_text = comment["body"]
                        
                        issues_conversation_details_all.write( str(issue_id)+"\t"  +str(comment_id)+"\t" +str(comment_url)+"\t"+ str(comment_user)+"\t" + str(comment_text) +"\n")
                        
                        #issues_conversation_text.write(str(issue_id)+"\t"  +str(comment_id)+"\t" +str(comment_url)+"\t"+ str(comment_user)+"\t" + str(comment_text) +"\n")
                    
                    except Exception, e: 
                        #print "Error : ", e 
                        pass
    issues_conversation_details_all.close()
    
    ##GET /repos/:owner/:repo/pulls/comments
    #url = main_url + '/pulls/comments?access_token={0}'.format(github_token)
    #print url
    #pulls = open("pull_request_comments.json", 'w')
    
    #data = getPagedRequest(url)
    #pullRequestComments = {}    
    #for pull in data:
        #pull_num = pull["id"]
        #pull_url = pull["url"]
        #text = pull["body"]
        #commit_id = pull["commit_id"]
        #user_login  = pull["user"]["login"]
        #pull_date = pull["created_at"]
        ##pullRequestComments[pull_num] =
        #print pprint(pull)
        
    
    

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
        #print("fetching %s" % url)
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
    
    #project = "geonode"
    #repo = "geonode"      
    main_url = "https://api.github.com/repos/"+ project+"/"+repo
    print main_url
    #getContributors(main_url)
    #getCoreCollaborators(main_url)
    #print getCommits(main_url)
    
    """
    get issue details and the conversation urls
    """
    #getIssuesList(main_url,"open")
    #getIssuesList(main_url,'closed')
    
    """
    get individual comments of each conversation of each issue
    """    
    getIssuesConversations(main_url)

