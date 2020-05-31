# BunnysTwitterScraper

Hello there, this is my first real "program". I don't entirely know what I'm doing. I've been mostly a script kiddy (minus the hacking part), but in light of recent events, I decided to make this in order to archive tweets about the protesting.


This will download the Tweet's text, the person's Twitter handle, screen name, what they tweeted from, where they tweeted from (if available), and the tweet's current likes and retweets. Getting the number of replies requires a premium API key (which costs $$$)

If there is a photo or video attached to the tweet, youtube-dl downloads the video, and the Twitter API & wget get the photos.

The .js file, powered by Node.js and Puppeteer, opens a headless browser to get a screenshot of the tweet.

This is currently what I would call a beta. It's a 2005 Toyota Corolla with a manual transmission.
It works, but it's not exactly attractive, and setup could be a pain.


# REQUIREMENTS
This is intended for Windows. I have no clue how it will work on other platforms. It probably won't.

If you don't have a Twitter developer account / API keys, you'll need to sign up for one at https://developer.twitter.com/en/apply-for-access in order to access the API, which you need to use this program. Once you have your account, create an app (I dont think good app names and descriptions are critical), and you should have gotten a couple API keys. Hooray! 

EDIT THESE API KEYS INTO THE EMPTY STRINGS IN THE .py FILE.

If you don't have the needed modules, I REALLY recommend installing pip if you haven't already https://pip.pypa.io/en/stable/installing/



# INSTALLATION
Download this repository as a zip file, and put the files into your desired place of download.

What's a setup.py file? I don't know. So here's how you set this up.

You will need:

Python (duh, the main file is a .py file) - https://www.python.org/downloads/ - I've been using it with version 3.8, but it should maybe hopefully probably work with older-ish versions.

Node.js - https://nodejs.org/en/download/  - Juse use the Windows Installer. If you've already installed it, I hope you have a node.exe file in the directory C:\Program Files\nodejs\ AND MAKE SURE THIS IS IN WINDOWS'S PATH. I'm not sure if it comes default with the installation - instructions on how to do that are here: https://www.youtube.com/watch?v=pYvL6e4NDv4


Puppeteer - https://github.com/puppeteer/puppeteer - command to install is `npm i puppeteer` in the windows CMD (once Node.js is installed and put into Windows's PATH)


To install the needed Python modules:

In the Windows command prompt, you can type `pip install youtube-dl`, `pip install tweepy`, `pip install tld`, `pip install wget`


# HOW TO RUN
Remove the default text in the `URLs.txt` file. Paste in tweet URLs with or without the `?s=20`. There must be one URL per line, with up to as many lines as you want. An example of a valid URL would be `https://twitter.com/CrackerBarrel/status/1265628864119701504` or `https://twitter.com/CrackerBarrel/status/1265628864119701504?s=20`.

Make sure you save this URLs.txt file before using the .py or .bat file.

For me, doubleclicking on the .py file doesn't work, and I have no gosh dang idea why. To circumvent this, I've included the run.bat file. Doubleclicking that file should run the Scraper.py (assuming python.exe is in Window's PATH)

If you really want to monitor and mess with this program, I recommend loading the project into PyCharm.


If you're still having troubles after reading all of that, use problem solving skills, or create an issue or something.

Suggestions on improvements are very much welcome. Happy hoarding!













# Things to Do

Download JSON metadata, like what youtube-dl does, and make that all nice and neat.

If the original tweet author replies to their own tweet (and starts a chain of follow-up statements), automagically get all of those, and put them together in a nice way
