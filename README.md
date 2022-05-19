# Music recommender
## To run this shitty dumb project
T push ca file /venv len vi t bi dieng
If cannot directly `manage.py runserver` this project then delete the folder /venv.

Then again recreate a new virtual environment
`python3 -m venv venv`
and activate it by `source venv/bin/activate`.

Install bunch of packages:

`pip3 install django djangorestframework numpy scipy matplotlib scikit-learn pandas`

Remember this shit:
```pip3 install spotipy```
___
## What is wrong right now
- Templates is messed up: Fucked up when tried to use `extends`. Can't `import` properly anymore.
___

## What to do next
- Display the recommend.html template with playlist.html data (??how about pass another parameter to recommend_detail view and requery song_list from song?)
- List danh sach cac sample playlist ra tu database 
- Click on each sample playlist's button -> switch to the corresponding detail display page
- Click on 'Recommend' button to switch to recommend template
- Display Sample name + description below
- Display song with artist and released year below 
___

## What can be extended
- Playable music
- Edit (add, remove) playlist by searching song name -> return list of song with details about artist, year
- Use restAPI to be faster and to look smarter
- Improve this ugly design??
___
## What fun haha
`sudo apt install sqlite3`

`sqlite3 db.sqlite3` to do sql stuff