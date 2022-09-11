# doing necessary imports
#import threading
import io
import os
#from logger_class import getLog
from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from flask_cors import CORS, cross_origin
#import pandas as pd
from MongoOperations import MongoDBManagement
from YouTubeScrapping import YouTubeScrapper
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from flask_sqlalchemy import SQLAlchemy
import requests
#rows = {}
#collection_name = from models import *
#logger = getLog('flipkrat.py')

free_status = True
#db_name = 'Flipkart-Scrapper'

app = Flask(__name__)  # initialising the flask app with the name 'app'
app.config.from_object(os.getenv('APP_SETTINGS',"config.DevelopmentConfig"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from models import *
from SqlOperations import Sql_Operations
#For selenium driver implementation on heroku
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")


#To avoid the time out issue on heroku


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        global free_status
        ## To maintain the internal server issue on heroku
        if free_status != True:
            return "This website is executing some process. Kindly try after some time..."
        else:
            free_status = True
        searchString =request.form['link']   # obtaining the search string entered in the form
        expected_video=int(request.form['count'])
        print(searchString)
        try:
           
            main_scrapper_object = YouTubeScrapper(executable_path=ChromeDriverManager().install(),
                                               chrome_options=chrome_options)
           # mongoClient = MongoDBManagement(username='Kavita', password='kavita1610')
            main_scrapper_object.openUrl(searchString,flag=True)
            #logger.info("Url hitted")
            main_scrapper_object.wait()
            thumbnails,video_links=main_scrapper_object.scrollMainPage(expected_video)
            channel_name=main_scrapper_object.getChannel()
            encoded_thumbnails=main_scrapper_object.encodeToBase64(thumbnails)
            final_comments=[]
            final_commenters=[]
            likes=[]
            total_comments=[]
            titles=[]
            gdrive=[]
            gdrive_id=""
            num_rows_deleted = db.session.query(Data).delete()
            db.session.commit() 
            mongoClient = MongoDBManagement(username='ragavan', password='ramanan')
            main_scrapper_object.refreshToken()
            ACCESS_TOKEN=main_scrapper_object.getToken()
            mongoClient.freeCollection(db_name="youtube",collection_name="data")
            f=open("./ids.txt","r")
            file_val=f.readlines()
            id_list=file_val[0]
            ids=id_list.split(" ")
            headers = {"Authorization": "Bearer "+ACCESS_TOKEN}  
            for h in range(0,len(ids)-1):
              t = requests.delete(
         "https://www.googleapis.com/drive/v3/files/"+ids[h],
           headers=headers
            )
            for i,video in enumerate(video_links[:expected_video]):
                new_scrapper_object=YouTubeScrapper(executable_path=ChromeDriverManager().install(),
                                               chrome_options=chrome_options)
                new_scrapper_object.openUrl(video,flag=False)
                print("Url Opened")
                new_scrapper_object.wait()
                titles.append(new_scrapper_object.getTitle())
                print("Got Title")
                new_scrapper_object.wait()
                likes.append(new_scrapper_object.getLikes())
                print("Got Likes")
                new_scrapper_object.scrollNewPage()
                new_scrapper_object.wait()
                total_comments.append(new_scrapper_object.getTotalComments())
                print("Got total comments")
                final_comments.append(new_scrapper_object.getComments())
                print("Got  comments")
                final_commenters.append(new_scrapper_object.getCommenters())
                print("Got commenters")
                file_name=new_scrapper_object.downloadVideo(video,i)
                link,g_id=new_scrapper_object.getGdriveLink(file_name,i)
                print("Got drive link")
                new_scrapper_object.deleteVideo(file_name)
                gdrive.append(link)
                gdrive_id=g_id+" "+gdrive_id
                   
                sql_object=Sql_Operations(channel_name,titles[i],video,gdrive[i],thumbnails[i],likes[i],total_comments[i])
                result=sql_object.add_Values()
                db.session.add(result)
                db.session.commit()
        
                for ind,c in enumerate(final_comments[i]):
                       result = {
                                  'channel_name':channel_name,
                                  'title':titles[i],
                                  'comments':final_comments[i][ind],
                                  'commenter':final_commenters[i][ind],
                                  'thumbnail':encoded_thumbnails[i]
                                }
                       mongoClient.insertRecord(db_name="youtube",collection_name="data",record=result)
                new_scrapper_object.closeConnection() 
           
            with open("./ids.txt","w")as ids:
             ids.write(gdrive_id)
                    
            records = mongoClient.findAllRecords(db_name="youtube",collection_name="data")
            results = db.session.query(Data).filter_by(channel_name=channel_name).all()   
            return render_template('results.html', rows=results,results=records)     
           
                  
        except Exception as e:
            raise Exception("(app.py) - Something went wrong while rendering all the details of videos.\n" + str(e))
    else:
            return render_template('index.html')

        
if __name__ == "__main__":
    app.run()  # running the app on the local machine on port 8000
