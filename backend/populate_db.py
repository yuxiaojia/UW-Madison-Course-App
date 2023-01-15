#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Peter Bryant, Jarvis Jia"
__credits__ = ["Peter Bryant", "Jarvis Jia",
               "Bryan Li", "Swathi Annamaneni", "Aidan Shine", "Tong Yang"]
__version__ = "1.0.0"
__maintainer__ = "Peter Bryant"
__email__ = "pbryant2@wisc.edu"
__status__ = "Development"

"""
Script to populate the database whose connection is defined in config.py.
- Database: MySQL DB hosted on AWS RDS
- Tables: courses, professors, rc (reddit comments), and teaches
- Static File Dependencies: config.py, all-courses.json, all-professors.json
- Function/Script Dependencies: madgrades.py, rmp_scrape/fetch_all.py, course_scrape/fetch_all.py
"""
# Python Standard Library Imports
import json
import time

# Python 3rd Party Imports
import praw            # PRAW: Python Reddit API Wrapper
from praw.models import MoreComments
import mysql.connector

# Custom Script Imports
import madgrades as mg  # MadGrades Script for Grade Distributions
# Public & Modified RMP API for Professor Data
from rmp_scrape.fetch_all import RateMyProfApi
import config

# Establish connection to MySQL DB
conn = mysql.connector.connect(
    user=config.user,
    password=config.password,
    host=config.host,
    database=config.database
)

# Instantiate an instance of PRAW's Reddit object
reddit = praw.Reddit(client_id=config.PRAW_client_id,
                     client_secret=config.PRAW_client_secret,
                     username=config.r_username,
                     password=config.r_password,
                     user_agent=config.PRAW_user_agent)

# Instantiate PRAW Subreddit Object for r/UWMadison
uwmadison_subreddit = reddit.subreddit('UWMadison')
reddit_url = 'https://www.reddit.com'


def pop_courses(testing=False):
    """
    Function to populate the courses table with all courses at UW-Madison. Entries contain a cUID, the course's name, 
    the course's subject, the course's code, the course's credits, and the course's description. Course data scraped from 
    guide.wisc.edu with course_scrape/fetch_all.py script, preloaded in comp_sci_test_courses.json.

    Args:
        testing (bool, optional): Whether or not to print runtime. Defaults to False.

    Returns:
        None: Populates the courses table with all courses at UW-Madison stored in the static file all-courses.json.
    """
    if testing:
        # Start a timer to measure the time it takes to populate the professors table
        start = time.time()
        print("----------pop_courses-----------")

    # file = open('./major_test_sample/major_courses.json', 'r') # Open the JSON file containing test CS courses
    # Open the JSON file containing test CS courses
    file = open('all-courses.json', 'r')

    data = json.load(file)          # Load the JSON file into a dictionary
    cursor = conn.cursor()          # Create a cursor object to execute SQL queries

    # For each course, try inserting its course data into the DB
    for key in data.keys():
        cName = data[key]['name']
        cSubject = data[key]['subject']
        cCode = data[key]['code']
        cCredits = data[key]['credits']
        cDescription = data[key]['description']
        cReq = data[key]['requisite']

        try:
            cursor.execute("INSERT INTO courses (cName, cSubject, cCode, cCredits, cDescription, cReq) VALUES (%s, %s, %s, %s, %s, %s)",
                           (cName, cSubject, cCode, cCredits, cDescription, cReq,))
            conn.commit()
        except Exception as e:  # cr:
            print(e)
            #print("Error inserting course into database")

    cursor.close()
    if testing:
        print("pop_courses' Runtime: ", time.time() - start, " seconds.")
    pass


