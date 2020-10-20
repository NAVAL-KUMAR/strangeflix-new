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
    subtitle = models.TextField()
    premium = models.BooleanField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField(max_length=300)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)

    def date_preety(self):
        return self.datetime.strftime('%b %e %Y')

class Like(models.Model):
    like = models.IntegerField(default=0)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Favourite(models.Model):
    favourite = models.BooleanField(default=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class History(models.Model):
    pause_time  =  models.FloatField(default=0)
    dateTime = models.DateTimeField(auto_now=True, blank=False, null=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Tag(models.Model):
    title=models.CharField(max_length=25)
    video=models.ForeignKey(Video,on_delete=models.CASCADE)

    def __str__(self):
        return self.title+str("/")+str(self.video)

class Flag(models.Model):
    video=models.ForeignKey(Video,on_delete=models.CASCADE,blank=True,null=True)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,blank=True,null=True)
    user=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    reason=models.TextField(max_length=100)
    date=models.DateTimeField()
    user_response=models.BooleanField()
    name=models.CharField(max_length=50)

    def __str__(self):
        return str(self.user)+str('/')+str(self.video)
