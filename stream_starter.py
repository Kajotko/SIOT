#Script to start a twitter stream with retrying

import time
while True:
    try:
        execfile("twitter_stream.py")
    except:
        time.sleep(60)  # wait before retrying to avoid rate limiting
        continue