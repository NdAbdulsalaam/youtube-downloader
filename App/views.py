from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from pytube import YouTube

def index(request):
    form = forms.YouTubeForm()
    return render(request, 'index.html', {'form': form})

def download(request):
    if request.method == 'POST':
        form = forms.YouTubeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                yt = YouTube(url)
                stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
                response = HttpResponse(content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{yt.title}.mp4"'
                stream.stream_to_buffer(response)
                return response
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
    return redirect('index')