def pop_professors(testing=False):
    """
    Function to populate the professors table with all professors at UW-Madison. Entries contain a pUID, the professor's first name, last name, and pData 
    (where pData is a dictionary of all RateMyProfessor data). Professor data scraped from RateMyProfessorss.com with rmp_scrape/fetch_all.py script, 
    preloaded in all-professors.json.

    Args:
        testing (bool, optional): Whether or not to print runtime. Defaults to False.

    Returns:
        None: Populates the professors table with all professors at UW-Madison stored in the static file all-professors.json.
    """
    if testing:
        # Start a timer to measure the time it takes to populate the professors table
        start = time.time()
        print("----------pop_professors-----------")

    # Open the JSON file containing professors
    file = open('all-professors.json', 'r')
    data = json.load(file)          # Load the JSON file into a dictionary
    cursor = conn.cursor()          # Create a cursor object to execute SQL queries

    # For each course, try inserting its course data into the DB
    for key in data:
        prof_json = data[key]
        # Convert the JSON professor data to JSON formatted string
        pData = json.dumps(prof_json)

        try:
            # Check if the professor is already in the DB
            cursor.execute(
                "SELECT * FROM professors WHERE pName = %s", (prof_json['name'],))
            result = cursor.fetchall()

            # If the professor is not in the DB, insert the professor into the DB
            if len(result) == 0:
                # Insert course into the database's professors table
                cursor.execute(
                    "INSERT INTO professors (pName, pData) VALUES (%s, %s)", (prof_json['name'], pData))
                conn.commit()

        except Exception as e:
            print(e)

    cursor.close()
    if testing:
        print("pop_professors' Runtime: ", time.time() - start, " seconds.")
    pass


def pop_reddit_comments(testing=False):
    """
    Function to populate the rc (reddit comments) table with all comments that are relevant to a certain course that were posted to r/UWMadison. Entries
    contain a rcUID (auto-incremented), the course's cUID, the comment's body (the text that makes up the comment), a URL to the comment, and the number
    of upvotes the comment received. Comment data scraped from r/UWMadison with PRAW per execution of the script.

    Args:
        testing (bool, optional): Whether or not to print runtime. Defaults to False.

    Returns:
        None: Populates the rc table with all comments that are relevant to a certain course that were posted to r/UWMadison.

    Notes:
        - The script will only scrape comments that are relevant to a course according to our criteria: 
            -> The comment title must contain the course's code or acronym.
            -> The comment must be a top-level comment (not a reply to another comment).
            -> The comment must have more than 2 upvotes and be 26 to 999 characters long or have the course acronym in the comment body.
        - At the moment, the script is restricted to only scrape comments for Statistics, Mathematics, and Computer Science courses.
            -> This is to reduce the runtime of the script and to avoid paying hosting fees for a larger database.
    """
    if testing:
        # Start a timer to measure the time it takes to populate the professors table
        start = time.time()
        print("-------pop_reddit_comments-------")

    cursor = conn.cursor()
    # Get the cUID, and cCode of all courses
    cursor.execute("SELECT cUID, cName, cCode, cSubject FROM courses")

    courses = cursor.fetchall()  # Store all course datac

    # Create a course acronym
    for course in courses:
        # only choose selective majors now
        if (course[3] == 'Statistics' or course[3] == 'Mathematics' or course[3] == 'Computer Sciences'):
            # Extract all numeric characters from the course's code
            cNum = ''.join(filter(str.isdigit, course[2]))
            search = course[2]
            # Extract the first letter of all alphabetical characters in the course's code
            acronym = ''
            for word in course[2].split():
                if word[0].isalpha():
                    acronym += word[0]

            # Keyword analysis using full course code, or the courses acronym + course number (e.g. CS506 or CS 506)
            for submission in uwmadison_subreddit.search(search, limit=50):
                if (search.lower() in submission.title.lower()) or (acronym + cNum in submission.title) or (acronym + ' ' + cNum in submission.title):
                    # A CommentForest is a list of top-level comments each of which contains a CommentForest of replies.
                    # Submission.comments attribute's comment forest (since each replacement requires a network request)
                    try:
                        # Iterate through each top-level comment in the comment forest
                        for comment in submission.comments.list():
                            if ((25 < len(comment.body) < 1000) and ((comment.score > 2) or (cNum in comment.body))):

                                # Insert reddit comment into the database's rc table
                                cursor.execute("INSERT INTO rc (cUID, comBody, comLink, comVotes) VALUES (%s, %s, %s, %s)", (
                                    course[0], comment.body, reddit_url+comment.permalink, comment.score,))
                                conn.commit()
                    except Exception as e:  # cr:
                        print(e)
        else:
            continue

    cursor.close()
    if testing:
        print("pop_reddit_comments' Runtime: ",
              time.time() - start, " seconds.")
    pass


