import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"my-key.json"
from google.cloud import vision
import io
from gtts import gTTS 
import pygame, sys, time
from pygame.locals import *
import os
import speech_recognition as sr 
from mutagen.mp3 import MP3
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

def google_text_speech(mytext,language="en"):
    
    print("\nConverting Text to Audio ...")
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("audio.mp3")
    audio = MP3("audio.mp3")
    audio_info = audio.info
    length_sec = int(audio_info.length)
    print("Playing Audio ...")
    pygame.init()
    pygame.mixer.music.load("audio.mp3")
    pygame.mixer.music.play()
    time.sleep(length_sec+1)
    pygame.mixer.music.stop()
    pygame.quit()
    print("End of Audio\n")


def Image_Text_Speech(path):
    """(i_to_text(path) function)"""
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    
    lang_list = []
    
    for p in response.full_text_annotation.pages:
        w = p.property.detected_languages
        for w in response.full_text_annotation.pages[0].property.detected_languages:
            l = w.language_code
            if(l == '' or l =='und'):
                l = 'en'
            if l not in lang_list:
                lang_list.append(l)
                
    if(len(lang_list)==0):
        lang_list.append("en-in")    
    
    final = ""
    print("\nText :")
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
#             print('\nBlock confidence: {}\n'.format(block.confidence))
            for paragraph in block.paragraphs:
#                 print('Paragraph confidence: {}'.format(
#                     paragraph.confidence))
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print(word_text,end=' ')
                    if(word_text=="."):
                        print()
                    final = final + word_text + ' '

#                     for symbol in word.symbols:
#                         print('\tSymbol: {} (confidence: {})'.format(
#                             symbol.text, symbol.confidence))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    
    """(google_text_speech(mytext,language="en") function)"""
    google_text_speech(final,lang_list[0])
    


# # OBJECT 



def Object_Detection(path):
    """
    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    
    google_text_speech('Number of objects found: {}'.format(len(objects)))
    
    if(len(objects)==0):
        return
    
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
#         print('Normalized bounding polygon vertices: ')
#         for vertex in object_.bounding_poly.normalized_vertices:
#             print(' - ({}, {})'.format(vertex.x, vertex.y))
        google_text_speech(object_.name)


# # Menu

r = sr.Recognizer() 
mic_list = sr.Microphone.list_microphone_names()


#change mic_name to corresponding mic
mic_name = 'USB PnP Sound Device: Audio (hw:2,0)'
for i, microphone_name in enumerate(mic_list): 
    if microphone_name == mic_name: 
        device_id = i




def voice_input():
    with sr.Microphone(device_index = device_id, sample_rate = 48000, chunk_size = 2048) as source: 
        #wait for a second to let the recognizer adjust the 
        #energy threshold based on the surrounding noise level 
        r.adjust_for_ambient_noise(source)
        os.system('clear')
        print("Say Something :")

        #listens for the user's input 
        audio = r.listen(source,timeout=60) 

        print("Loading...\n")

        try: 
            text = r.recognize_google(audio) 
            print("Audio Input : " + text)
            return text

        #error occurs when google could not understand what was said 

        except sr.UnknownValueError: 
            print("Google Speech Recognition could not understand audio")
            return 0

        except sr.RequestError as e: 
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return -1

def currency(img_path):
    image = Image.open(img_path)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    curr = model.predict_classes(data)
    print(class_label[curr[0]],"₹")
    google_text_speech(str(class_label[curr[0]])+"₹")




img_path = 'image.jpg'

np.set_printoptions(suppress=True)
model = tensorflow.keras.models.load_model('keras_model.h5',compile=False)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
class_label={0:"10 old",1:"10 new",2:"20 old",3:"20 new",4:"50 old",5:"50 new",6:"100 old",7:"100 new",8:"200",9:"500",10:"2000"}




# MAIN DRIVER CODE

while(True):
    inp_str = voice_input()
    if not inp_str:
        #google_text_speech("Sorry, could not understand. Say that Again ")
        continue
    
    if (inp_str.lower().find('jarvis') != -1):
        '''if (inp_str.find('image') != -1):
            print("Taking Snapshot...")
            os.system('raspistill -o image.jpg ')
            google_text_speech("Taking Snapshot")'''
            
        if (inp_str.lower().find('object') != -1):
            print("Taking Snapshot...")
            google_text_speech("Taking Snapshot")
            os.system('raspistill -o image.jpg ')
            print("Scanning Object...")
            google_text_speech("Scanning Object")
            Object_Detection(img_path)
            
        elif (inp_str.lower().find('text') != -1):
            print("Taking Snapshot...")
            google_text_speech("Taking Snapshot")
            os.system('raspistill -o image.jpg ')
            print("Reading Text")
            google_text_speech("Reading Text")
            Image_Text_Speech(img_path)
            
        elif (inp_str.lower().find('currency') != -1):
            print("Taking Snapshot...")
            google_text_speech("Taking Snapshot")
            os.system('raspistill -o image.jpg ')
            print("Scanning currency")
            google_text_speech("Scanning currency")
            currency(img_path)
            
        elif (inp_str.lower().find('exit') != -1):
            google_text_speech("Terminating !")
            print("Terminating ! ...")
            break
            
        else:
            print("Invalid Command!\nRepeat Command")
            google_text_speech("Invalid Command!. Repeat Command")
            
    
            
    '''else: 
        print("Invalid Command\nPlease Try Again ")
        google_text_speech("Invalid Command. Please Try Again ")'''






