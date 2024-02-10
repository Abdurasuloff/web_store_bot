import os
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Product  # Replace 'your_app' with the actual name of your app

from pprint import pprint as print

@receiver(post_save, sender=Product)
def upload_image(sender, instance: Product, created, *args, **kwargs):
   
    
    if created:
        # if created and instance.image:
        api_url = f"https://api.telegram.org/bot6952853589:AAExy00MDt2WdKndse_zZgvq4pomJ_7koCE/sendPhoto"
        
        chat_id = 6400738281
        
        image_path  = instance.image.path
        
        
        caption = f"{instance.name} "
        
        data = {
            'chat_id': chat_id,
            'caption':caption,
            'parse_mode':'html',
        }
        
        files = {'photo': open(image_path, 'rb')}
        
        response = requests.post(api_url, data=data, files=files)
        
        if response.status_code == 200:
            print("Image sent successfully to Telegram channel!")
            
            data = response.json()
            
            file_id = data['result']['photo'][-1]['file_id']
            
            instance.image_file_id = file_id
            
            instance.save()
            
            
            
            
        else:
            print(f"Failed to send image. Status code: {response.status_code}")
