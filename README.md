# youtube-scrapper
Youtube Scrapping using selenium and beautiful soup without youtube API 

#Description
1.If Url of a Youtube Channel and number of videos to fetch is given we can get
    * Latest top number of videos mentioned with
          * Channel Name
          * Video link
          * Title of the video
          * Likes of the video
          * Total comments of the video
          * Comments of the video
          * Commenters of the video
          * Thumbnails of the video
          * Thumbnail converted to base64
          * Gdrive Link of the video (Video downloaded and uploaded to google drive)
          
  

# Stacks Used
Python 3.10.4
SqlAlchemy -Postgresql
MongoDB
Flask

# How to run the file
1. Clone the repository
2. pip install -r  requirements.txt
3. flask run

# Files and Folders
1. templates              = contains basic html files
2. app.py                 = starter file for flask app
3. config.py              = configure environmental variables
4. credentails.json       = contains secret tokens to access google drive via google drive api
5. fileid.json            = used to get id of the file uploaded in the gdrive.
6. ids.txt                = contains all the file ids of uploaded videos in gdrive
7. manage.py              = It is used for migarting sql database
8. models.py              = It is used for creating database entity
9. MongoOperations.py     = Contains code to interact with mongodb
10.Procfile               = For hosting in heroku
11.RepositoryForObject.py = Contains tags to fetch for scraping youtube
12.requirements.tx        = necessary installations
13.SqlOperations.py       = Contains SqlOperations.
14.YoutubeScrapping.py    = To Interact with Youtube
