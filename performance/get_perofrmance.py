#!/usr/bin/python
# usage: get_performance.py <url> <url> ...
import sys
from datetime import datetime
from time import sleep
import subprocess
from multiprocessing import Pool
import signal
import ctypes

def init_worker():
	signal.signal(signal.SIGINT, signal.SIG_IGN)

def curl_tt_to_file(url):
	
	file_name=url.split("//")
	print(url)
	terminate_process = False
	while not terminate_process:
		try:
			with open('stats_%s.csv' % file_name[-1], 'a+') as csvfile:
				arg = ['curl', 
					'-s',
					'-w',
					'"%{time_total}\n"',
					'-o',
					'/dev/null',
					url
					]
				p = subprocess.Popen(arg, stdout=subprocess.PIPE, 
									   stderr=subprocess.PIPE)
				out, err = p.communicate()
				csvfile.write('"%(ts)s",%(sec)s' % {
					"ts": str(datetime.now())[:16], "sec": out[1:-1]})
				csvfile.close()
				print("running %(url)s %(dt)s" % {"url": url, "dt": str(datetime.now())})
				sleep(60)
		except KeyboardInterrupt:
			print("terminating...")
			terminate_process = True
		

def main(argv):
	if len(argv) < 3:
		print("please pass 2 urls (ie: python get_perofrmance.py https://ww5.welcomeclient.com http://10.1.100.49 )")
		sys.exit()
	    
	try:
		urls = argv[1:]
		print urls
		url_count=(len(argv)-1)
		print url_count
		pool = Pool(processes=url_count)
		mp = pool.map_async(curl_tt_to_file, urls)
		pool.close()
		pool.join()
		print("done: %s" % mp)
	
	except KeyboardInterrupt:
		print("terminating process...")
		pool.terminate()
		pool.join()

		
	
if __name__ == "__main__":
	main(sys.argv)