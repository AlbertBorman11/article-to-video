#!/usr/bin/env python
import sys
import os
import random
import re
import requests
import pyttsx3
from PIL import Image, ImageDraw, ImageFont, ImageColor
from bs4 import BeautifulSoup
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip

def get_text_from_article(url):
    print(f"Fetching data from {url}")
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectTimeout:
        print("Connection error, please try again.")
        quit()
    soup = BeautifulSoup(response.text, "html.parser")
    header = soup.find(class_="blog_header").text.strip() if soup.find(class_="blog_header") else ""
    text = soup.find(class_="article_text").text.strip() if soup.find(class_="article_text") else ""
    text = text.replace('Читайте по теме:', 'Listen to the topic:')
    print("Data received!")
    return header, text

def get_audio_duration(audio_file):
    return len(AudioFileClip(audio_file)) / 1000

def format_text(text):
    # Cleaning up unnecessary spaces and line breaks
    formatted_text = text.strip()

    # Replacing double quotes with single quotes
    formatted_text = formatted_text.replace('"', "'")

    # Splitting text into paragraphs
    paragraphs = formatted_text.split("\n")

    # Processing each paragraph
    formatted_paragraphs = []
    for paragraph in paragraphs:
        # Removing leading and trailing spaces in the paragraph
        formatted_paragraph = paragraph.strip()

        # Splitting the paragraph into sentences
        sentences = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", formatted_paragraph)

        # Processing each sentence
        formatted_sentences = []
        for sentence in sentences:
            # Removing leading and trailing spaces in the sentence
            formatted_sentence = sentence.strip()

            # Skipping empty sentences
            if not formatted_sentence:
                continue

            # Adding <s> and </s> tags to mark the sentence
            formatted_sentence = "<s>" + formatted_sentence + "</s>"
            formatted_sentences.append(formatted_sentence)

        # Joining processed sentences into a paragraph
        formatted_paragraph = "<p>" + " ".join(formatted_sentences) + "</p>"
        formatted_paragraphs.append(formatted_paragraph)

    # Joining processed paragraphs into text
    formatted_text = " ".join(formatted_paragraphs)

    # Adding <speak> and </speak> tags to mark the speech
    formatted_text = "<speak>" + formatted_text + "</speak>"
    return formatted_text

def text_to_speech(text, filename, voice):
    engine = pyttsx3.init()
    if voice == 1:
        engine.setProperty('voice', "com.apple.speech.synthesis.voice.yuri")
        engine.setProperty('rate', 175)
    else:
        engine.setProperty('voice', "com.apple.speech.synthesis.voice.milena.premium")
        engine.setProperty('rate', 165)
    engine.save_to_file(text, filename)
    engine.runAndWait()
    print(f"Text successfully voiced and saved to file {filename}")

def authenticate_google_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive

def create_video(audio_file, image_file, output_file, drive):
    audio = AudioFileClip(audio_file)
    image = ImageClip(image_file)
    video = CompositeVideoClip([image.set_duration(get_audio_duration(audio_file) + 3)])
    video = video.set_audio(audio)
    video.write_videofile(output_file, codec='libx264', audio_codec='aac', fps=24)
    gfile = drive.CreateFile({'title': output_file})
    gfile.SetContentFile(output_file)
    gfile.Upload()
    print("Video uploaded to Google Drive.")

def create_preview(title, width, height, color_schemes, font_size, output_file):
    text_color, background_color = random.choice(color_schemes)
    image = Image.new('RGB', (width, height), ImageColor.getrgb(background_color))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/Users/macbookpro/Documents/youtube news/ofont.ru_Kanit Cyrillic.ttf', font_size)
    text_width, text_height = draw.textsize(title, font=font)
    lines = []
    if text_width > width:
        words = title.split()
        line = ""
        for word in words:
            line_width, _ = draw.textsize(line + word + " ", font=font)
            if line_width > width:
                lines.append(line.strip())
                line = ""
            line += word + " "
        lines.append(line.strip())
    else:
        lines.append(title)
    current_y = (height - len(lines) * text_height) // 2
    for line in lines:
        line_width, _ = draw.textsize(line, font=font)
        x = (width - line_width) // 2
        draw.text((x, current_y), line, font=font, fill=ImageColor.getrgb(text_color))
        current_y += text_height
    image.save(output_file)
    print("Preview created!")

