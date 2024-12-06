from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import logout as auth_logout, authenticate,login 


def home(request):
    print(request)
    return render(request, 'index.html')


def about(request):
    return render(request, 'aboutus.html')

def features(request):
    return render(request, 'service.html')

def contactpage(request):
    return render(request, 'con.html')

def back(request):
    return render(request, 'mainnew.html')


from django.contrib.auth.models import User

def signup_view(request):
    print('goodydm')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        print(f"Received: {username}, {password}, {email}")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'registration.html')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email address is already in use.")
            return render(request, 'registration.html')

        # Hash the password
        hashed_password = make_password(password)

        try:
            # Create a new user
            print('inside try')
            user = User(username=username, password=hashed_password, email=email)
            user.save()
            print('User saved successfully.')

            # Optional: Add a message for successful registration
            messages.success(request, 'Your account has been created successfully!')
            return render(request, 'login.html')  # Redirect to the login page after successful registration
        except Exception as e:
            # Log the exception and show a generic error message
            print(f"Error saving user: {e}")
            messages.error(request, "An error occurred while creating your account. Please try again later.")
            return render(request, 'registration.html')
    return render(request, 'registration.html')

def login_views(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print('auth hai')
        if user is not None:
            print('user ke ander')
            login(request, user) 
            messages.success(request, 'You have been successfully logged in.')
            return render(request, 'index.html')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')


def logout(request):
    auth_logout(request)  
    return render(request, 'index.html') 


# # views.py
# import speech_recognition as sr
# import string
# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import GestureMapping, SpeechRecognition
# from PIL import Image
# import os

# def speech_to_text(request):
#     r = sr.Recognizer()

#     # Fetch gesture mappings from the MongoDB
#     gesture_mapping = GestureMapping.objects.first()  # Assuming only one entry exists
#     if not gesture_mapping:
#         return JsonResponse({"error": "Gesture mappings not found in the database"}, status=500)

#     isl_gif = gesture_mapping.isl_gif
#     arr = gesture_mapping.arr

#     if request.method == "POST":
#         with sr.Microphone() as source:
#             r.adjust_for_ambient_noise(source)
#             audio = r.listen(source)

#             try:
#                 recognized_text = r.recognize_sphinx(audio)
#                 print("You said:", recognized_text.lower())

#                 # Clean up recognized text (remove punctuation)
#                 for c in string.punctuation:
#                     recognized_text = recognized_text.replace(c, "")

#                 # Handle a special case (e.g., "goodbye")
#                 if recognized_text.lower() in ["goodbye", "good bye", "bye"]:
#                     return JsonResponse({"message": "Goodbye!"}, status=200)

#                 # If the recognized text is a known ISL gif phrase
#                 if recognized_text.lower() in isl_gif:
#                     return JsonResponse({"message": f"GIF functionality for {recognized_text.lower()} is not implemented yet."}, status=200)

#                 # If the recognized text is alphabetic (letters a-z)
#                 recognized_data = []
#                 image_urls = []

#                 for char in recognized_text.lower():
#                     if char in arr:
#                         image_address = f'letters/{char}.jpg'
#                         image_urls.append(image_address)  # Store the image path
#                         recognized_data.append({"letter": char, "image_url": image_address})

#                 # Save recognized text and image URLs in the database
#                 speech_recognition = SpeechRecognition.objects.create(
#                     text=recognized_text.lower(),
#                     image_url=image_urls
#                 )

#                 return JsonResponse({
#                     "message": "Text recognized and images saved",
#                     "recognized_text": recognized_text.lower(),
#                     "data": recognized_data
#                 }, status=200)

#             except Exception as e:
#                 return JsonResponse({"error": str(e)}, status=500)

#     return render(request, 'speech_to_text.html')


def videocheck(request):
    return render(request, 'camera.html')



def tryyy(request):
    return render(request, 'tryy.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# List of phrases that should correspond to GIFs
isl_gif = ['any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
           'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office', 'do you have money',
           'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry', 'flower is beautiful',
           'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch', 'happy journey',
           'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bored doing nothing', 
           'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop']

# List of alphabet letters for sign language images
arr = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r', 's','t','u','v','w','x','y','z']

@csrf_exempt
def speech_to_text(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            recognized_text = data.get('text', '').lower()
            print(f"Received Text: {recognized_text}")

            # Check if recognized text matches a GIF
            if recognized_text in isl_gif:
                gif_url = f'/static/ISL_Gifs/{recognized_text}.gif'
                return JsonResponse({'gif_url': gif_url})

            # Check if recognized text matches a letter and return corresponding image
            image_urls = []
            for c in recognized_text:
                if c in arr:
                    image_path = f'/static/letters/{c}.jpg'
                    image_urls.append(image_path)

            if image_urls:
                return JsonResponse({'image_urls': image_urls})

            return JsonResponse({'message': 'Text not recognized'})
        
        except Exception as e:
            return JsonResponse({'message': f"Error processing text: {str(e)}"})

    return JsonResponse({'message': 'Invalid request method'})

from django.shortcuts import render
from django.http import JsonResponse
import json

def text_to_sign(request):
    if request.method == 'POST':
        input_text = request.POST.get('inputText', '').lower()
        print(f"Received Text: {input_text}")

        gif_url = None
        image_urls = []
        message = None

        # Check if recognized text matches a GIF
        if input_text in isl_gif:
            print("pharse mila ")
            gif_url = f'/static/ISL_Gifs/{input_text}.gif'

        # Check if recognized text matches a letter and return corresponding image
        for c in input_text:
            if c in arr:
                print("image mil gya")
                image_path = f'/static/letters/{c}.jpg'
                image_urls.append(image_path)

        if not gif_url and not image_urls:
            message = "Text not recognized or no matching images found."

        return render(request, 'texttosign.html', {
            'gif_url': gif_url,
            'image_urls': image_urls,
            'message': message
        })

    return render(request, 'texttosign.html')
