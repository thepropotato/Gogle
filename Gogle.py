import json
from bs4 import BeautifulSoup
import urllib.request
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from io import BytesIO
from io import BytesIO
import requests
from flask import jsonify,Flask, render_template, redirect, url_for, request, session
import time
import os


google_api_key = os.getenv('Google_API_key')   # YOUR GOOGLE API KEY (can be created in Google cloud console)
google_engine_index = "974f71f92973b4990"
openai_api_key = os.getenv('OpenAI_API_key')   # YOUR OPENAI API KEY (API key creation is free, but you have to pay for using the models used in this code)

import pandas as pd
import json

def ask_google(query):
    columns = ['Title', 'Link']
    df = pd.DataFrame(columns=columns)
    
    url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={google_engine_index}&q={query}"
    response = requests.get(url)
    data = json.loads(response.text)

    if 'error' in data:
        print("Error:", data['error']['message'])
        df = df._append({'Title': 'Error', 'Link': 'Uh-Oh, An unexpected error has occurred !'}, ignore_index=True)
    elif 'items' not in data:
        print("No search results found.")
    else:
        search_results = data['items']

        for result in search_results:
            title = result['title']
            link = result['link']
            df = df._append({'Title': title, 'Link': link}, ignore_index=True)
    
    return df

def generate_summary(huge_text):

    import openai
    openai.api_key = openai_api_key

    try :
        chunk_size = 4000 
        summary = ""

        chunks = [huge_text[i:i+chunk_size] for i in range(0, len(huge_text), chunk_size)]

        for chunk in chunks:
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=f"Please summarize the following text in not more than one paragraph (Please strictly do not write more than one paragraph). You can cut off non-completed words. Make sure the meaning holds \n\n {chunk}",
                max_tokens=500, 
                temperature=1,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            summary += response.choices[0].text.strip() + " "
        
        return summary.strip()
    except Exception as e:
        return "No sufficient and suitable content found."
    
def scrape(url):
    try :
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        request = urllib.request.Request(url, headers=headers)

        scraped_data = urllib.request.urlopen(request)
        
        article = scraped_data.read()
        parsed_article = BeautifulSoup(article, "html.parser")

        paragraphs = parsed_article.find_all('p')

        text = ""

        for p in paragraphs:
            text += p.text
            
        if text == "" or text == None :
            text = "No paragraph content found."

        return text
    
    except Exception as e:
        return ""

def get_subtitles(youtube_url):
    try:
        video_id = youtube_url.split('?v=')[1]  # Extract video ID from URL
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        subtitles = ''
        for segment in transcript_list:
            subtitles += segment['text'] + ' '
        return subtitles.strip()
    except Exception as e:
        return ("Failed to extract subtitles, The most possible reason is that the provided video has no subtitles")

def extract_audio_from_video(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_content = BytesIO()
    audio_stream.stream_to_buffer(audio_content)
    audio_content.seek(0)
    
    return audio_content

def transcribe_audio_from_bytesio(audio_bytes_io):
    import assemblyai as aai
    base_url = "https://api.assemblyai.com/v2"

    headers = {
        "authorization": "a71d23dd92b6477983988cf41ccc0dff"
    }

    response = requests.post(base_url + "/upload", headers=headers, data=audio_bytes_io)

    upload_url = response.json()["upload_url"]

    data = {
        "audio_url": upload_url
    }

    url = base_url + "/transcript"
    response = requests.post(url, json=data, headers=headers)

    transcript_id = response.json()['id']
    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()

        if transcription_result['status'] == 'completed':
            return transcription_result['text']

        elif transcription_result['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

        else:
            time.sleep(3)


def gogle_transcript(url):
    subtitles = get_subtitles(url)
    if subtitles == "Failed to extract subtitles, The most possible reason is that the provided video has no subtitles" :
        audio_io = extract_audio_from_video(url)
        subtitles = transcribe_audio_from_bytesio(audio_io)
    return subtitles

# --------------------------------- FINAL FUNCTIONS ------------------------------------ #

def gogle_summarize(query):
    results = ask_google(query)
    titles = results['Title']
    links = results['Link']
    data = list(zip(titles, links))

    summary = ""    
    try:
        for ind in range(3):
            text_in_web = scrape(links[ind])
            page_summary = generate_summary(text_in_web)
            summary += "\n\n" + page_summary
        final_summary = generate_summary(summary)
        final_summary = "\n" + final_summary.split("\n")[-1]

    except Exception as e:
        final_summary = "Unable to generate a summary. This might be due to insufficient text content on the main webpages."

    return final_summary

def gogle_page_summarize(url) :
    text = scrape(url)
    summary = generate_summary(text)
    return summary

def gogle_video_summarize(url):
    transcript = gogle_transcript(url)
    summarized_transcript = generate_summary(transcript)
    return transcript, summarized_transcript

# ------------------------------------- FLASK ROUTES --------------------------------------- #

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/download', methods=['GET', 'POST'])
def home_download():
    return render_template('download.html')

@app.route('/about', methods=['GET', 'POST'])
def home_about():
    return render_template('about.html')

@app.route('/showgoogleresults', methods=['POST'])
def show_google_results_route() :
    data = request.json
    query = data.get('query')
    results = ask_google(query)
    titles = results['Title']
    links = results['Link']
    data = list(zip(titles, links))
    return jsonify({"data" : data})


@app.route('/querysummarize', methods=['POST'])
def query_summarize_route():
    data = request.json
    query = data.get('query')
    summary = gogle_summarize(query)
    return summary

@app.route('/videotranscript', methods=['POST'])
def gogle_transcript_route():
    data = request.json
    video_url = data.get('url')
    transcript, summarized_transcript = gogle_video_summarize(video_url)
    return jsonify({'transcript': transcript, 'summarized_transcript': summarized_transcript})

@app.route('/webpagesummarize', methods=['POST'])
def gogle_page_summarize_route():
    data = request.json
    web_url = data.get('url')
    summary = gogle_page_summarize(web_url)
    return summary

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404

@app.errorhandler(Exception)
def internal_server_error(error):
    return redirect(url_for('custom_error_page'))

@app.route('/error')
def custom_error_page():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)


