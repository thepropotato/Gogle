# What is Gogle ? 

**Gogle** is a search tool and summarizer that can efficiently
 1. Show Google results of a query and summarize them.
 2. Generate transcript for a youtube video (even for a video without subtitles) and summarize it.
 3. Read an entire webpage and summarize it for you.
 4. Read out the summaries.

All this to save time and avoid going through all the links displayed in the results page of Google. 

Website : The website is now live at <a href=https://dogogle.onrender.com>https://dogogle.onrender.com</a><br><br>


# Gogle - Website

The website is built purely using Python, HTML, CSS and a bit of Javascript. The website is *built responsive* (adapting to screens), but **for a better experience, viewing from a Laptop/Computer (Landscape mode) is suggested**.
<br>

    Each line of code behind the website is written from scratch.
<br>

# Landing (Home) page

![alt text](https://github.com/thepropotato/Gogle/blob/main/readme-images/home.png)

The landing page has a header row for navigation. The buttons on the side bar (namely *Search*, *Youtube Video*, *Webpage*) are the modes of summarization Gogle offers.

1. Clicking on the **Gogle** button will scroll to the landing page.

2. A click on the **Download** button will take you to the download page of the website.

3. To go to the **About** section of the website, just hit on the About button.<br><br>

# Services : Modes of Summarization

<h3>1. Query summarization :</h3>

![alt text](https://github.com/thepropotato/Gogle/blob/main/readme-images/query-search.png)

The **Search** button will change the mode of the website to *Query Summarization*. For a demo, I've searched for one of India's top directors S.S. Rajamouli, Gogle first shows the Google results for the query and then proceeds to summarize them.

    NOTE : A lot of experimenting proved that the first 3 results contain the approppriate and most relevant content, in line with the search query. So Gogle summarizes the first 3 results. 

<br>

<h3>2. Youtube video summarization :</h3>

![alt text](https://github.com/thepropotato/Gogle/blob/main/readme-images/youtube-video.png)

The **Youtube video** button will change the mode of the website to *Youtube video Summarization*. To display the results, I've searched the link of the teaser of Rajinikanth's Coolie.

The details of what happens behind the screens is clearly discussed in the [Behind the screens](#back-end) section of the article.

Once the search results are obtained, the original transcript of the video will displayed on the right and the summarized transcript will take the left part of the screen.

**Read Aloud feature :**

<video controls>
    <source src="https://raw.githubusercontent.com/thepropotato/Gogle/575dc31f0a44135ac38f2c537e35cbbd8c5911a9/readme-images/demo.mp4" type="video/mp4">
</video>

For a better understanding of the working of the site, i have also included a loading animation video in the video.

<br>

<h3>3. Webpage summarization :</h3>

![alt text](https://github.com/thepropotato/Gogle/blob/main/readme-images/webpage.png)

The **Webpage** button will change the mode of the website to *Webpage Summarization*. I have triggered this route with the link of Wikipidea page of Mahatma Gandhi. The summary is provided on the left half, along with the original website displayed on the right half of the page.

<br>

# Download page

![alt text](https://github.com/thepropotato/Gogle/blob/main/readme-images/download.png)

Keeping in mind the percentage of people preferring CLIs over GUIs, We decided to provide a command line tool that does all that the website can do.

Hitting on the **Download** button will quickly start the download of the Command line tool. 

At this moment Gogle (CLI) is only available for windows, and will be downloaded in ".exe" extension. Others can always clone this repository though.<br><br>

# About page

![alt text](https://github.com/thepropotato/Gogle/blob/main/readme-images/about.png)

This section of the website talks about the creators and our primary aim with Gogle. You can always get in touch with us using the creator cards.
<br>

<h1 id="back-end">Behind the screens</h1>

In the backend, everything is done using API calls.

- Text summarization is done using *OpenAI's API*.
- Youtube videos (with subtitles) will be first going through a process for extraction of the exisiting transcripts. Then the extracted transcripts will be summarized.
- Youtube videos (without subtitles) will be first converted to audio and this audio is passed to *AssemblyAI's API* for performing the audio to text conversion process.
- Google results are being shown using Google's *Custom search engine API.*

<br>

# Design choices

With the design, I wanted the website to look futuristic and friendly. So, i decided to use boxy fonts.

- Fonts used :
    - <a href="https://www.urbanfonts.com/fonts/Metal_On_Metal.font">Metal on metal</a>
    - <a href="fonts.google.com/specimen/Share+Tech">Share tech</a>
    - <a href="https://fonts.google.com/specimen/Bungee+Hairline">Bungee Hairline</a>

- Icons used are from:
    - <a href="https://fonts.google.com/icons">Google icons</a>
    - <a href="https://fontawesome.com/icons">Font awesome</a> 
<br><br>


# Technologies used

- HTML
- CSS
- Python
- Flask
- JavaScript <br><br>

# Why "Gogle" ?

The reason behind naming the tool Gogle is that, Google has two o's which (might) take some time to pronoune. Whereas Gogle with a single 'o' is relatively faster to pronounce. With the aim to make the user find what he really wants quickly, we thought this would be in-line with the context.

<br>

# Gogle - Command Line Tool

![alt text](https://github.com/thepropotato/Gogle/blob/main/readme-images/CLI-1.png)
Upon opening the installed "Gogle.exe" file, you will find this animation.

![alt text](https://github.com/thepropotato/Gogle/blob/main/readme-images/CLI-2.png)
Immediately after which, this table of valid commands will pop up to help you get familiar with our tool.

<br>

# Queries and Feedback

For any Queries and feedback please mail me at notvenupulagam@gmail.com

Hope you liked the website. Have a good day. Happy gogling.

*Thank you.*
