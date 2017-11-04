#!/bin/env python
import os
# import sys
import shutil
import re
import pprint
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class hsSorter(object):

    SERIES = set()  # type: set

    def __init__(self, folder):
        self.folder = folder
        self.horribleSubsRegex = re.compile(r'(\[HorribleSubs\]' +
                                            r'\s+(.*)' +  # Series name, group2
                                            r'(\s)?-(\s)?' +
                                            r'(\d\d)' +  # Chapter number,group4
                                            r'(\d)?(\s)?(\[\d+p\])' +
                                            r'(.mkv|.mp4))', re.VERBOSE)

    def getSeriesFolders(self):
        for f in os.listdir(self.folder):
            if re.search(self.horribleSubsRegex, f):
                name = re.search(self.horribleSubsRegex, f).group(2)
                name = name.strip(' ')
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
