import importlib
import requests
import sys
import os
import logging
from logging import FileHandler, DEBUG
import ntpath
from getwebdir import scrape_file_list_from_URL
from urllib.parse import urljoin

def main(argv):
    if len(sys.argv) < 5:
        sys.exit("Usage: %s <waf_directory> <waf_url> <file_type> <log_file_path> <harvest_subdirectories_flag>" % argv[0])
    else:
        waf_directory = argv[1]
        waf_url = argv[2]
        file_type = argv[3]
        log_file_path = argv[4]
        harvest_subdirectories_flag = argv[5] == "true"

	# Create waf directory if it doesn't exist
        if not os.path.exists(waf_directory):
            os.makedirs(waf_directory)

        logging.basicConfig(filename=log_file_path,level=logging.DEBUG)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        for filename in scrape_file_list_from_URL(waf_url, file_type, harvest_subdirectories_flag):
            logging.debug(filename)
            if file_type in filename:
                file_url = filename
                logging.debug("Connecting to: " + file_url)
                file_request = try_request(file_url,1,20)
                if file_request is not None:
                    path, file = ntpath.split(filename)
                    output_file = os.path.join(waf_directory, file)
                    if os.path.isdir(waf_directory):
                        logging.debug("Writing: " + output_file)
                        open(output_file, 'wb').write(file_request.content)                        
                    else:
                        logging.error("Failed to copy file: " + output_file)

def try_request(file_url, num_tries, num_retries):
    try:
        return requests.get(url=file_url)
    except Exception:
        num_tries += 1
        if num_tries < num_retries:
            logging.warning("Failed to retrieve data for: " + file_url + ". Trying again.")
            time.sleep(1)
            return try_request(file_url, num_tries, num_retries)
        else:
            logging.error("Failed to retrieve data for: " + file_url + ". Too many attempts have failed to try again.")
            return None

if __name__ == "__main__":
    main(sys.argv[0:])       
 
