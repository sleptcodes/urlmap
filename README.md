# urlmap
An extensive and modifiable sitemapper.

*******************************************************************************

urlmap.py

written by Mateo Hadeshian

USAGE: python3 urlmap.py [target] [max threads (optional... defaults to 10)]

*******************************************************************************

urlmap.py is an extensive and modifiable sitemapper.

For each word in wordlist.txt, tries to GET [target]/word and reports to the 
command line if an intriguing and/or unique response is received. If 403 is
received, program will recurse over [target]/word in case [target]/word is
a directory. Additionally will try adding each extension in extensions.py to
each word as well. 
