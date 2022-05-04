#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Import library
import requests
import json
import argparse
import logging


## Logging
logging.basicConfig (filename = "shyin_homework1_log.txt", level = logging.INFO, format = "%(asctime)s-[%(process)d][%(thread)d]|[%(levelname)s]|[%(filename)s:%(lineno)d][%(funcName)s]|%(message)s")

## Defination of argparse
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--keyword", dest = "keyword", help = "keyword", required = True)
parser.add_argument("-l", "--limit", dest = "limit", help = "limit", default = 50, required = False)

def Crawls_result(crawls_keyword, crawls_limit) :
    
    crawls_url = "https://shopee.tw/api/v4/search/search_items" 

    crawls_header = {
        ## Avoid IP getting block
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "x-api-source" : "pc",
        ## Get keyword from user
        "referer" : "https://shopee.tw/search?keyword=%s" % (crawls_keyword)
    }

    ## Get limit from user

    crawls_params = {
        "keyword" : crawls_keyword,
        "page_type" : "search",
        "scenario" : "PAGE_GLOBAL_SEARCH",
        "limit" : crawls_limit,
        "version" : 2

    }

    crawls_payload = {

    }

    crawls_response = requests.get(url = crawls_url, headers = crawls_header, params = crawls_params, data = crawls_payload)
    if "item_basic" in crawls_response.text :
        print("Status Code : {} successful".format(crawls_response.status_code))
        print ("Total result : {}".format(crawls_limit))
        #print ("Response : {}".format(crawls_response.text))
        print("----------  ----------  ----------  ----------  ----------")
        ## Logging
        logging.info ({"Status code": crawls_response.status_code})
        logging.info ({"crawls_limit": crawls_limit, "keyword": crawls_keyword})
        #logging.info (crawls_response.text)
    elif '"total_count":0' in crawls_response.text :
        print("Status Code : {} successful".format(crawls_response.status_code))
        print ("Response : Keyword not found \n{}".format(crawls_response.text))
        ## Logging
        logging.info ({"Status code": crawls_response.status_code})
        logging.error ({"crawls_limit": crawls_limit, "keyword": crawls_keyword})
        logging.error (crawls_response.text)
    elif crawls_response.status_code != 200 :
        print ("Status Code : {} failed".format(crawls_response.status_code))
        print ("Response : {}".format(crawls_response.text))
        ## Logging
        logging.error ({"Status code": crawls_response.status_code})
        logging.error ({"crawls_limit": crawls_limit, "keyword": crawls_keyword})
        logging.error (crawls_response.headers)
        logging.error (crawls_response.text)
        exit ()
        

    crawls_print_result = crawls_response.json()
    
    crawls_print_result_sort = [] 

    
    for product in crawls_print_result ["items"] :

        itemid = product["item_basic"]["itemid"]
        historical_sold = product["item_basic"]["historical_sold"]
        crawls_print_result_sort += [[str(itemid), int(historical_sold) ]]

    crawls_print_result_sort_result = sorted(crawls_print_result_sort, key=(lambda x:x[1]), reverse = True)

    ## Enumerate : display the the index of a list element
    for (index, product) in (enumerate(range(len(crawls_print_result_sort_result)), start = 1 )) :
        ## Print in 1 line, python2 need added with "," in print behind
        print("The number "+ str(index)),
        print(" item id is "+ crawls_print_result_sort_result[product][0]),
        print(" with sales amount "+ str(crawls_print_result_sort_result[product][1]))

        ## Logging
        #logging.info ("The number "+ str(index) + " item id is " + str (crawls_print_result_sort_result[product][1]) + " with sales amount " + str (crawls_print_result_sort_result[product][1]))
        logging.info ({'itemid': crawls_print_result_sort_result[product][0] , 'historical_sold': str(crawls_print_result_sort_result[product][1])})

if __name__ == "__main__" :
    args = parser.parse_args()
    crawls_keyword = args.keyword
    crawls_limit = args.limit
    Crawls_result(crawls_keyword, crawls_limit)
