import requests
import sys
import argparse
import threading

# Algebraic Laws:
# response status == 200-400 AND url != response.url ---> print [url]/[word]
# response status 404                                ---> return null.
# response status 403 (possible directory)           ---> print and recurse: urlmap([url]/[word]) 
# response status 405 (method not allowed)           ---> print [url]/[word]
# response status 401 OR 407                         ---> print [url]/[word]
def req(URL):
	r = requests.get(URL)
	if (r.status_code < 400 or r.status_code == 405 or r.status_code == 401 or r.status_code == 407) and URL != r.url:
		print(str(r.status_code) + ": " + URL + "\n")
	elif r.status_code == 403:
		print(str(r.status_code) + ": " + URL + "\n")
		urlmap(URL)


# prints all files found in the provided domain
# 
# For each word in wordlist, try to connect to [url]/[word]:
# 

def urlmap(URL, maxThreads):
	# Parameter type: string
	# return type   : null 
	threads = []

	with open('wordlist.txt') as wordlist:
		for word in wordlist:
			with open('extensions.txt') as extensions:
				for ext in extensions:
					if threading.active_count() <= maxThreads:
						t =  t1 = threading.Thread(target=req, args=(URL + "/" + word + ext,))
						threads.append(t)
						t.start()
					else:
						req(URL + "/" + word + ext)

	for thrd in threads:
		thrd.join()

	return


ogURL = sys.argv[1]

try:
	r = requests.get(ogURL)

	if r.ok:
		print("Beginning scan\n")
		maxThreads = 10

		if sys.argv[2]:
			try:
				maxThreads = int(sys.argv[2])
			except:
				print("Unable to parse [MAX THREADS] argument correctly. Defaulting to 10.\n")

		else:
			print("Defaulting to 10 threads.\n")

		# valid url 
		urlmap(ogURL, maxThreads)

	else:
		print("Cannot GET specified webfile from host: responded with status " + str(r.status_code))

except requests.exceptions.RequestException: 
	print("Cannot GET provided target (malformed url).\nUSAGE: python urlmap.py [target] [max threads (optional)]")

except KeyboardInterrupt:
	print("Quitting Scan")