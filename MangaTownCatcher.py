"""Script to Download Mangas from MangaTown"""

import os
import time
import requests
import re
from cbzarchiver import makecbz

#SEARCH FOR # TO FIND ALL COMMENTS

HEADERS = requests.utils.default_headers()
HEADERS.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",})

if os.name == "nt":
    SLASH = "\\"
else:
    SLASH = "/"

def get_file(srcfile, srcurl, counter=0, ftype=0):#ftype indicates if picture or not
    """Function to Downloadad and verify downloaded Files"""
    if counter == 5:
        print("Could not download File:", srcfile, "in 5 attempts")
        return 1
    counter = counter + 1
    if not os.path.isfile(srcfile):
        time.sleep(5) # why wait 5 secs? because it'll make you "look" like neither a bot/script nor like a reading human 
        print("Downloading", srcurl, "as", srcfile)
        with open(srcfile, "wb") as fifo:#open in binary write mode
            response = requests.get(srcurl, headers=HEADERS)#get request
            #print("\n\n\n", response.headers,"\n\n\n") # check against actual filesize
            fifo.write(response.content)#write to file
        if int(str(os.path.getsize(srcfile)).strip("L")) < 10000 and ftype: #Assumes Error in Download and redownlads File
            print("Redownloading", srcurl, "as", srcfile)
            autocleanse(srcfile)
            return get_file(srcfile, srcurl, counter)
        else: #Assume correct Filedownload
            return 0
    else:
        if int(str(os.path.getsize(srcfile)).strip("L")) < 10000 and ftype: #Assumes Error in Download and redownlads File
            print(srcfile, "was already downloaded but the filesize does not seem to fit -> Redownl0ading")
            autocleanse(srcfile)
            return get_file(srcfile, srcurl, 0)
        else: #Assume correct Filedownload
            print("File was downloaded correctly on a previous run")
            return 0

def autocleanse(cleansefile):
    """ Function for safer deleting of files """
    if os.path.exists(cleansefile):
        os.remove(cleansefile)
        return
    else:
        print("File", cleansefile, "not deleted, due to File not existing")
        return

def init_preps():
    """Function to initiate the Download Process"""
    cwd = os.path.dirname(os.path.realpath(__file__)) + SLASH
    os.chdir(cwd)
    print("Recommended URL-Format would be: http://www.mangatown.com/manga/log_horizon/\n")
    #inputurl = str(input("Please enter the URL of the Manga you want to download: "))
    inputurl = "http://www.mangatown.com/manga/log_horizon/"#cm
    firstchapter = int(float(input("Please enter the Number of the first Chapter you want: ") or 1))
    lastchapter = int(float(input("Please enter the Number of the last Chapter you want: ") or 1))

    indexfile = cwd + "indexfile.html"
    manganame = inputurl.split("/")[4].replace("_s_", "s_").replace("_", " ").replace(":", " -").title()
    mangadir = cwd + manganame + SLASH
    chapterlist = []
    if not os.path.exists(mangadir):
        os.mkdir(mangadir)

    get_file(indexfile, inputurl)

    regex = re.compile(r"c\d+")

    with open(indexfile, "r") as inde:
        print("opened file")
        inchapter = False
        for line in inde:
            line = str(line)
            chapterurl = ""
            if "chapter_content" in line:
                inchapter = True
                print("true", inchapter)
            if "<a href=" in line and inchapter:
                print("foundlink")
                chapterurl = "http://" + line.split("\"//")[1].split("\">")[0]
                chapter = int(regex.findall(chapterurl)[0].split("c")[1].split("/")[0])
                print("Chapter", chapter, ":\t", chapterurl)
                chapterdir = mangadir + "Chapter " + str(chapter) + SLASH
                chapterlist.append([chapter, chapterurl, chapterdir])
            if "comment_content" in line and inchapter:
                inchapter = False
                print("eof")

    autocleanse(indexfile)
    chapterlist.reverse()
    for chapter in chapterlist:
        if chapter[0] >= firstchapter and chapter[0] <= lastchapter:
            if not os.path.exists(chapter[2]):
                os.mkdir(chapter[2])
            print("Url:", chapter[1])
            print("Chapterdir:", chapter[2])
            retrieve_chapter(chapter[1], chapter[2])
            print("making dat shit cbz")
    makecbz(mangadir)
    exit(0)

def retrieve_chapter(chapterurl, chapterdir):
    """ Function to download Volumes"""

    chapterfile = chapterdir + "chapter.html"
    get_file(chapterfile, chapterurl)
    maxpages = 0
    with open(chapterfile, "r") as chap:
        for line in chap:
            line = str(line)
            if "<option value=\"" in line and not "Featured" in line:
                option = int(line.split("\">")[1].split("<")[0])
                if option > maxpages:
                    maxpages = option
    print("Maxpages:", maxpages)
    autocleanse(chapterfile) # uncomment
    for x in range(1, maxpages + 1):
        pageurl = chapterurl + str(x) + ".html"
        pagefile = chapterdir + str(x) + ".html"
        retval = retrieve_page(pageurl, pagefile, chapterdir, str(x))
        print("retval for page", x, "is:", retval)
        pageurl = ""
        pagefile = ""
    return 0

def retrieve_page(pageurl, pagefile, chapterdir, itera):
    """ Function to Download all images of a Chapter """
    retval = -1
    get_file(pagefile, pageurl)
    imgbool = False
    with open(pagefile, "r") as pgf:
        for line in pgf:
            if "read_img" in line:
                imgbool = True
            if "<img src=\"" in line and "id=\"image\"" in line and imgbool:
                imgurl = line.split("src=\"")[1].split("\" ")[0]
                print(imgurl)
                imgfile = chapterdir + "Page " + str(itera) + ".jpg"
                retval = get_file(imgfile, imgurl, 0, 1)
    autocleanse(pagefile)
    return retval

def main():
    """MAIN"""
    os.umask(0)
    init_preps()
main()

###########################################################
# *Documentation*
#Chapterlist Structure:
#Type: List
#each entry is a "Volume" that contains
#chapterlist[0]: Volume's Number (ex.: Volume 6)
#chapterlist[1]: Link of Chapter
#chapterlist[2]: Directory that the Volume will be saved in
###########################################################
