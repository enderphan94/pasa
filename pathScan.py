import re
from sys import argv
from os.path import exists
import optparse
import argparse
import sys
import os
import requests
import re
import progressbar
from time import sleep

parser = argparse.ArgumentParser()

parser.add_argument(
    '-u',
    '--url',
    help='Input URL You Want To Scan',
    required=True)

args = parser.parse_args()

url = args.url

def main():
	dic = open("dicc.txt",'r')
	array_dir = []
	array_file= []
	array_ban = []
	count = 0
	total = 0
	for pay in dic.readlines():
		total = total + 1
	dic.seek(0)
	bar = progressbar.ProgressBar(maxval=total, \
    		widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	for count in xrange(total):
		for line in dic.readlines():
			count = count + 1
			bar.update(count)
			sleep(0.1)
			try:
				word = line.strip("\n")
				tgturl = url + word
				req = requests.get(tgturl, timeout=10)	
				if req.status_code == 200:
					if "Index of" in req.content:
						array_dir.append(word)
					else:
						array_file.append(word)
				elif req.status_code == 403:
					array_ban.append(word)
				#elif req.status_code == 404:
				#	print "[-] whoops! The server has not found anything matching the URI given"
			except:
				print "[-] Nothing found"	
	bar.finish()
	for sub_dir in array_dir:	
		print "[+] Folder has been found: "+url+sub_dir
	for sub_file in array_file:
		print "[+] File is readable: "+url+sub_file
	for sub_ban in array_ban:
		print "[-] Folders/files are forbidden:"+url+sub_ban

if __name__ == "__main__":
	main()
