# -*- coding: utf-8 -*-
import os
import shutil
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def ReadCSV(FilePath):
	fp = open(FilePath,'r')
	AllData = []
	for line in fp.readlines():


