import random
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import base64
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from RepositoryForObject import ObjectRepository
from selenium.webdriver.common.by import By
#import pandas as pd
import httplib2
from oauth2client import GOOGLE_REVOKE_URI, GOOGLE_TOKEN_URI, client
import json
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
#from mongoDBOperations import MongoDBManagement
from youtube_dl import YoutubeDL
import os

class YouTubeScrapper:

    def __init__(self, executable_path, chrome_options):
        """
        This function initializes the web browser driver,BeautifulSoup
        :param executable_path: executable path of chrome driver.
        """
        try:
            self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
            html=self.driver.page_source
            self. soup = BeautifulSoup(html, "html.parser")
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initializing the webdriver object.\n" + str(e))

   
    def getLocatorsObject(self):
        """
        This function initializes the Locator object and returns the locator object
        """
        try:
            locators = ObjectRepository()
            return locators
        except Exception as e:
            raise Exception(f"(getLocatorsObject) - Could not find locators\n" + str(e))

    def findElementByClass(self,class_name):
        """
        This function finds element by class name
        """
        try:
            element = self.driver.find_elements(By.CLASS_NAME,class_name)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByClass) - ClassPath provided was not found.\n" + str(e))

    def findElementByTagClass(self,tag_name,class_name):
        """
        This function finds web element using Classpath provided
        """
        try:
            element = self.soup.find(tag_name,{"class":class_name})
            
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByTagClass) - ClassPath provided was not found.\n" + str(e))
    
    def findAllElementByTagClass(self,tag_name,class_name):
        """
        This function finds web element using Classpath provided
        """
        try:
            element = self.soup.find_all(tag_name,{"class":class_name})
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByTagClass) - ClassPath provided was not found.\n" + str(e))

    def findAllElementByTagId(self, tag_name,id_name):
        """
        This function finds web element using tag_name provided
        """
        try:
            element = self.soup.find_all(tag_name,{"id":id_name})
            return element
        except Exception as e:
            raise Exception(f"(findElementByTag) - TagPath provided was not found.\n" + str(e))

       
    def openUrl(self, url,flag):
        """
        This function open the particular url passed.
        :param url: URL to be opened.
        """
        try:
            if self.driver and flag:
                self.driver.get(url+"/videos")
                return True
            elif self.driver and (flag==False):
                self.driver.get(url)
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(openUrl) - Something went wrong on opening the url {url}.\n" + str(e))



    def getTitle(self):
        """
        This function helps to retrieve title of the video.
        """
        try:
            locator = self.getLocatorsObject()
            tag_name,class_name = locator.getVideoTitle()
            self.waitExplicitlyForCondition(class_name)
            title = self.findElementByTagClass(tag_name=tag_name,class_name=class_name).text
            
            return title
        except Exception as e:
            raise Exception(f"(title) - Not able to get the title.\n" + str(e))
            
    def getVideoUrls(self):
        """
        This function helps to retrieve url of the videos.
        """
        try:
            locator = self.getLocatorsObject()
            class_name = locator.getVideoLinks()
            links = self.findElementByClass(class_name=class_name)
            final_links=[]
            for link in links:
                 final_links.append(link.get_attribute("href"))
            return final_links
        except Exception as e:
            raise Exception(f"(final links) - Not able to get the links.\n" + str(e))
            
    def getLikes(self):
        """
        This function helps to retrieve likes of the video.
        """
        try:
            locator = self.getLocatorsObject()
            tag_name,class_name = locator.getVideoLikes()
            self.waitExplicitlyForCondition(class_name)
            likes = self.findElementByTagClass(tag_name=tag_name,class_name=class_name).text
            
            return likes
        except Exception as e:
            raise Exception(f"(likes) - Not able to get the likes.\n" + str(e))
     
    def getTotalComments(self):
        """
        This function helps to retrieve total comments of the video.
        """
        try:
            
            locator = self.getLocatorsObject()
            tag_name,class_name = locator.getVideoTotalComments()
            self.waitExplicitlyForCondition(class_name)
            self.wait()
            total_comments = self.findElementByTagClass(tag_name=tag_name,class_name=class_name).span.text
            
            return total_comments
        except Exception as e:
            raise Exception(f"(total_comments) - Not able to get the total_comments.\n" + str(e))

    def getChannel(self):
        """
        This function helps to retrieve channel name of the video.
        """
        try:
            locator = self.getLocatorsObject()
            tag_name,class_name = locator.getChannelName()
            channel = self.findElementByTagClass(tag_name=tag_name,class_name=class_name).text
           
            return channel
        except Exception as e:
            raise Exception(f"(channel) - Not able to get the channel.\n" + str(e))
      
    def getThumbnails(self):
        """
        This function helps to retrieve thumbnail of the video.
        """
        try:
            locator = self.getLocatorsObject()
            tag_name,class_name = locator.getVideoThumbnail()
            self.waitExplicitlyForCondition(class_name)
            thumbnails = self.findAllElementByTagClass(tag_name=tag_name,class_name=class_name)
            
            final_thumbnail=[]
            for thumbnail in thumbnails[1:]:
                final_thumbnail.append(thumbnail.img['src'])
           
            return final_thumbnail
        except Exception as e:
            raise Exception(f"(thumbnails) - Not able to get the thumbnails.\n" + str(e))
    
    def getComments(self):
        """
        This function helps to retrieve comments of the video.
        """
        try:
            locator = self.getLocatorsObject()
            tag_name,id_name = locator.getVideoComments()
            self.wait()
            comments = self.findAllElementByTagId(tag_name=tag_name,id_name=id_name)
            final_comments=[]
            for comment in comments:
                final_comments.append(comment.text)
            return final_comments
        except Exception as e:
            raise Exception(f"(comments) - Not able to get the comments.\n" + str(e))
      
    def getCommenters(self):
        """
        This function helps to retrieve comments of the video.
        """
        try:
            locator = self.getLocatorsObject()
            tag_name,id_name = locator.getVideoCommenters()
            self.wait()
            commenters = self.findAllElementByTagId(tag_name=tag_name,id_name=id_name)
            final_commenters=[]
            for commenter in commenters:
                final_commenters.append(commenter.span.text.strip())
            return final_commenters
        except Exception as e:
            raise Exception(f"(commenters) - Not able to get the commenters.\n" + str(e)) 
    
    def scroll_to_end(self):
      """
      Scrolls the page normally to height
      """ 
      self.driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight );")
      
    def waitExplicitlyForCondition(self, element_to_be_found):
        """
        This function explicitly for condition to satisfy
        """
        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
            WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, element_to_be_found)))
            return True
        except Exception as e:
            return False
    def wait(self):
        """
        This function waits for the given time
        """
        try:
            self.driver.implicitly_wait(5)
            html = self.driver.page_source
            self. soup = BeautifulSoup(html, "html.parser")
        except Exception as e:
            raise Exception(f"(wait) - Something went wrong.\n" + str(e))

    
      
            
    def scrollMainPage(self,max_links_to_fetch):
           """
           Scroll main page
           """  
           self.wait()
           thumbnail_count = 0
           results_start = 0
           while thumbnail_count < max_links_to_fetch:
                  html=self.driver.page_source
                  self. soup = BeautifulSoup(html, "html.parser")
                  thumbnails=self.getThumbnails()
                  number_results=len(thumbnails)
                  print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
                  thumbnail_count =number_results
                  if thumbnail_count >= max_links_to_fetch:
                      print(f"Found:{number_results}")
                      break
             
                  print("Found:", thumbnail_count, "image links, looking for more ...")
                  self.scroll_to_end()
                  self.wait()
           video_links =self.getVideoUrls(); 
           return thumbnails[:max_links_to_fetch],video_links[:max_links_to_fetch]
    
    def encodeToBase64(self,thumbnails):
       """
       This function is used to convert images to base64 format
       """
       try:
          encodings=[]
          for img in thumbnails: 
                  my_string = base64.b64encode(requests.get(img).content)
                  encodings.append(my_string)
          return encodings
       
       except Exception as e:
            raise Exception(f"(encodeToBase64 ) - Something went wrong on encoding base 64.\n" + str(e))
    
    def scrollNewPage(self):
        """
        Scrolls down the video page
        """
       
        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        while True:
              self.driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight );")
              self.wait()
              new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
              if new_height == last_height: 
                 break
              last_height = new_height
              self.wait()
        self.wait()
    
    def downloadVideo(self,video,i):
     """
     This method is used to download the video
     """
     try:
        file_name='file_name{}.mp4'.format(i)
        ydl_opts = {'outtmpl': file_name}
        with YoutubeDL(ydl_opts) as ydl:
             ydl.download([video])
        return file_name
     except Exception as e:
            raise Exception(f"(downloadVideo) - Something went wrong on download video.\n" + str(e))
    
    def deleteVideo(self,file_name):
     """
     This is used to download video
     """        
     try:
        
        os.remove(file_name)
     except Exception as e:
            raise Exception(f"(deleteVideo) - Something went wrong on delete video.\n" + str(e))
    
    def refreshToken(self):
           """
           refresh token
           """
           f = open('./credentials.json')
           data = json.load(f)  
           CLIENT_ID = data['client_id']
           CLIENT_SECRET = data['client_secret']
           REFRESH_TOKEN =data['refresh_token']
          
           credentials = client.OAuth2Credentials(
               access_token=None,  # set access_token to None since we use a refresh token
               client_id=CLIENT_ID,
               client_secret=CLIENT_SECRET,
               refresh_token=REFRESH_TOKEN,
               token_expiry=None,
               token_uri=GOOGLE_TOKEN_URI,
               user_agent=None,
               revoke_uri=GOOGLE_REVOKE_URI)
           credentials.refresh(httplib2.Http())  # refresh the access token (optional)
           data=credentials.to_json()
           with open("./credentials.json","w") as files:
                files.write(data)
           
    def getToken(self):
           """
           Get access token
           """
           f = open('./credentials.json')
           data = json.load(f)   
           ACCESS_TOKEN=data['access_token']
           return ACCESS_TOKEN
            
    def getGdriveLink(self,file_name,i):
     """
     This function get gdrive links of video
     """ 
     try:
           self.refreshToken()
           ACCESS_TOKEN=self.getToken()
           
           
           # Bearer (Enter the token)
           headers = {"Authorization": "Bearer "+ACCESS_TOKEN}  
           para = {
              "name": "videos_{}.mp4".format(i),   # enter file name to be created
               "parents": ["1kf__uKLzmPX3tQxNcsqcAYvWSIbJ9Ss4"]  #enter id of folder where u want to upload the file
              }
           files = {
             'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
            'file': open(file_name, "rb")  #file to be uploaded
               }
           r = requests.post(
               "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                headers=headers,
               files=files
              )
           with open("./fileid.json","w")as ids:
             ids.write(r.text)
           f=open("./fileid.json","r")
           file_val=json.load(f)
           glink="https://drive.google.com/file/d/"+file_val["id"]+"/view?usp=sharing"
           return glink,file_val["id"]
     except Exception as e:
            raise Exception(f"(getdrivelink) - Something went wrong on get drive link.\n" + str(e))
            
    def closeConnection(self):
        """
        This function closes the connection
        """
        try:
            self.driver.close()
        except Exception as e:
            raise Exception(f"(closeConnection) - Something went wrong on closing connection.\n" + str(e))
        