def pop_teaches(testing=False):
    """
    Function to populate the teaches table with cUIDs and pUIDs for each course which defines what courses each professor teaches. Entries contain a tUID
    (auto-incremented), the course's cUID, and the professor's pUID. Professor data scraped from MadGrades.com per execution of the script.

    Args:
        testing (bool, optional): Whether or not to print runtime. Defaults to False.

    Returns:
        None: Populates the teaches table with cUIDs and pUIDs for each course which defines what courses each professor teaches.
    """
    if testing:
        # Start a timer to measure the time it takes to populate the professors table
        start = time.time()
        print("----------pop_teaches----------")

    cursor = conn.cursor()
    # Get the cUID, and cCode of all courses
    cursor.execute("SELECT cUID, cCode FROM courses")
    courses = cursor.fetchall()

    # For each course in the courses table, find the professor(s) that teach the course
    for course in courses:
        cUID = course[0]
        cCode = course[1]
        # Get the grade distribution for the course from MadGrades.com
        grade_distributions = mg.mad_grades(cCode)

        # Make sure MadGrades returns a dictionary of grade distribution data for each course
        if (grade_distributions is None):
            continue

        course_professors = []  # List of professors that teach the course
        all_term_data = []     # List of all term data for the course

        # Get the section data for each term
        for i in range(len(grade_distributions["courseOfferings"])):
            single_term_data = grade_distributions["courseOfferings"][i]["sections"]
            # Store all term data into a list
            all_term_data.append(single_term_data)

        num_terms = len(all_term_data)

        # For every term, get the professor's name and add it to the list of professors for that course
        for j in range(num_terms):
            for k in range(len(all_term_data[j])):

                # If the course has multiple professors, add each professor to the list of professors for that course
                if (len(all_term_data[j][k]["instructors"]) > 1):
                    for L in range(len(all_term_data[j][k]["instructors"])):
                        if all_term_data[j][k]["instructors"][L] not in course_professors:
                            course_professors.append(
                                all_term_data[j][k]["instructors"][L])

                # If the course has only one professor, add that professor to the list of professors for that course if they aren't already in the list
                else:
                    if all_term_data[j][k]["instructors"][0] not in course_professors:
                        course_professors.append(
                            all_term_data[j][k]["instructors"][0])

        # For every professor that teaches a course, get their pUID and insert it into the teaches table for that course
        for professor in course_professors:
            try:
                prof_name = professor['name']
                # Solution to a bug in the MadGrades API (depricated?)
                prof_name = prof_name.replace("X / ", "").replace("S / ", "")

                # Get the pUID of the professor
                cursor.execute(
                    "SELECT pUID from professors where pName Like %s", (prof_name,))
                pUID = cursor.fetchone()

                # If the professor is in the professors table, add them to the teaches table with the course's cUID
                if pUID is not None:
                    try:
                        cursor.execute(
                            "INSERT INTO teaches (cUID, pUID) VALUES (%s, %s)", (cUID, pUID[0],))
                        conn.commit()
                    except Exception as e:
                        print(e)
            except Exception as e:
                # print(e)
                print("Error inserting into teaches table")

    cursor.close()
    if testing:
        print("pop_teaches' Runtime: ", time.time() - start, " seconds.")
    pass


def pop_db(testing=False):
    """
    Function that populates the entire database by calling all pop-functions.

    Args:
        testing (bool, optional): Whether or not to print runtime. Defaults to False.

    Returns:
        None: Populates the entire database by calling all pop-functions.
    """
    if testing:
        start = time.time()
        print("-------------pop_db-------------")
        print("Populating Database...")

    pop_courses(testing)
    pop_professors(testing)
    pop_reddit_comments(testing)
    pop_teaches(testing)

    if testing:
        print("-------------------------------")
        print("Database Populated.")
        print("pop_db's Runtime: ", time.time() - start, " seconds.")
        print("-------------------------------")
    pass


if __name__ == '__main__':
    pop_db(testing=True)  # Run all Pop Functions
    # PopDB(testing = False) # Run all Pop Functions
    conn.close()
