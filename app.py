import streamlit as st
import numpy as np
import easyocr
import cv2
from googletrans import Translator
from PIL import Image
import pandas as pd
language_mapping = {
    'Telugu': 'te',  # Telugu
    'Hindi': 'hi',  # Hindi
    'Tamil': 'ta',  # Tamil
    'Bengali': 'bn',  # Bengali
    'Bhojpuri':'bho',
    'kannada': 'kn',  # Kannada
    'marathi': 'mr',  # Marathi
    'Urdu': 'ur',  # Urdu
    'Assamese': 'as',  # Assamese
    'Nepali': 'ne',  # Nepali
    'Konkani': 'gom',  # Konkani
    'English': 'en', #english
    'Maithili': 'mai',  # Maithili
    'French': 'fr',  # French
    'Spanish': 'es',  # Spanish
    'Latin':'la',
    'German': 'de',  # German
    'Chineese(simplified)': 'ch_sim',  # Chinese (Simplified)
    'Chineese(traditional)':'ch_tra',
    'Danish':'da',
    'Persian(farsi)':'fa',
    'Irish':'ga',
    'Hungarian':'hu',
    'Japanese': 'ja',  # Japanese
    'Arabic': 'ar',  # Arabic
    'Russian': 'ru',  # Russian
    'Romanian':'ro',
    'Portuguese': 'pt',  # Portuguese
    'Italian': 'it',  # Italian
    'Korean': 'ko',  # Korean
    'Dutch': 'nl',  # Dutch
    'Swedish': 'sv',  # Swedish
    'Turkish': 'tr',  # Turkish
    'Ukranian':'uk',
    'Polish': 'pl',  # Polish
    'Vietnamese': 'vi',  # Vietnamese
    'Thai': 'th',  # Thai
    'Indonesian': 'id',  # Indonesian
    'Malay': 'ms',  # Malay
    'Mongolian':'mn',
    'Afrikaans':'af',
    'Maltese':'mt',
}
def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://www.bpmcdn.com/f/files/vernon/import/2023-06/33146655_web1_230628-KCN-morning-start_1.jpg;w=960");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
st.markdown("""
<style>
.big-font {
    font-size:300px !important;
}
</style>
""", unsafe_allow_html=True)
set_bg_hack_url()
st.title(":white[OCR Based Multi Lingual Text Extraction and Machine Translation]")

def save_captured_image(img_bytes):
  img_arr = np.frombuffer(img_bytes, np.uint8)
  img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
  cv2.imwrite("captured_image.jpg", img)

def preprocess(img):
    img_np = np.array(img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]
    return img

def text_extract(img, lan, slang, dlang):
    # Load the image
    gray = preprocess(img)
    reader = easyocr.Reader([lang])
    results = reader.readtext(img)
    df=pd.DataFrame(results, columns=['bbox','text','conf'])
    print(df['text'])
    l=len(df)
    text=""
    for i in range(l):
      text=text+df['text'][i]+" "
    #text = pytesseract.image_to_string(gray, lang=lan)
    if not text:
        return "Text not found"
    translator = Translator()
    try:
        translated = translator.translate(text, src=slang, dest=dlang)
        translated_text = translated.text
    except Exception as e:
        print("Translation error:", e)
        translated_text = "Text not found"
    
    return translated_text
    

uploaded_file = st.file_uploader("Choose a file in jpg format")
picture = st.camera_input("Take a Picture")
option1 = st.selectbox('Source Language' , ('Afrikaans',
    'Arabic',
    'Assamese',
    'Bengali',
    'Bhojpuri',
    'Chineese(simplified)',
    'Chineese(traditional)',
    'Danish',
    'Dutch',
    'English',
    'French',
    'German',
    'Hindi',
    'Hungarian',
    'Indonesian',
    'Irish',
    'Italian',
    'Japanese',
    'Kannada',
    'Korean',
    'Konkani',
    'Latin',
    'Maithili',
    'Malay',
    'Maltese',
    'Marathi',
    'Mongolian',
    'Nepali',
    'Persian(farsi)',
    'Polish',
    'Portuguese',
    'Romanian',
    'Russian',
    'Spanish',
    'Swedish',
    'Tamil',
    'Telugu',
    'Thai',
    'Turkish',
    'Ukranian',
    'Urdu',
    'Vietnamese'))
option2 = st.selectbox('Desired Language' , ('Afrikaans',
    'Arabic',
    'Assamese',
    'Bengali',
    'Bhojpuri',
    'Chineese(simplified)',
    'Chineese(traditional)',
    'Danish',
    'Dutch',
    'English',
    'French',
    'German',
    'Hindi',
    'Hungarian',
    'Indonesian',
    'Irish',
    'Italian',
    'Japanese',
    'Kannada',
    'Korean',
    'Konkani',
    'Latin',
    'Maithili',
    'Malay',
    'Maltese',
    'Marathi',
    'Mongolian',
    'Nepali',
    'Persian(farsi)',
    'Polish',
    'Portuguese',
    'Romanian',
    'Russian',
    'Spanish',
    'Swedish',
    'Tamil',
    'Telugu',
    'Thai',
    'Turkish',
    'Ukranian',
    'Urdu',
    'Vietnamese'))
slang = language_mapping.get(option1)
dlang = language_mapping.get(option2)
lang=slang
if option1=='Chineese(simplified)':
    slang = 'zh'
if option1=='Chineese(traditional)':
    slang = 'zh-TW'
if option2=='Chineese(simplified)':
    dlang = 'zh'
if option2=='Chineese(traditional)':
    dlang = 'zh-TW'
if picture:
  save_captured_image(picture.read())
  st.success("Image uploaded")
  img = cv2.imread('captured_image.jpg')
  st.image(img,caption='uploaded image')
  text = text_extract(img, lang, slang, dlang)
  st.write(text)
elif uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img,caption='uploaded image')
    text = text_extract(img, lang, slang, dlang)
    st.write(text)
