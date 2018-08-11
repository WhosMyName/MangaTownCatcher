## Why To Use

MangaTownCatcher was created for those people:
* This special kind of people who would like to read/archive their favorite Mangas offline.
* For People who don't have a always perfect/working Internet Access or just want to bulk-download Mangas.

Mangafox got renamed to [MangaTown](http://www.mangatown.com/)  
Well idk :shrug:, Script got fixed...  

## Requirements

### Requirements \*nix

* Install Python3 via your package manager
* Install requests via python3 -m pip install requests
* Download or Clone this Repo

### Requirements Windows

* Download and Install Python3 from [Python Downloadpage](https://www.python.org/downloads/release/python-360/)  
add Python3 to PATH during installation and disable Path-Limit
* Install requests via python -m pip install requests
* Download or Clone this Repo

## How to use

### \*nix
* open Terminal, cd to Script-Path, python3 MangaTownCatcher.py

>*Exit via Ctrl + C*

### Windows
Either open Directory in CMD and execute python MangaTownCatcher.py or double-click to open:
* open Terminal, cd to Script-Path, python MangaTownCatcher.py

>*Exit via Ctrl + C*

### How MangaTownCatcher works

* It will take your Input, parse it and download all relevant Files from MangaTown
* After parsing those Files, it will poroceed to download the Imagefiles
* It will quit automatically or you can, if you want stop it midway using *Ctrl + C*

>**Note:** *I added time.sleep(5) to prevent the Script from triggering the Chaptcha Mechanism/Bot Detection.*  

>**Note:** *Additionally I might have added a Download-Limit of 5 to prevent the Script from downloading all Chapters in parallel.  
This Feature can be disabled by changing the Value of LIMIT to some Value fitting for your use.*

```python
LIMIT = 5 #<-------------- YourValueHere
```
