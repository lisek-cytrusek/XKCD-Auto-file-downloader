import urllib.request
import os
import getpass
import schedule
import time

user = getpass.getuser()


def content():
    frontpage = urllib.request.urlopen('http://xkcd.com')
    pagecontent = str(frontpage.read())
    return pagecontent


def getlink(page):
    # znajduje poczatek linku
    linkstart = page.find('this comic: ')
    # znajduje koniec linku
    linkend = page.find('<br />\\nImage URL')
    # oddaje gotowy link (pomiedzy poczatkiem a koncem)
    thelink = page[linkstart + 12:linkend-1]
    return thelink


def gettitle(page):
    titlestart = page.find('<div id="ctitle">')
    titleend = page.find('</div>\\n<ul class="comicNav">')
    thetitle = page[titlestart+17:titleend]
    return thetitle


def getpicture(page):
    picturestart = page.find('embedding')
    pictureend = page.find('<div id="transcript"')
    thepicture = page[picturestart+12:pictureend-2]
    return thepicture


def gethovertext(page, thetitle):
    picturestart = page.find('embedding')
    pictureend = page.find('<div id="transcript"')
    thepicture = page[picturestart + 18:pictureend - 2]
    starttext = 'n<div id="comic">\\n<img src="{}" title="'.format(thepicture)
    lentextstart = 29 + len(thepicture) + 9
    textstart = page.find(starttext)
    textfin = '" alt="{}'.format(thetitle)
    textend = page.find(textfin)
    thetext = page[textstart+lentextstart:textend]
    return thetext


def savehovertextastxt(number, title, text, path):
    truetitle = number + " " + title
    completename = os.path.join(path, truetitle + '.txt')
    with open(completename, 'w+') as f:
        f.write(text)


def checkfolder():
    filepath = '/home/{}/Desktop/xkcd/'.format(user)
    xkcd = os.path.dirname(filepath)
    if not os.path.exists(xkcd):
        os.makedirs(xkcd)
    return xkcd


def getpath():
    mypath = '/home/{}/Desktop/xkcd/'.format(user)
    return mypath


def eng():
    checkfolder()
    page = content()
    thepath = getpath()
    thelink = getlink(page)
    thetitle = gettitle(page)
    thepicture = getpicture(page)
    text = gethovertext(page, thetitle)
    thenumber = thelink.split('/')[-1]
    fullfilename = os.path.join(thepath, thenumber + " " + thetitle + '.png')
    savehovertextastxt(thenumber, thetitle, text, thepath)
    urllib.request.urlretrieve(thepicture, fullfilename)


schedule.every().monday.at("12:00").do(eng)
schedule.every().wednesday.at("12:00").do(eng)
schedule.every().friday.at("12:00").do(eng)
while True:
    schedule.run_pending()
    time.sleep(1)
