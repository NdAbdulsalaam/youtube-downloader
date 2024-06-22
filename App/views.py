# from django.shortcuts import render, redirect
# from django.http import StreamingHttpResponse, HttpResponse
# from . import forms
# from pytube import YouTube
# import io

# def index(request):
#     form = forms.YouTubeForm()
#     return render(request, 'index.html', {'form': form})

# def stream_video(stream):
#     buffer = io.BytesIO()
#     stream.stream_to_buffer(buffer)
#     buffer.seek(0)
#     while True:
#         data = buffer.read(8192)  # Read in 8KB chunks
#         if not data:
#             break
#         yield data

# def download(request):
#     if request.method == 'POST':
#         form = forms.YouTubeForm(request.POST)
#         if form.is_valid():
#             url = form.cleaned_data['url']
#             try:
#                 yt = YouTube(url)
#                 stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
#                 response = StreamingHttpResponse(stream_video(stream), content_type='video/mp4')
#                 response['Content-Disposition'] = f'attachment; filename="{yt.title}.mp4"'
#                 return response
#             except Exception as e:
#                 return HttpResponse(f"An error occurred: {str(e)}", status=500)
#     return redirect('index')


from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, HttpResponse
from . import forms
from pytube import YouTube
import io

def index(request):
    form = forms.YouTubeForm()
    return render(request, 'index.html', {'form': form})

def stream_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        if stream:
            chunk_size = 1024 * 1024  # 1MB chunk size
            with stream.stream as s:
                while True:
                    chunk = s.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        else:
            yield b"No suitable video stream found"
    except Exception as e:
        yield f"Error streaming video: {str(e)}".encode()

def download(request):
    if request.method == 'POST':
        form = forms.YouTubeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                yt = YouTube(url)
                response = StreamingHttpResponse(stream_video(url), content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{yt.title}.mp4"'
                return response
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}", status=500)
    return redirect('index')

