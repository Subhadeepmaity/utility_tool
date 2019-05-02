from __future__ import unicode_literals
import pafy
import time
import json
import logging
import os
import pyfiglet

logging.basicConfig(format='%(levelname)s   %(message)s', level=logging.INFO)

def youtube_log(total, recvd, ratio, rate, eta):
	pass

def youtube_downloader(link, write_directory):
	try:
		pf_obj_vd = pafy.new(link)
		
		logging.info("\t============================================================")
		logging.info("\tVideo Title: {0}".format(pf_obj_vd.title))
		logging.info("\tVideo Duration : {0}".format(pf_obj_vd.duration))

		vid = pf_obj_vd.getbest('mp4',False)

		logging.info("\tChoosen Video Stream : {0}".format(vid))
		logging.info("\tVideo Size : {0}".format(vid.get_filesize()))
		logging.info("\tInitiating download from {url}".format(url=link))

		vid.download(filepath=write_directory,callback=youtube_log)

		logging.info("\n\tDownload completed.")
		logging.info("\t============================================================")

	except Exception as ex:
		logging.exception(
	        "Exceptions while downloading the link [{0}]".format(link),
	        extra={"error_message": ex.message}
	    )
		raise

if __name__ == '__main__':
	start = time.time()
	
	f = pyfiglet.Figlet(font='doh',width=200)
	print(f.renderText('YouTube Downloader'))
	
	youtube_links_file = 'links_for_youtube.txt'
	dirName = "Videos"

	if not os.path.exists(dirName):
	    os.mkdir(dirName)
	    print("Directory " , dirName ,  " Created ")
	else:    
	    print("Directory " , dirName ,  " already exists")

	write_path = os.path.join(os.getcwd(),dirName)

	try:
		with open(youtube_links_file) as fp_links:
			for cnt, link in enumerate(fp_links):
				logging.info("{0}. Link : {1}".format(cnt+1, link))

				supply_params = {
				    'link': link,
				    'write_directory': write_path,
				}   
				
				youtube_downloader(**supply_params)

	except (IOError, EOFError) as ex:
	    logging.exception(
	        "File [{0}] Error.".format(youtube_links),
	        extra={"error_message": ex.message}
	    )
	    raise

	except Exception as ex:
	    logging.exception(
	        "Exceptions while handling File [{0}]".format(youtube_links),
	        extra={"error_message": ex.message}
	    )
	    raise
    
	done = time.time()
	elapsed = done - start
	hours, remainder = divmod(elapsed, 3600)
	minutes, seconds = divmod(remainder, 60)
	logging.info("Time elapsed : %02d:%02d:%02d" % (hours, minutes, seconds))
	print("Done..!!")
