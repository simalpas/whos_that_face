import os
import requests
from django.db import models
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from faker import Faker

fake = Faker()


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    face = models.ImageField(upload_to="faces/", null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically populate first_name and last_name using Faker
        if not self.first_name:
            self.first_name = fake.first_name()
        if not self.last_name:
            self.last_name = fake.last_name()

        # Fetch and save the face image from 'thispersondoesnotexist.com'
        if not self.face:
            # Fetch image
            response = requests.get("https://thispersondoesnotexist.com/image")
            if response.status_code == 200:
                image_content = ContentFile(response.content)
                # Create a random filename
                file_name = f"{get_random_string(10)}.jpg"
                # Save the image to the media directory
                self.face.save(file_name, image_content, save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
