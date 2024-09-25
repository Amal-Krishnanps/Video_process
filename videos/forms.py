from django import forms
from .models import Video

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']

    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')
        if not video_file.name.endswith(('.mp4', '.mkv','.avi','.mov')):
            raise forms.ValidationError("Only MP4 and MKV files are allowed.")
        return video_file