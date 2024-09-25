
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings  
from .models import Video, Subtitle
from .forms import VideoUploadForm
from django.db.models import Q
import subprocess
import os,re



def process_video(video_path, video_instance):
    
    output = subprocess.check_output(
        ['ffprobe', '-i', video_path, '-show_streams', '-select_streams', 's'],text=True)
    lines = output.splitlines()
    
    # print ('\noutput')
    # print (output)
            
    subtitle_languages =[]
    
    for match in re.finditer(r"TAG:language=(\w+)", output):
        language = match.group(1)
        subtitle_languages.append(language)
        
    print ('lan:', subtitle_languages)
    

    
    for lang in subtitle_languages:
        subtitle_file = f"subtitles_{lang}.srt"
        try:
            process = subprocess.Popen(
            ["ffmpeg", "-loglevel", "debug", "-i", video_path, "-vn", "-c:a", "copy", "-filter:a", f"subtitles=file={subtitle_file}:subtitle_lang={lang}", subtitle_file],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            for line in iter(process.stderr.readline, b''):
                print(line.decode(), end='')

            process.stderr.close()
            process.wait()

            if process.returncode == 0:
                with open(subtitle_file, 'r') as file:
                    subtitle_content = file.read()
                    Subtitle.objects.create(
                    video=video_instance,
                    language=lang,
                    subtitle_file=subtitle_file,
                    content=subtitle_content
            )
        except Exception as e:
            print(f"Error processing subtitles for language {lang}: {e}")





def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            print('Video uploaded')
            

            process_video(video.video_file.path, video)
            print("Video Processing Success'")
            
            ##### mkv files not playing in browser
            converted_path = convert_to_mp4(video.video_file.path)
            if converted_path and converted_path != video.video_file.path:
                video.video_file.name = os.path.relpath(converted_path, start=settings.MEDIA_ROOT)
                video.save()
                
            return redirect('video_list')
                
    else:
        form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})




def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})


def video_detail(request, id):
    video = get_object_or_404(Video, id=id)
    subtitles = video.subtitles.all()
    return render(request, 'video_detail.html', {'video': video,'subtitles': subtitles})



def search_subtitles(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        subtitles = Subtitle.objects.filter(content__icontains=query)

        for subtitle in subtitles:
            if isinstance(subtitle.content, str):
                timestamp = get_timestamp(subtitle.content, query)
                results.append({
                    'video_id': subtitle.video.id,
                    'video_title': subtitle.video.title,
                    'language': subtitle.language,
                    'content': subtitle.content,
                    'timestamp':timestamp
            })
    return render(request, 'search.html', {'results': results, 'query': query})



def get_timestamp(subtitle_content, query):
    if not isinstance(subtitle_content, str):
        return None
    
    lines = subtitle_content.splitlines()
    
    for line in lines:
        if query.lower() in line.lower():
            pattern = r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})'
            match = re.search(pattern, line)
            if match:
                start_time = match.group(1)  
                return start_time.split(',')[0]
                
    return None




def convert_to_mp4(video_path):
    """
    Converts the uploaded video file to mp4 format if it is not in mp4 format.
    """
    base, ext = os.path.splitext(video_path)
    if ext.lower() == '.mp4':
        return video_path  # No need to convert


    output_path = f"{base}.mp4"
    command = ['ffmpeg', '-i', video_path, '-codec', 'copy', output_path]

    try:
        subprocess.run(command, check=True)
        return output_path
    except subprocess.CalledProcessError:
        return None