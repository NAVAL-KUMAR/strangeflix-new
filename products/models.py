from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    upload_date = models.DateTimeField()
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    filename = models.FileField(upload_to='', blank=True)
    thumbtail = models.ImageField(upload_to='', blank=True)
    link = models.URLField(max_length=200, blank=True)
    subtitle = models.FileField(upload_to='', blank=True)
    premium = models.BooleanField(default=False)

    class Meta:
        ordering = ('-upload_date',)

    def __str__(self):
        return self.title
    def date_prety(self):
        return self.datetime.strftime('%d-%m-%Y %H:%M:%S')

class Comment(models.Model):
    name = models.CharField(max_length = 50)
    text = models.TextField(max_length=300)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)

    def date_prety(self):
        return self.datetime.strftime('%d-%m-%Y %H:%M:%S')

class Like(models.Model):
    like = models.IntegerField(default=0)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Favourite(models.Model):
    favourite = models.BooleanField(default = False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class History(models.Model):
    pause_time  =  models.FloatField(default=0)
    duration_time = models.FloatField(default=0)
    dateTime = models.DateTimeField(auto_now=True, blank=False, null=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def date_prety(self):
        return self.dateTime.strftime('%d-%m-%Y %H:%M:%S')

class Tag(models.Model):
    title=models.CharField(max_length=25)
    video=models.ForeignKey(Video,on_delete=models.CASCADE)

    def __str__(self):
        return self.title+str("/")+str(self.video)

class Flag(models.Model):
    video=models.ForeignKey(Video,on_delete=models.CASCADE)
    user=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    reason=models.TextField(max_length=100)
    date=models.DateTimeField()
    user_response=models.BooleanField()
    name=models.CharField(max_length=50)

    def __str__(self):
        return str(self.user)+str('/')+str(self.video)

    def date_prety(self):
        return self.date.strftime('%d-%m-%Y %H:%M:%S')

class Playlist(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=300, null=True,blank=True)
    thumbtail = models.ImageField(upload_to='', blank=True)
    upload_date = models.DateTimeField(auto_now=True, blank=False, null=False)

    def __str__(self):
        return str(self.title)

class playlist_video(models.Model):
    name = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    video=models.ForeignKey(Video,on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    def date_prety(self):
        return self.datetime.strftime('%d-%m-%Y %H:%M:%S')

class payPerView(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    status = models.CharField(max_length=20)
    type = models.CharField(max_length=10)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + str("/") + str(self.enddate) + str('/') + self.status


class UserNotification(models.Model):
    video=models.ForeignKey(Video,on_delete=models.CASCADE,blank=True, null=True,)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,blank=True, null=True)
    description=models.TextField(max_length=500,null=True,blank=True)
    user=models.ForeignKey('auth.User',on_delete=models.CASCADE,null=True,blank=True)
    type=models.CharField(max_length=10)
    date=models.DateTimeField()