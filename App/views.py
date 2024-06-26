from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, HttpResponse
from . import forms
from pytube import YouTube
import io

def index(request):
    form = forms.YouTubeForm()
    return render(request, 'index.html', {'form': form})

def stream_video(stream):
    buffer = io.BytesIO()
    stream.stream_to_buffer(buffer)
    buffer.seek(0)
    while True:
        data = buffer.read(2 * 1024 * 1024)  # Read in 2MB chunks
        if not data:
            break
        yield data

def download(request):
    if request.method == 'POST':
        form = forms.YouTubeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                yt = YouTube(url)
                stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
                return StreamingHttpResponse(
                    stream_video(stream),
                    content_type='video/mp4',
                    headers={'Content-Disposition': f'attachment; filename="{yt.title}.mp4"'}
                )
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}", status=500)
    return redirect('index')
