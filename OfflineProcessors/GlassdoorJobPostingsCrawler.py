from bs4 import BeautifulSoup, SoupStrainer  # For HTML parsing
import urllib2  # Website connections
import re  # Regular expressions
from time import sleep  # To prevent overwhelming the server between connections
import pandas as pd  # For converting results to a dataframe and bar chart plots
import sqlite3
from urllib2 import Request, urlopen
from JobRecommenderSystem.OfflineProcessors.JobListingUrls import finance as f_url
from JobRecommenderSystem.OfflineProcessors.JobListingUrls import information_technology as it_url
from JobRecommenderSystem.OfflineProcessors.JobListingUrls import telecommunication as t_url
from JobRecommenderSystem.OfflineProcessors.JobListingUrls import health_care as hc_url
from JobRecommenderSystem.OfflineProcessors.JobListingUrls import insurance as in_url
from JobRecommenderSystem.OfflineProcessors.JobListingUrls import more_items

from JobRecommenderSystem.libs import DatabaseProvider as db

import time

headers = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"

def __drop_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS job_listings')

def __create_job_listings_table(create):
    if create:
        connection = db.get_db();
        cursor = connection.cursor();
        __drop_table(cursor)
        cursor.execute('CREATE TABLE job_listings(sector TEXT, company_name TEXT, location TEXT, url TEXT, job_description TEXT)')
        cursor.close()
        connection.close()

def __insert_record(cursor, sector, company_name, location, url, description):
    cursor.execute(
        'INSERT OR REPLACE INTO job_listings (sector, company_name, location, url, job_description) VALUES(?, ?, ?, ?, ?)',
        (sector, company_name, location, url, description))

def __get_JobView(soup):
    return soup.find("div", {"id" : "JobView"})

def __get_emp_info(soup):
    return soup.find("div", {"class" :"empInfo tbl"})

def __get_emp_name(soup):
    emp_name = soup.find("span", {"class" : "strong ib"})
    if emp_name:
        return emp_name.text.encode('ascii', 'ignore').strip()
    return None

def __get_emp_location(soup):
    loc = soup.find("span", {"class" : "subtle ib"})
    if loc:
        loc = loc.text.encode('ascii', 'ignore')
        return loc
    return None

def __get__JobDescription(soup):
    item = soup.find("div", {"id": "JobContent"})
    return item.find("div", {"class": "jobDescriptionContent desc"})

def __clean_JobDescription(job_description):
    if job_description:
        return job_description.get_text(separator='\n').encode('ascii', 'ignore')
    return None

def __clean_location(location):
    return location

def crawl_and_populate_db(base_url, url, header, sector):
    q = Request(url)
    q.add_header("User-Agent", header)
    connection = db.get_db();
    cursor = connection.cursor();
    try:
        html = urllib2.urlopen(q).read()
        soup = BeautifulSoup(html, "html.parser")
        items = soup.findAll("ul", {"class": "jlGrid hover"})
        job_URLS = [base_url + link.get('href') for link in items[0].findAll('a', href=True)]
        print "count of Job URLs %d" % len(job_URLS)
        for url in job_URLS:
            time.sleep(2);
            q = Request(url)
            q.add_header("User-Agent", header)
            html = urllib2.urlopen(q).read()
            soup = BeautifulSoup(html, "html.parser")
            job_view_soup = __get_JobView(soup)
            emp_info_soup = __get_emp_info(job_view_soup)
            emp_name = __get_emp_name(emp_info_soup)
            loc = __get_emp_location(emp_info_soup)
            loc = __clean_location(loc)
            job_description = __get__JobDescription(job_view_soup)
            job_description = __clean_JobDescription(job_description)
            __insert_record(cursor, sector, emp_name, loc, url, job_description)
            connection.commit()
    except urllib2.HTTPError, e:
        print e.code
        print e.msg
        print e.fp.read()
    finally:
        cursor.close()
        connection.close()


def __create_job_listings_for_finance():
    for url in [li['url'] for li in f_url]:
        print "using url %s" % url
        crawl_and_populate_db(base_url, url, headers, "Finance")

def __create_job_listings_for_IT():
    for url in [li['url'] for li in it_url]:
        print "using url %s" % url
        crawl_and_populate_db(base_url, url, headers, "Information Technology")

def __create_job_listings_for_telecommunication():
    for url in [li['url'] for li in t_url]:
        print "using url %s" % url
        crawl_and_populate_db(base_url, url, headers, "Telecommunications")

def __create_job_listings_for_health_care():
    for url in [li['url'] for li in hc_url]:
        print "using url %s" % url
        crawl_and_populate_db(base_url, url, headers, "Health Care")

def __create_job_listings_for_insurance():
    for url in [li['url'] for li in in_url]:
        print "using url %s" % url
        crawl_and_populate_db(base_url, url, headers, "Insurance")


if __name__ == '__main__':
    base_url = "https://www.glassdoor.com/"
    #__create_job_listings_table(True)
    #__create_job_listings_for_finance()
    #__create_job_listings_for_IT()
    #__create_job_listings_for_telecommunication()
    #__create_job_listings_for_health_care()
    #__create_job_listings_for_insurance()
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&" \
          "typedKeyword=Vmware&sc.keyword=Vmware&locT=C&locId=1147431&jobType="
    crawl_and_populate_db(base_url, url, headers, "Information Technology")



