__author__ = 'github_deliberations'
__Project__= 'GitHub Deliberations Data Extraction Module'

from urllib2 import urlopen
import json
import sys
import re,codecs,string
from datetime import datetime
import time
from pprint import pprint
import nltk
from bs4 import BeautifulSoup
from markdown import markdown


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


def removeControlChars(x):
    return "".join([i for i in x if ord(i) in range(32, 127)])

def text_cleanup(text):
    text = text.replace("\t"," ")
    text = text.replace("\n"," ")
    text = text.replace("\r"," ")
    text = text.encode('ascii', 'ignore')
    #newtext= " ".join([(word) for word in text.split() if not (word.startswith('http') or word.startswith("@"))])
    return text
    

def getIssuesList(main_url, state='open'):
    """
    Note: all pull-requests are "issues" - some are closed/merged and some are still open. 
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
    #fname3 = "issues_text_" +state + ".tsv"

    issues_all = codecs.open(fname1, 'w',  "UTF-8") 
    issues_conversation_urls = codecs.open(fname2, 'w',  "UTF-8") 
    #issues_text = codecs.open(fname3, 'w',  "UTF-8") 


    pulls ={}
    print len(data)
    for pull in data:
        try:
            pull_num = pull["number"]
            pull_state = pull["state"]        
            pull_title = pull["title"]
            pull_url = pull["url"]
            body = pull["body"]
            text = text_cleanup(body)            
            comments_num = pull["comments"]
            comments_url = pull["comments_url"]
            pull_created_at = pull["created_at"]
            pull_closed_at = pull["closed_at"]
            user_login  = pull["user"]["login"]
            
            #print text

            #print pull_num
            issues_all.write(str(pull_num)+"\t" + str(pull_state)+"\t" +str(user_login)+"\t"+str(text)+"\t" + str(pull_url)+"\t"  +str(comments_num)+"\t" +str(comments_url)+"\t"+ str(pull_created_at)+"\t" + str(pull_closed_at) +"\n")
            issues_conversation_urls.write(
                str(pull_num)+"\t" + str(pull_state)+"\t"+str(comments_num)+"\t" +str(comments_url) +"\n" )
            #issues_text.write( str(pull_num)+"\t" +str(text)+ "\n" )
        except Exception, e:        
            #print "Error : ", e        
            pass

    issues_all.close()
    issues_conversation_urls.close()
    #issues_text.close()

def getIssuesConversations(main_url):

    issues_conversation_details_all = codecs.open("issues_conversation_details_all.tsv", 'w',  "UTF-8")     
    issues_conversation_details_all_raw = codecs.open("issues_conversation_details_all_raw.tsv", 'w',  "UTF-8")     
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
                        text = comment["body"]
                        comment_text = text_cleanup(text)
                        created_at = comment["created_at"]

                        issues_conversation_details_all.write( str(issue_id)+"\t"+str(comment_id)+"\t" + str(created_at) +"\t"  +str(comment_url)+"\t"+ str(comment_user)+"\t" + str(comment_text) +"\n")
                        
                        comment_dict = {}
                        comment_dict["comment_meta"] = str(issue_id)+"\t"  +str(comment_id)+"\t"  + str(created_at) +"\t" +str(comment_url)+"\t"+ str(comment_user)
                        comment_dict["comment_text"] = text
                        
                        issues_conversation_details_all_raw.write(json.dumps(comment_dict))
                        issues_conversation_details_all_raw.write("\n")

                    except Exception, e: 
                        #print "Error : ", e 
                        pass
    issues_conversation_details_all.close()
    issues_conversation_details_all_raw.close()



def getPullsList(main_url, state='open'):
    url = main_url + '/pulls?access_token={0}&state={1}'.format(github_token,state)

    print url  

    data = getPagedRequest(url)
    fname1 = "pulls_all_" +state +".tsv"
    fname2 = "pulls_conversation_urls_" +state + ".tsv"
    #fname3 = "pulls_text_" +state + ".tsv"

    issues_all = codecs.open(fname1, 'w',  "UTF-8") 
    issues_conversation_urls = codecs.open(fname2, 'w',  "UTF-8") 
    #issues_text = codecs.open(fname3, 'w',  "UTF-8") 


    pulls ={}
    print len(data)
    for pull in data:
        try:
            pull_num = pull["number"]
            pull_state = pull["state"]        
            pull_title = pull["title"]
            pull_url = pull["url"]
            body = pull["body"]
            text = text_cleanup(body)            
            #comments_num = pull["number"]
            comments_url = pull["comments_url"]
            pull_created_at = pull["created_at"]
            pull_closed_at = pull["closed_at"]
            user_login  = pull["user"]["login"]
            
            #print text

            #print pull_num
            issues_all.write(str(pull_num)+"\t" + str(pull_state)+"\t" +str(user_login)+"\t"+str(text)+"\t" + str(pull_url)+"\t" +str(comments_url)+"\t"+ str(pull_created_at)+"\t" + str(pull_closed_at) +"\n")
            issues_conversation_urls.write(
                str(pull_num)+"\t" + str(pull_state)+"\t" +str(comments_url) +"\n" )
            #issues_text.write( str(pull_num)+"\t" +str(text)+ "\n" )
        except Exception, e:        
            print "Error : ", e        
            pass

    issues_all.close()
    issues_conversation_urls.close()
    #issues_text.close()

def getPullsConversations(main_url):

    pulls_conversation_details_all = codecs.open("pulls_conversation_details_all.tsv", 'w',  "UTF-8")     
    pulls_conversation_details_all_raw = codecs.open("pulls_conversation_details_all_raw.tsv", 'w',  "UTF-8")     

    fnames = ["pulls_conversation_urls_open.tsv" ,"pulls_conversation_urls_closed.tsv" ]  
    for fname in fnames:
        with codecs.open(fname, 'r',  "UTF-8") as fin:
            for line in fin:
                main_url = line.strip().split("\t")[2].strip()
                issue_id = line.strip().split("\t")[0].strip()
                url = main_url + '?access_token={0}'.format( github_token)
                data = getPagedRequest(url)
                for comment in data:
                    try:
                        comment_id = comment["id"]
                        comment_url = comment["url"]
                        comment_user = comment["user"]["login"]
                        text = comment["body"]
                        comment_text = text_cleanup(text)
                        created_at = comment["created_at"]
                        
                        pulls_conversation_details_all.write( str(issue_id)+"\t"  +str(comment_id)+"\t"  + str(created_at) +"\t"+str(comment_url)+"\t"+ str(comment_user)+"\t" + str(comment_text) +"\n")

                        comment_dict = {}
                        comment_dict["comment_meta"] = str(issue_id)+"\t"  +str(comment_id)+"\t"  + str(created_at) +"\t"+str(comment_url)+"\t"+ str(comment_user)
                        comment_dict["comment_text"] = text
                                
                        pulls_conversation_details_all_raw.write(json.dumps(comment_dict))
                        pulls_conversation_details_all_raw.write("\n")                     
                    except Exception, e: 
                        #print "Error : ", e 
                        pass
    pulls_conversation_details_all.close()
    pulls_conversation_details_all_raw.close()

    

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

    #"""
    #get issue details and the conversation urls
    #"""
    #getIssuesList(main_url,"open")
    #getIssuesList(main_url,'closed')

    #"""
    #get individual comments of each conversation of each issue
    #"""    
    #getIssuesConversations(main_url)

    
    """
    get pull details and the conversation urls
    """
    #getPullsList(main_url,"open")
    #getPullsList(main_url,'closed')

    """
    get individual comments of each conversation of each pull request
    """    
    getPullsConversations(main_url)
    

    #testtext = "heloworld. \r\n what! is this @pmatta \n /*this is the*/ hello\n and http://github.com this is world\n "
    #print text_cleanup(testtext)
    #test()
