# Code for finding clusters of users based on activity. Currently not using this. 
#
def get_model(all_contributor_metrics,metric_name, metric_list, metric_place):
    """ Finding 4 groups using k_means clustering algorithm"""
    print " Model: ", metric_name
    model_file = codecs.open("model_"+metric_name+".tsv", 'w',  "UTF-8") 
    try:
        status, final_centroids, final_clusters = github_kmeans.find_centroids_clusters(metric_list,4)
        if status == "error":
            print "Error in: ",metric_name
        else:
            centroids_clusters = sorted(zip(final_centroids, final_clusters))        
            for user,metrics in all_contributor_metrics.items():
                for num, cluster in enumerate(centroids_clusters):
                    metric_val = int(metrics[metric_place])            
                    if int(metric_val) in cluster[1]:
                        if num==0:
                            model_file.write(user+ "\t"+ str(metric_val)+"\t"+ "low")
                        elif num==1:
                            model_file.write(user+ "\t"+  str(metric_val)+ "\t"+ "medium")
                        elif num==2:
                            model_file.write(user+ "\t"+  str(metric_val)+ "\t"+ "high")
                        elif num==3:
                            model_file.write(user+  "\t"+ str(metric_val)+ "\t"+ "very_high")  

                        model_file.write("\n")
    except Exception, e:        
        print "Error in: ",metric_name
        print  e      
    model_file.close()


def print_classifier_group_model():
    # print out the 5 activity classification groups value for each user
    all_contributor_metrics = {}
    list_commit_cnt = []
    list_commit_add_del = []
    list_issue_open_close = []
    list_issue_comment_cnt = []
    list_pull_open_close = []

    with codecs.open("user_activity_metric.tsv", 'r',  "UTF-8") as fin:
        fin.readline() #ignore first line
        for line in fin:
            line_split = line.strip().split("\t")
            
            commit_cnt = int(line_split[1])
            list_commit_cnt.append(commit_cnt)
            
            commit_add_del= int(line_split[2]) + int(line_split[3])
            list_commit_add_del.append(commit_add_del)
            
            issue_open_close = int(line_split[4]) + int(line_split[5])
            list_issue_open_close.append(issue_open_close)
            
            issue_comment_cnt = int(line_split[6])
            list_issue_comment_cnt.append(issue_comment_cnt)
            
            pull_open_close = int(line_split[7]) + int(line_split[8])
            list_pull_open_close.append(pull_open_close)
            all_contributor_metrics[line_split[0]] = [commit_cnt,commit_add_del,issue_open_close,issue_comment_cnt,pull_open_close]
            

    #print  list_commit_cnt,list_commit_add_del, list_issue_open_close , list_issue_comment_cnt , list_pull_open_close 

    #intially thought of using median, but later used k-means which is better for getting groups
    #midpt = len(list_commit_cnt)/2
    #median_commit_cnt = sorted(list_commit_cnt)[midpt]
    #median_commit_add_del = sorted(list_commit_add_del)[midpt]
    #median_issue_open_close = sorted(list_issue_open_close)[midpt]
    #median_issue_comment_cnt = sorted(list_issue_comment_cnt)[midpt]
    #median_pull_open_close = sorted(list_pull_open_close)[midpt]
    
    print  all_contributor_metrics
    get_model(all_contributor_metrics,"commit_cnt", list_commit_cnt, 0)
    get_model(all_contributor_metrics,"commit_add_del", list_commit_add_del, 1)
    get_model(all_contributor_metrics,"issue_open_close", list_issue_open_close, 2)
    get_model(all_contributor_metrics,"issue_comment_cnt", list_issue_comment_cnt, 3)
    get_model(all_contributor_metrics,"pull_open_close", list_pull_open_close, 4)

    #for classifier_grp in [list_commit_cnt,list_commit_add_del, list_issue_open_close , list_issue_comment_cnt , list_pull_open_close ]:
        #try:
            #centroids_clusters = github_kmeans.find_centroids_clusters(classifier_grp,4)
            #for centroidpt, finalcluster in centroids_clusters:
                    #print "Centroid: %s" % centroidpt
                    #print "Cluster contents: %r" % finalcluster 
        #except Exception, e:        
                #print "Error in: ",classifier_grp
                #print  e  
