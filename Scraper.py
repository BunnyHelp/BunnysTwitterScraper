import os
import youtube_dl
import tweepy
from tld import get_tld
import time
from datetime import datetime
import wget


ydl_opts = {}

# auth.set_access_token(access_key, access_secret)

# Attempt top open a URLs.txt file
URLList = []
try:
    URLsTextFile = open('URLs.txt', 'r')
    with URLsTextFile as file:
        URLList = [line.rstrip('\n') for line in file]
except FileNotFoundError:
    print("URLs.txt not found.\nGive one URL to download.")
    URL = input("URL: ")
    URLList = URL
    pass
print(URLList)

for thisURL in URLList:
    URL = str(thisURL)
    URL.strip()
    parsedURL = get_tld(URL, as_object=True)
    domain = parsedURL.domain

    if domain == 'youtube':
        ids = URL[URL.rfind("=") + 1:]
    elif domain == 'twitter':
        # It seems we are downloading a Twitter page, so lets initialize the API
        consumer_key = ""
        consumer_secret = ""
        access_key = ""
        access_secret = ""
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        api = tweepy.API(auth)

        if "?" in URL:
            URL.strip()
            ids = URL[URL.rfind("/") + 1:URL.rfind("?")]
        else:
            ids = URL[URL.rfind("/") + 1:]  # Get the ID of the tweet from the URL
    ids.strip() # strip trailing whitespace


    ydl_opts = {
        'format': '(bestvideo[vcodec^=av01][height>=1080][fps>30]/bestvideo[vcodec=vp9.2][height>=1080][fps>30]/bestvideo[vcodec=vp9][height>=1080][fps>30]/bestvideo[vcodec^=av01][height>=1080]/bestvideo[vcodec=vp9.2][height>=1080]/bestvideo[vcodec=vp9][height>=1080]/bestvideo[height>=1080]/bestvideo[vcodec^=av01][height>=720][fps>30]/bestvideo[vcodec=vp9.2][height>=720][fps>30]/bestvideo[vcodec=vp9][height>=720][fps>30]/bestvideo[vcodec^=av01][height>=720]/bestvideo[vcodec=vp9.2][height>=720]/bestvideo[vcodec=vp9][height>=720]/bestvideo[height>=720]/bestvideo)+(bestaudio[acodec=opus]/bestaudio)/best',
        'verbose': True,
        'force-ipv4': True,
        'no-continue': True,
        'ignoreerrors': True,
        'nooverwrites': True,
        #'download_archive': 'archive.log',
        'writedescription': True,
        'writeinfojson': True,
        'writeannotations': True,
        'write_all_thumbnails': True,
        'writesubtitles': True,
        'subtitleslangs': 'en',
        'writeautomaticsub': True,
        'subtitlesformat': 'srt',
        'merge_output_format': 'mkv'
    }

    # Adding an output template to the ydl_opts dictionary according to the domain we're attempting to scrape
    if domain == 'youtube':
        ydl_opts['outtmpl'] = domain + '/%(id)s/video/%(id)s.%(ext)s'
    elif domain == 'twitter':
        print(ids)
        status = api.get_status(ids, tweet_mode="extended")
        ydl_opts['outtmpl'] = domain + '/' + status.user.screen_name + '/' + ids + '/video/' + ids + '.%(ext)s'

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([str(URL)])

    def get_screenshot(screenshot_directory):
        try:
            print("Getting screenshot...")
            # Writing the current URL to a file that NodeJS / Puppeteer can read to pull a screenshot from.
            send_URL = open('temp.txt', 'a')
            send_URL.write(URL)
            send_URL.close()
            string = " \"C:\Program Files\\nodejs\\node.exe\" screenshot.js"
            os.system(string)  # Sending the command to NodeJS to run the script for Puppeteer.
            time_now = str(datetime.now()).replace('.', " ").replace(":", "_")
            os.rename('screenshot.png', screenshot_directory + '/' + time_now + ' screenshot.png')
            print("Screenshot success.")
            os.remove("temp.txt")  # Cleanup that URL file
        except FileExistsError:
            print("Somehow, this screenshot already exists.")
            pass


    if domain == 'youtube':
        print()
    elif domain == 'twitter':
        try:
            os.makedirs("twitter/" + status.user.screen_name + "/" + ids)
            #print("Warning: This screenshot has already been downloaded.")
        except FileExistsError:
            # directory already exists
            #
            pass
        this_tweets_directory = str("twitter/" + status.user.screen_name + "/" + ids + "/")
        get_screenshot(this_tweets_directory)

        # Getting photos included in the tweet, from the extended_entities list
        media_files = set()
        try:
            media = status.extended_entities.get('media', [])
        except AttributeError:
            # Getting photos included in the tweet, from the extended_entities list
            media = status.entities.get('media', [])
        except:
            print("Error in  status.entities.get('media', [])")
            pass
        if len(media) > 0:
            try:  # im too lazy to figure out how to iterate for the amount of files that could be present, so it just goes over all possible 4 media file the tweet could have, and passes the exception
                media_files.add(media[0]['media_url'])
                media_files.add(media[1]['media_url'])
                media_files.add(media[2]['media_url'])
                media_files.add(media[3]['media_url'])
            except IndexError:
                pass

        # Downloading each Twitter photo URL gotten
        for media_file in media_files:
            # if ".mp4" or ".mov" in media_file:
            #    pass
            # else:
            print(media_file + ":orig")
            try:
                wget.download(str(media_file + "?format=jpg&name=orig"), this_tweets_directory)
            except:
                wget.download(str(media_file + "?format=png&name=orig"), this_tweets_directory)
            finally:
                pass


        create_tweet_text = open(this_tweets_directory + '/tweet text.txt', 'a', encoding='utf-8')

    try:

        create_tweet_text.write(status.retweeted_status.full_text + "\n \n")
        create_tweet_text.write('Created at: ' + str(status.created_at) + ' by @' + status.user.screen_name + " (screen name: " + status.user.name + ")\n")
        create_tweet_text.write('Location: ' + str(status.place) + " , " + str(status.coordinates) + "\n")
        create_tweet_text.write('From: ' + status.source + "\n")
        create_tweet_text.write('Tweet id: ' + ids + "\n")
        # needs premium create_tweet_text.write('Replies: ' + str(status.reply_count)
        create_tweet_text.write("Likes: " + str(status.favorite_count) + "\nRetweets: " + str(status.retweet_count))

    except AttributeError:  # Not a Retweet
        create_tweet_text.write(status.full_text + "\n \n")
        create_tweet_text.write('Created at: ' + str(status.created_at) + ' by @' + status.user.screen_name + " (screen name: " + status.user.name + ")\n")
        create_tweet_text.write('Location: ' + str(status.place) + " , " + str(status.coordinates) + "\n")
        create_tweet_text.write('From: ' + status.source + "\n")
        create_tweet_text.write('Tweet id: ' + ids + "\n")
        # needs premium createTweetText.write('Replies: ' + str(status.reply_count)
        create_tweet_text.write("Likes: " + str(status.favorite_count) + "\nRetweets: " + str(status.retweet_count))
