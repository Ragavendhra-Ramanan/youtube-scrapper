from app import db
from sqlalchemy.dialects.postgresql import JSON


class Data(db.Model):
    __tablename__ = 'data_s'

    id = db.Column(db.Integer, primary_key=True)
    channel_name=db.Column(db.String())
    title = db.Column(db.String())
    video_link = db.Column(db.String())
    gdrive_link = db.Column(db.String())
    thumbnail_link = db.Column(db.String())
    likes = db.Column(db.String())
    total_comments = db.Column(db.String())

    def __init__(self, channel_name,title, video_link,gdrive_link,thumbnail_link,likes,total_comments):
        self.channel_name=channel_name
        self.title = title
        self.video_link = video_link
        self.gdrive_link = gdrive_link
        self.thumbnail_link= thumbnail_link
        self.likes=likes
        self.total_comments=total_comments
        
    def __repr__(self):
        return '<id {}>'.format(self.id)
