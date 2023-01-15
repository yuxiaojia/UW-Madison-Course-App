__author__ = "Jarvis Jia"
__credits__ = ["Peter Bryant", "Jarvis Jia", "Bryan Li", "Swathi Annamaneni", "Aidan Shine"]
__version__ = "1.0.0"
__maintainer__ = "Jarvis Jia"

#!/usr/bin/python3
import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint

def ScrapeCourses():

    """
    Function to scrape the courses from UW-Madison course guide page

    """
    # Set up the url from UW-Madison course guide page 
    url = 'https://guide.wisc.edu/courses/acct_i_s/'

    # scrape the overall data from requests
    data = requests.get(url)

    my_data = []

    # beautiful soup package to scrape the page
    soup = BeautifulSoup(data.text, 'html.parser')

    # select the articles from page
    articles = soup.select('p')

    # open a file to store the course information
    f = open("test_file.json", "w")
    i = 0
    j = 0
    my_dict = {}
    nested_dict = {}

    # Loop through each course
    for link in soup.find_all('p'):
        current_dict = {}
        i = i + 1

        # get the course name
        if i == 1:
            my_dict['name'] = link.get_text().replace(u'\xa0', u'').replace(u'\u200b', u'').replace(u'\xa9', u'').replace(u'\u2022', u'').replace(u'\n', u'').replace(u'\u2014', u'')

        # get the course credits
        if i == 2 : 
            my_dict['credits'] = link.get_text().replace(u'\xa0', u'').replace(u'\u200b', u'').replace(u'\xa9', u'').replace(u'\u2022', u'').replace(u'\n', u'').replace(u'\u2014', u'')

        # get the course description
        if i == 3 : 
            my_dict['description'] = link.get_text().replace(u'\xa0', u'').replace(u'\u200b', u'').replace(u'\xa9', u'').replace(u'\u2022', u'').replace(u'\n', u'').replace(u'\u2014', u'')

        # get the course requisite
        if i == 4 : 
            my_dict['requisite'] = link.get_text().replace(u'\xa0', u'').replace(u'\u200b', u'').replace(u'\xa9', u'').replace(u'\u2022', u'').replace(u'\n', u'').replace(u'\u2014', u'')

        # get the course last taught information
        if 'Last Taught' in link.get_text().replace(u'\xa0', u'').replace(u'\u200b', u'').replace(u'\xa9', u'').replace(u'\u2022', u'').replace(u'\n', u'').replace(u'\u2014', u''):
            my_dict['last taught'] = link.get_text().replace(u'\xa0', u'').replace(u'\u200b', u'').replace(u'\xa9', u'').replace(u'\u2022', u'').replace(u'\n', u'').replace(u'\u2014', u'')
            i = 0
            j = j + 1
            current_dict[f'class{j}']   = my_dict
            #nested_dict.update(current_dict)
            with open("test_file.json", "a") as outfile:
                json.dump(current_dict,  outfile, indent = 4)
            outfile.close()
            break

if __name__ == '__main__':
    ScrapeCourses()