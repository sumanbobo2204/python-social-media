# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 21:14:38 2019

@author: Suman
"""

import requests
import json
import random
import sys
import facebook as fb

token = $FBTOKEN


# Though commenting and liking to the feed in user timeline is prohibited currently
# One can automate the like and comment to a post in any FB page via page access token
def posting_to_fb(feed_id=None,message=None):
    """
    posting message to feed and liking the feed::
        
    """
    graph = fb.GraphAPI(token)
    profile = graph.get_object(feed_id.split('_')[0])
    posts = graph.get_connections(profile['id'], 'posts')
    for post in posts['data']:
        graph.put_object(post['id'],'likes')
        r = graph.put_comment(post['id'],message=message)
    #fb_feed_post_uri = 'https://graph.facebook.com/' + feed_id + '/comments?access_token=' + token + '&message=' +message
    #fb_feed_like_uri = 'https://graph.facebook.com/' + feed_id + '/likes?access_token=' + token
    # posting to feed
    print(r)
    # liking the feed


def get_feeds_response_from_fb(uri=None, counter=0):
    """
    getting feeds from facebook graph api ::
        
    """
    #print(sys.path)
    random_text = ['Hi', 'Hello', 'How are you!!']
    
    # facebook gives 25 feeds at a time ::
    flag = True
    if counter == 0:
        fb_feed_uri = 'https://graph.facebook.com/me/feed?access_token=' +token
        uri = fb_feed_uri
            
    # iterating the facebook feeds ::
    if flag:
        try:          
            result = json.loads((requests.get(uri)).text)
            for data in result['data']:
                #print(data)
                if 'message' in data:
                    feed_id = data['id']
                    # need to send reply to this ::
                    # 1. getting random comment ::
                    comment = '(Python_FB_Automate :: (#TEST::#DEBUG)) -->' +random.choice(random_text)
                    print(feed_id)
                    print('Retrieved message from FB post :: {m}'.format(m=data['message']))
                    print('posting comment ::' +comment)
                    #posting_to_fb(feed_id,comment)
                else:
                    flag = False
            counter += 1
        except ConnectionError as ex:
            print("Connection Error :: {e} ".format(e=str(ex)), file=sys.stderr)
        
    # getting the uri for the next set of results ::
    if 'paging' in result and 'next' in result['paging']:
        fb_feed_uri = result['paging']['next']
        get_feeds_response_from_fb(fb_feed_uri,counter)
        #print(fb_feed_uri)


# Execute the main:: 
if __name__ == '__main__':
    get_feeds_response_from_fb()

    
    

