from django.shortcuts import render, redirect
from .forms import UploadForm
from .models import Upload
import subprocess
import os

def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save()
            result = process_file(upload.file.path)
            return render(request, 'result.html', {'result': result})
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})

def process_file(file_path):
    # Ensure the script path is correct
    script_path = os.path.join(os.path.dirname(__file__), 'Sentiment_Analysis_of_Stock.py')
    
    # Use the correct Python executable for Windows
    result = subprocess.run(['python', script_path, file_path], capture_output=True, text=True)
    return result.stdout
