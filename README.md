# 🐍 News-to-Video Script 📰🎥

This script converts news articles into videos with text-to-speech narration and uploads them to Google Drive. 🚀

## Requirements

- Python 3.6 or above
- `requests`, `pyttsx3`, `Pillow`, `beautifulsoup4`, `pydrive`, `moviepy` Python packages

## Usage

1. Install the required packages:

   ```bash
   pip install requests pyttsx3 Pillow beautifulsoup4 pydrive moviepy
   ```

2. Save the script to a file, e.g., `news_to_video.py`.

3. Run the script with the URL of the news article as a command-line argument:

   ```bash
   python news_to_video.py <article_url>
   ```

   Replace `<article_url>` with the actual URL of the news article.

4. The script will create a video with text-to-speech narration and upload it to Google Drive. The generated video will have the same name as the article's title.

## 📚 Acknowledgments

This script uses several Python libraries and APIs:

- `requests`: for making HTTP requests to fetch the news article.
- `beautifulsoup4`: for parsing the HTML response and extracting the article's text.
- `pyttsx3`: for converting the formatted text into speech and saving it as an audio file.
- `Pillow`: for creating the preview image with the article's title.
- `pydrive`: for authenticating with Google Drive and uploading the video.
- `moviepy`: for combining the audio and image into a video.

Feel free to modify and improve this script according to your needs. Happy coding! 🎉🚀
