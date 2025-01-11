#!/bin/python3

import praw
import re
import urllib.request
import pyvips
import os
import math
from dotenv import load_dotenv

load_dotenv()

SIZE = 2048
WIDTH = 8
HEIGHT = 8
CELL_SIZE = SIZE / WIDTH
if (input("download top images? (y/N): ") == "y"):
  reddit = praw.Reddit(
    # client_id="XmjPO5BB5aLW5Dub3Npm8A",
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent="python:birdification:v1.0 (by u/johncraft2003)"
  )

  def download(url, name):
    urllib.request.urlretrieve(url, name)

  submissions = reddit.subreddit("birdification").top(limit=WIDTH * HEIGHT, time_filter="month")
  s = False
  for k, i in enumerate(submissions):
    # print(f"{k + 1}: {i.url}")
    if (re.match("https://i\.redd\.it/[a-zA-Z0-9]+\.(jpeg|png)", i.url)):
      # print("valid")
      download(i.url, f"images/{k}.jpeg") # assume jpeg since its the majority 
    else:
      print(f"found controversial post: {i.title} ({i.url}). ignoring for now")
      s = True

  if (s):
    while True:
      inp = input("not all posts could be downloaded, proceed? (pro tip: use this time to download them manually) (y/n): ")
      if (inp == "n"):
        exit()
      if (inp == "y"):
        break

imgs = [os.path.join("images", f) for f in os.listdir("images")
        if os.path.isfile(os.path.join("images", f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if not imgs:
  print("confusion!!!!!!!!!!! no images????")
  exit()

# assuming tiles are squared
canvas = pyvips.Image.black(SIZE, SIZE)

for k, i in enumerate(imgs):
  try:
    image = pyvips.Image.new_from_file(i, access="sequential")
    image = image.resize(CELL_SIZE / image.width, vscale=CELL_SIZE / image.height)

    index = int(os.path.basename(i).split(".")[0])
    x = index % HEIGHT
    y = math.floor(index / WIDTH)
  
    canvas = canvas.insert(image, x * CELL_SIZE, y * CELL_SIZE)
  except Exception as e:
    print(f"FAILITION!!!!!!! {i}: {e}")

canvas.write_to_file("output.png")
print(f"success")