# Checking if the URL is provided as a command-line argument
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    print("Please provide the URL as a command-line argument.")
    sys.exit(1)

# Fetching article data from the URL
article_title, main_text = get_text_from_article(url)
news_text = f"{article_title}\n\n{main_text}\n\nSubscribe and like! It helps the channel."
audio_file, preview_output_file = "news_audio.mp3", "news_image.jpg"
print(news_text)

# Formatting and processing the news text
news_text = format_text(news_text)
print(news_text)

# Converting the news text to speech
text_to_speech(news_text, audio_file, random.randint(1, 2))

# Creating a preview image
preview_width, preview_height, preview_color_schemes, preview_font_size = 1280, 720, [('#074A5E', '#FD975E'), ('#07BD59', '#59014E'), ('#91FEC7', '#3B5C91'), ('#482BEA', '#8DE6B7'), ('#23016B', '#3DCA06'), ('#3DE109', '#360D75'), ('#23104B', '#BE906A'), ('#2531E7', '#B5F7E1'), ('#21A08B', '#54023C'), ('#1F4897', '#9CE08D'), ('#D7C106', '#4A1987'), ('#8BF0D9', '#5D4E20'), ('#2C05EB', '#FBC137'), ('#9826FA', '#8DFCEB'), ('#F2E497', '#7143D0'), ('#534207', '#20DB1C'), ('#AED847', '#180FB5'), ('#0415C7', '#75BF4A'), ('#291A78', '#F7ABE4'), ('#0B194D', '#95D81E'), ('#A92310', '#B7F8E9'), ('#A3BF18', '#7E0829'), ('#270E8D', '#57CF8A'), ('#D456FE', '#0C137D'), ('#48D76B', '#264A83'), ('#F4E027', '#874CA9'), ('#4DFE7B', '#6C0478'), ('#EFC324', '#531CA2'), ('#3541BD', '#AEC6D5'), ('#20DE34', '#254A18'), ('#F387A6', '#830B4C'), ('#B1A5EC', '#1C2648'), ('#91072C', '#71E6AD'), ('#830B2D', '#70C8A5'), ('#ACFD85', '#561C89'), ('#3B1647', '#FD6C20'), ('#6A4295', '#A6DB79'), ('#43D0A8', '#0E3894'), ('#9BC478', '#91034B'), ('#AF67D5', '#3D062E'), ('#5109DE', '#06E34D'), ('#4F1920', '#30EC57'), ('#6F2B4C', '#58DB9A'), ('#F27D5A', '#2F0CB9'), ('#42FDC5', '#493BFD'), ('#9EA0D6', '#4E0F91'), ('#2435A6', '#F8E059'), ('#032B65', '#7BC698'), ('#093D28', '#18E749'), ('#60FB57', '#B5347C'), ('#692CA4', '#1ED9FB'), ('#CDEF75', '#1C2FAE'), ('#310469', '#01E3DA'), ('#1D354F', '#A4C3F0'), ('#3C7645', '#9DFC52'), ('#F4DCA2', '#1F392A'), ('#C1E3A4', '#B80753'), ('#31DA70', '#091D27'), ('#1E0BF8', '#17E3D4'), ('#4A387C', '#93D501')], 70
create_preview(article_title, preview_width, preview_height, preview_color_schemes, preview_font_size, preview_output_file)

# Authenticating Google Drive
drive = authenticate_google_drive()

# Creating the video and uploading it to Google Drive
create_video(audio_file, preview_output_file, f"{article_title.replace(' ', '_')}.mp4", drive)

# Removing temporary files
if os.path.exists(preview_output_file) and os.path.exists(audio_file):
    os.remove(preview_output_file)
    os.remove(audio_file)
    print("Done!")
else:
    print(f"Files {preview_output_file} and {audio_file} not found.")

