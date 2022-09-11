
from models import *

class Sql_Operations:
  def __init__(self, channel_name,title, video_link,gdrive_link,thumbnail_link,likes,comments,):
        """
        This function sets the required url
        """
        try:
           self.channel_name=channel_name
           self.title = title
           self.video_link = video_link
           self.gdrive_link = gdrive_link
           self.thumbnail_link= thumbnail_link
           self.likes=likes
           self.total_comments=comments
        
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initiation process\n" + str(e))
  def add_Values(self):
    """
    Adds to the database
    """
    result=Data(
                   channel_name=self.channel_name,
                   title = self.title,
                   video_link = self.video_link,
                   gdrive_link = self.gdrive_link,
                   thumbnail_link = self.thumbnail_link,
                   likes = self.likes,
                   total_comments = self.total_comments
                
                )
    return result
    

