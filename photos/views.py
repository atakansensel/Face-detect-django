from django.shortcuts import render, redirect
from .models import Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
import cv2
import time
import os 
import io
from PIL import Image
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile

def detect_faces(cascade, test_image, name,scaleFactor = 1.1):
    
    image_copy = test_image.copy()
    
    gray_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)

    faces_rect = cascade.detectMultiScale(gray_image, scaleFactor=scaleFactor, minNeighbors=5)

    for (x, y, w, h) in faces_rect:
        cv2.rectangle(image_copy, (x, y), (x+w, y+h), (0, 255, 0), 10)
    
    cv2.imwrite(name,image_copy)
   
    PIL_image = Image.open(name)
    
    im_io = io.BytesIO()
    PIL_image.save(im_io, 'JPEG')
    im_io.seek(0) 
    image = InMemoryUploadedFile(
        im_io, None, name, 'image/jpeg', len(im_io.getvalue()), None
    )
    
    photo = Photo.objects.create(
                description=image.name,
                image=image,
            )
    photo.save()
    return image_copy



def gallery(request):
    user = request.user
    
    photos = Photo.objects.all()

    context = {'photos': photos}
    return render(request, 'photos/gallery.html', context)



def addPhoto(request):
    

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        
        for image in images:
            
            photo = Photo.objects.create(
                image=image,
            )
            photo.save()
            # get current directory
            
            
            
            x = '/static/images/'
            # buraya tam uzantısını yapıştırır mısın ? örnek : C:/Users/Hakan/Desktop/projects/freelance/New folder (3)/face-detect-app/static/images/
            y = os.path.join('', photo.image.name)
            
            name = "processed_" + str(photo.image.name)
            # buraya tam uzantısını yapıştırır mısın ? 
            y1 = os.path.join('', name)  
            test_image2 = cv2.imread(y)
            # bu xml dosyası view ile aynı yerde olması gerekiyor 
            #C:\\Users\\Hakan\\Desktop\\projects\\freelance\\New folder (3)\\haarcascade_frontalface_default.xml

            haar_cascade_face = cv2.CascadeClassifier('')
            
            detect_faces(haar_cascade_face, test_image2, y1, scaleFactor = 1.1)
            
        return redirect('gallery')

    
    return render(request, 'photos/add.html')
