from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Subtitle(models.Model):
    video = models.ForeignKey(Video, related_name='subtitles', on_delete=models.CASCADE)
    language = models.CharField(max_length=50) 
    subtitle_file = models.FileField(upload_to='subtitles/')  
    content = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.language} subtitles for {self.video.title}"
