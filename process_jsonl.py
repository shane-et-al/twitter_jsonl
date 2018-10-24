import io
import json
import csv
import os

fields = ["created_at", "id", "full_text", "in_reply_to_user_id", "user__id", "user__name", "user__screen_name", "user__location", "user__description", "user__followers_count", "user__friends_count", "user__created_at", "user__favourites_count", "user__utc_offset",
          "user__time_zone", "user__geo_enabled", "user__verified", "user__statuses_count", "user__lang", "user__is_translator", "user__is_translation_enabled", "user__translator_type", "geo", "coordinates", "place", "retweet_count", "favorite_count", "lang"]

filenames = [input("Enter filename: ")]
if filenames[0]=="":
    filenames = [f for f in os.listdir('.') if os.path.isfile(f)]
for filename in filenames:
    if filename[-5:] != "jsonl":
        continue
    print("Processing ",filename,"...")
    tweets = []
    f = open(filename)
    for line in f:
        tweet = {}
        j = json.loads(line)
        for field in fields:
            target = j
            for i in field.split("__"):
                if i == "full_text" and i not in target and "text" in target:
                    # Failover to Twitter API compatibility mode "text" field
                    i = "text"
                try:
                    target = target[i]
                except ValueError:
                    print("ERROR: specified field '",field, "'was not found in JSON line:\n",line)
            tweet[field] = target
        tweets.append(tweet)

    with open(filename+'.csv', 'w') as outfile:
        w = csv.DictWriter(outfile, fields, delimiter=',',
                        escapechar='\\', quoting=csv.QUOTE_ALL, lineterminator='\n')
        w.writeheader()
        for tweet in tweets:
            for key in tweet.keys():
                tweet[key] = str(tweet[key]).replace(
                    "\n", "\\n").replace("\r", "\\n")
            w.writerow(tweet)
