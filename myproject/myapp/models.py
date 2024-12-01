from djongo import models  # Import models from djongo

# User model for authentication or user information
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)

    def __str__(self):
        return self.email

# GestureMapping model to store gesture mappings with lists (for MongoDB)
class GestureMapping(models.Model):
    isl_gif = models.ArrayField(models.TextField())  # Use TextField (suitable for strings)
    arr = models.ArrayField(models.CharField(max_length=1))  # Array of single characters (e.g., a, b, c)

    def __str__(self):
        return "Gesture Mappings"

# SpeechRecognition model to store speech-to-text results with images
class SpeechRecognition(models.Model):
    text = models.CharField(max_length=255)  # Recognized text from speech
    image_url = models.JSONField(default=list)  # List of image paths associated with the recognized text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the recognition was created

    def __str__(self):
        return f"Speech Recognition: {self.text} ({self.created_at})"
