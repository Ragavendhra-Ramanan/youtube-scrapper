class ObjectRepository:

    def __init__(self):
        print()

    def getVideoLinks(self):
        video_tag= "yt-simple-endpoint.style-scope.ytd-grid-video-renderer"
        return video_tag

    def getVideoTitle(self):
        title_tag = "yt-formatted-string"
        title_class= "style-scope ytd-video-primary-info-renderer"
        return title_tag,title_class

    def getVideoLikes(self):
        likes_tag = "yt-formatted-string"
        likes_class= "style-scope ytd-toggle-button-renderer style-text"
        return likes_tag,likes_class

    def getVideoTotalComments(self):
        comments_total_tag = "yt-formatted-string"
        comments_total_class = "count-text style-scope ytd-comments-header-renderer"
        return comments_total_tag,comments_total_class

    def getVideoCommenters(self):
        commenter_tag = "a"
        commenter_id  = "author-text"
        return commenter_tag,commenter_id

    def getVideoComments(self):
        comment_tag = "yt-formatted-string"
        comment_id  = "content-text"
        return comment_tag,comment_id

    def getVideoThumbnail(self):
        thumbnail_tag = "yt-img-shadow"
        thumbnail_class= "style-scope ytd-thumbnail no-transition"
        return thumbnail_tag,thumbnail_class

    def getChannelName(self):
        name_tag = "yt-formatted-string"
        name_class="style-scope ytd-channel-name"
        return name_tag,name_class

    
