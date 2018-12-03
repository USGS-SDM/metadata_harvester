import requests
import io
import sys, getopt
import re
import time
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def main(argv):
        waf_url = ''
        file_extension = ''

        try:
                opts, args = getopt.getopt(argv, "hw:f:",["wafurl=", "fileextension="])
        except getopt.GetoptError:
                print('getwebdir.py -w <wafurl> -f <fileextension>')
                sys.exit(2)

        if not opts:
                print('getwebdir.py -w <wafurl> -f <fileextension>')
                sys.exit()
        if len(opts) < 2:
                print('getwebdir.py -w <wafurl> -f <fileextension>')
                sys.exit()
        for opt, arg in opts:
                if opt == '-h':
                        print('getwebdir.py -w <wafurl> -f <fileextension>')
                        sys.exit()
                elif opt in ("-w", "--wafurl"):
                        waf_url = arg
                elif opt in ("-f", "--fileextension"):
                        file_extension = arg
        print(scrape_file_list_from_URL(waf_url, file_extension, get_subdirectories))

def scrape_file_list_from_URL(waf_url, file_extension, get_subdirectories):
    link_list = set()
    request = try_request(waf_url)
    html_page_results = BeautifulSoup(request.text, 'html.parser')
    anchors = html_page_results.findAll('a')
    for item in anchors:
        anchor_link = item.get('href')
        if item.get('href').endswith('/') and (anchor_link not in waf_url) and get_subdirectories:
            subdirectory_file_list = scrape_file_list_from_URL(urljoin(waf_url, item.get('href')), file_extension, get_subdirectories)
            for filename in subdirectory_file_list:
                if file_extension in filename:
                    item_to_add = urljoin(urljoin(waf_url, item.get('href')), filename)
                    if item_to_add not in link_list:
                        link_list.add(item_to_add)
        elif item.get('href').endswith(file_extension):
            try:
                link_to_add = urljoin(waf_url, item.get('href'))
                if link_to_add not in link_list:
                    print("Adding: " + link_to_add)
                    link_list.add(link_to_add)
            except Exception as e:
                print("An error occurred: " + str(e))
        else:
            print(item.get('href'))
    return link_list

def try_request(waf_url):
    try:
        return requests.get(url=waf_url)
    except Exception:
        time.sleep(1)
        return try_request(waf_url)

if __name__ == "__main__":
   main(sys.argv[1:])            
