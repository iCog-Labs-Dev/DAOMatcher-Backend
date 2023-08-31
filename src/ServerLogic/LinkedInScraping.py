import requests
import os
import urllib.parse
import json

#Loaing api key from environment file
api_key = os.getenv("LIX_API_KEY")
payload={}
headers = {
  'Authorization': api_key
}

def handleException(response:requests.Response):
  if response.ok:
    return json.loads(response.text)
  else:
    print(response.text)
    error = json.loads(response.text)
    raise Exception(f"Lix Error: {error['error']['message']}")

#Used to get user information displayed on the profile page of the user
def getBasicUserInfo(username):
  
  url = f"https://api.lix-it.com/v1/person?profile_link=https://linkedin.com/in/{username}"

  response = requests.request("GET", url, headers=headers, data=payload)
  userInfo = handleException(response)
  return userInfo
    
  

#Get user Connections
def getUserConnections(username, count):
  url = f"https://api.lix-it.com/v1/connections?count={count}&start=0&viewer_id={username}"
  response = requests.request("GET", url, headers=headers, data=payload)
  userConns = handleException(response)
  return userConns

#Supposed to fetch email address but doesn't work as expected
def getEmailAddress(username):
  url = f"https://api.lix-it.com/v1/contact/email/by-linkedin?url=https://linkedin.com/in/{username}"
  
  response = requests.request("GET", url, headers=headers, data=payload)
  userEmails = handleException(response)
  return userEmails

def getPostsByUser(userInfo):
  
  #Extracting user sales navigation link given the user information json
  salesNavLink:str = userInfo["salesNavLink"]
  salesNavLink = salesNavLink.split("lead")[1]
  
  #Sales navigation Id is used by linkedIn to identify posts made by a user
  salesNavigationID = salesNavLink.split("/")[-1].split(",")[0]
  
  postUrl = f'https://www.linkedin.com/search/results/content/?fromMember={salesNavigationID}&origin=SWITCH_SEARCH_VERTICAL&sid=G;z'
  postUrl = urllib.parse.quote(postUrl, safe='')
  
  url = f"https://api.lix-it.com/v1/li/linkedin/search/posts?url={postUrl}"
  
  # print(postUrl) #Uncomment this for debugging
  print(url) #Uncomment this for debugging
  
  response = requests.request("GET", url, headers=headers, data=payload)
  userPosts = handleException(response)
  return userPosts



