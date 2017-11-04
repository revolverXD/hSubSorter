#!/bin/env python
import os
import shutil
import re
import pprint
import logging
import pdb
import bs4
import requests
import subprocess


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.INFO)


class hsSorter(object):

    SERIES = set()  # type: set
    MAGNET_REGEx = re.compile(r'((<link>)(.*))')

    def __init__(self, folder):
        self.folder = folder
        self.horribleSubsRegex = re.compile(r'(\[HorribleSubs\]' +
                                        r'\s+(.*)' +  # Series name, group2
                                        r'(\s)?-(\s)?' +
                                        r'(\d\d)' +  # Chapter number,group5
                                        r'(\d)?(\s)?(\[\d+p\])' +
                                        r'(.mkv|.mp4))', re.VERBOSE)

    def getSeriesFolders(self):
        for f in os.listdir(self.folder):
            if re.search(self.horribleSubsRegex, f):
                name = re.search(self.horribleSubsRegex, f).group(2).strip(' ')
                self.SERIES.add(name)
        logging.info('Those are the unique series the script found: %s '
                    % pprint.pformat(self.SERIES))

    def createSeriesFolders(self):
        for name in self.SERIES:
            dirName = str(os.path.join(self.folder, name))
            if os.path.isdir(os.path.join(self.folder, name)):
                print("%s already exist, won't create it again"
                      % dirName)
            else:
                logging.info("I will create the following dir %s" % dirName)
                os.makedirs(os.path.join(self.folder, name))

    def moveFiles(self):
        os.chdir(self.folder)
        for f in os.listdir(self.folder):
            if re.search(self.horribleSubsRegex, f):
                dirName = re.search(self.horribleSubsRegex, f).group(2).strip()
                shutil.move(f, os.path.join(dirName, f))
#                 logging.info("will move %s to the new location %s" % (f, dirName))

    def findEp(self):
        os.chdir(self.folder)
        largest = 0
        for d in os.listdir(self.folder):
            if d in self.SERIES:
                sleep(1)
                os.chdir(d)
                for f in os.listdir():
                    try:
                        epNumber = re.search(self.horribleSubsRegex, f).group(5).strip(' ')
                        if int(epNumber) > largest:
                            epFile = open("lates.txt", 'w')
                            epFile.write(epNumber)
                            epFile.close()
                    except:
                        print('Debug time')
                        pdb.set_trace()
                os.chdir('..')

    def getMagnet(self):
        hsRssFeed = "http://horriblesubs.info/rss.php?res=1080"
        req = requests.request("GET", url=hsRssFeed)

        output = bs4.BeautifulSoup(req.text, features="xml")
        outut_list = list(str(output).split('</link>'))
        self.MAGNET_REGEX = re.compile(r'((<link>)(.*))')
#         magnet = []
        for i in outut_list:
#             print(re.search(self.horribleSubsRegex, i).group(1))
            try:
                if re.search(self.horribleSubsRegex, i).group(2).strip(' ') in os.listdir(self.folder):
                    print(r'transmission-remote --auth <username>:<password> --add "%s"' % str(re.search(self.MAGNET_REGEX, i).group(3).strip(' ')))
                    subprocess.call(['transmission-remote --auth <username>:<password> --add "%s"' % str(re.search(self.MAGNET_REGEX, i).group(3).strip(' '))], shell=True)
            except:
                continue
