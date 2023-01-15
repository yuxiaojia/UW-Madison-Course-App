#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Peter Bryant, Jarvis Jia"
__credits__ = ["Peter Bryant", "Jarvis Jia",
               "Bryan Li", "Swathi Annamaneni", "Aidan Shine, Tong Yang"]
__version__ = "1.0.0"
__maintainer__ = "Peter Bryant"
__email__ = "pbryant2@wisc.edu"
__status__ = "Development"

"""
Flask application for MadCourseEvaluator back end web API.
- AWS EC2 Public IP: 3.145.22.97
- Hosted React Front End: https://madgers.netlify.app/
- Routes:
    /all-courses
    /all-profs
    /course-info/<cUID>
    /course-profs/<cUID>
    /reddit-comments/<cUID>
    /grade-distribution/<cUID>
    /prof-info/<pUID>
    /prof-courses/<pUID>
- URL Params: 
    cUID = Course Unique ID
    pUID = Professor Unique ID
"""

# Flask Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy ORM
from flask_cors import CORS             # CORS: Cross Origin Resource Sharing

# Python Imports
from sqlalchemy import create_engine    # SQLAlchemy Engine
import json

# Custom Scripts
# Custom MadGrades Script for Grade Distributions
import madgrades as mg
import config                           # Application Configuration

db_uri = 'mysql://' + config.user + ':' + config.password + '@' + config.host + '/' + config.database
db = SQLAlchemy()

app = Flask(__name__)
CORS(app)                                       # Enable CORS for all routes
app.config['CORS_HEADERS'] = 'Content-Type'     # Set CORS header
app.secret_key = config.secret                  # Set Flask Secret Key
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri  # Set SQLAlchemy URI
engine = create_engine(db_uri)                  # Create SQLAlchemy Engine

@app.route('/all-courses', methods=['GET', 'POST'])
def all_courses():
    """
    Returns JSON of all courses at the university along with all fields associated with each course.

    Args:
        None

    Returns:
        all_course_json_data (dict): Dictionary of all courses at the university along with all fields associated with each course.
    """
    conn = engine.raw_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")  # Store all data on all courses

    if cursor.rowcount == 0:  # If no rows are returned, return an empty dictionary with key 'error'
        return {'error': 'No courses found for route /all-courses.'}

    all_courses = cursor.fetchall()
    all_course_json_data = {}

    # For each course, store all course data in a dictionary
    for course in all_courses:
        course_json_data = {'cUID': None, 'cName': None, 'cCode': None}
        course_json_data['cUID'] = course[0]
        course_json_data['cName'] = course[1]
        course_json_data['cCode'] = course[3]
        all_course_json_data[course_json_data['cUID']] = course_json_data

    cursor.close()
    conn.close()
    return all_course_json_data


@app.route('/all-profs', methods=['GET', 'POST'])
def all_profs():
    """
    Returns a dictionary of all professors at the university along with all fields associated with each professor.

    Args:
        None

    Returns:
        all_profs_json_data (dict): Dictionary of all professors at the university along with all fields associated with each professor.
    """
    conn = engine.raw_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pUID, pData FROM professors")  # Execute SQL query

    if cursor.rowcount == 0:  # If no rows are returned, return an empty dictionary with key 'error'
        return {'error': 'No professors found for route /all-profs.'}

    all_profs = cursor.fetchall()  # Fetch all the rows from professors table
    all_profs_json_data = {}

    # Stor all professor data in a dictionary
    for prof in all_profs:
        pUID = prof[0]
        pData = json.loads(prof[1])
        all_profs_json_data[pUID] = pData

    cursor.close()
    conn.close()
    return all_profs_json_data


@app.route('/course-info/<cUID>', methods=['GET', 'POST'])
def course_info(cUID):
    """
    Returns all of a single course's information from courses table corresponding to the given cUID.

    Args:
        cUID (str): Course Unique ID

    Returns:
        course_json_data (dict): Dictionary of all fields associated with the course corresponding to the given cUID.
    """
    conn = engine.raw_connection()
    cursor = conn.cursor()

    # Get the corresponding course data from courses table:
    cursor.execute("SELECT * FROM courses WHERE cUID = %s",
                   (cUID,))   # Execute SQL query

    if cursor.rowcount == 0:  # If no rows are returned, return an empty dictionary with key 'error'
        return {'error': 'No professors found for route /course-info/' + cUID + '.'}

    # Fetch all the course data for the given cUID
    course_data = cursor.fetchall()[0]
    course_json_data = {'cUID': None, 'cName': None, 'cSubject': None,  # Create a dictionary to store course data
                        'cCode': None, 'cCredits': None, 'cDescription': None, 'cReq': None}

    # Populate the course dictionary
    course_json_data['cUID'] = course_data[0]
    course_json_data['cName'] = course_data[1]
    course_json_data['cSubject'] = course_data[2]
    course_json_data['cCode'] = course_data[3]
    course_json_data['cCredits'] = course_data[4]
    course_json_data['cDescription'] = course_data[5]
    course_json_data['cReq'] = course_data[6]

    cursor.close()
    conn.close()
    return course_json_data


@app.route('/course-profs/<cUID>', methods=['GET', 'POST'])
def course_profs(cUID):
    """
    Returns all professors who have taught the a course corresponding to the given cUID. 

    Args:
        cUID (str): Course Unique ID

    Returns:
        all_prof_json_data (dict): Dictionary mapping pUID to pData for all professors who have taught the course corresponding to the given cUID.
    """
    conn = engine.raw_connection()
    cursor = conn.cursor()

    q = "SELECT pUID, pData FROM professors WHERE pUID IN (SELECT pUID FROM teaches WHERE cUID = %s)"
    # Get all the professors who have taught the course recently
    cursor.execute(q, (cUID,))

    if cursor.rowcount == 0:  # If no rows are returned, return an empty dictionary with key 'error'
        return {'error': 'No professors found for route /course-profs/' + cUID + '.'}

    all_profs = cursor.fetchall()  # Fetch all the rows from professors table

    all_prof_json_data = {}  # Create a dictionary mapping pUID to pData

    # Populate the all_prof_json_data dictionary
    for prof in all_profs:
        pUID = prof[0]
        pData = json.loads(prof[1])
        all_prof_json_data[pUID] = pData

    cursor.close()
    conn.close()
    return all_prof_json_data


@app.route('/reddit-comments/<cUID>', methods=['GET', 'POST'])
def reddit_comments(cUID):
    """
    Returns all Reddit comments associated with the course corresponding to the given cUID.

    Args:
        cUID (str): Course Unique ID
    
    Returns:
        all_rc_json_data (dict): Dictionary mapping rcUID to rcData for all Reddit comments associated with the course corresponding to the given cUID.
    
    Notes:
        - At the moment, the script is restricted to only scrape comments for Statistics, Mathematics, and Computer Science courses.
            -> This is to reduce the runtime of the script and to avoid paying hosting fees for a larger database.
    """
    conn = engine.raw_connection()
    cursor = conn.cursor()

    # Get all Reddit comments associated with the course
    cursor.execute("SELECT * FROM rc WHERE cUID = %s", (cUID,))

    if cursor.rowcount == 0:  # If no rows are returned, return an empty dictionary with key 'error'
        return {'error': 'No professors found for route /reddit-comments/' + cUID + '.'}

    all_rc = cursor.fetchall()  # Fetch all the rows from rc table

    all_rc_json_data = {}  # Create a dictionary mapping rcUID to rcData

    # Populate the all_rc_json_data dictionary with all Reddit comment data
    for rc in all_rc:
        comID = rc[0]
        comBody = rc[1]
        comLink = rc[2]
        comVotes = rc[3]
        all_rc_json_data[comID] = {'comBody': comBody,
                                   'comLink': comLink, 'comVotes': comVotes}

    cursor.close()
    conn.close()
    return all_rc_json_data


@app.route('/grade-distribution/<cUID>', methods=['GET', 'POST'])
def grade_distribution(cUID):
    """
    Returns grade distributions for the provided course cUID.

    Args:
        cUID (str): Course Unique ID

    Returns:
        grade_distribution (dict): Dictionary containing grade distribution data for the course corresponding to the given cUID.
    """
    conn = engine.raw_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT cCode FROM courses WHERE cUID = %s", (cUID,))  # Get the course code for the course
    # Fetch the course code and strip the whitespace
    cCode = cursor.fetchall()[0][0]

    if cursor.rowcount == 0:  # If no rows are returned, return an empty dictionary with key 'error'
        return {'error': 'No courses found for route /grade-distribution/' + cUID + '.'}

    # Get grade distribution for the course using the course code
    grade_distribution = mg.mad_grades(cCode)

    # Get the cumulative grade distribution for each professor
    grade_distribution['professor_cumulative_grade_distribution'] = {}

    # Get the name of all professors who have taught the course in the database
    cursor.execute(
        "SELECT p.pUID, p.pName from professors p, courses c, teaches t WHERE c.cCode = %s and c.cUID = t.cUID and p.pUID = t.pUID", (cCode,))

    if cursor.rowcount == 0:  # If no rows are returned, return an empty dictionary with key 'error'
        return {'error': 'No professors found for route /grade-distribution/' + cUID + '.'}

    # Fetch all the professor names for professors who have taught the course
    course_profs = cursor.fetchall()

    # For each professor, populate the grade_distribution dictionary with their cumulative grade distribution (sum over all sections)
    for prof_info in course_profs:
        prof_pUID = prof_info[0]
        prof_name = prof_info[1]
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID] = {
        }
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['name'] = prof_name
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['aCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['abCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['bCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['bcCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['cCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['crCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['dCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['fCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['iCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['nCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['nrCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['nwCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['otherCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['pCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['sCount'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['total'] = 0
        grade_distribution['professor_cumulative_grade_distribution'][prof_pUID]['uCount'] = 0

        # For each grade distribution, add the grade counts to the cumulative grade distribution for the professor
        for key in grade_distribution['professor_cumulative_grade_distribution'][prof_pUID].keys() - {'name'}:
            for i in range(len(grade_distribution["courseOfferings"])):
                for j in range(len(range(len(grade_distribution["courseOfferings"][i]['sections'])))):
                    for k in range(len(grade_distribution["courseOfferings"][i]['sections'][j]['instructors'])):
                        API_prof_name = grade_distribution["courseOfferings"][
                            i]['sections'][j]['instructors'][k]['name']
                        # If the professor name in the API contains "X / ", remove the "X / " from the name
                        if "X / " in API_prof_name:
                            API_prof_name = API_prof_name.split("X / ")[1]
                        # If the professor name is in the returned API data, add the grade counts to the cumulative grade distribution for the professor
                        if API_prof_name == prof_name.upper():
                            grade_distribution['professor_cumulative_grade_distribution'][prof_pUID][
                                key] += grade_distribution["courseOfferings"][i]['sections'][j][key]
    cursor.close()
    conn.close()
    return grade_distribution


@app.route('/prof-info/<pUID>', methods=['GET', 'POST'])
def professor_info(pUID):
    """
    Returns all RateMyProfessor data for a professor associated with the given pUID.

    Args:
        pUID (str): The pUID of the professor whose data is to be returned.
    
    Returns:
        professor_data (dict): A dictionary containing all RateMyProfessor data for the professor associated with the given pUID.

    """
    conn = engine.raw_connection()
    cursor = conn.cursor()

    # Get professor data from professors table
    cursor.execute("SELECT pData FROM professors WHERE pUID = %s", (pUID,))

    if cursor.rowcount == 0:  # If no rows are returned, return an empty dictionary with key 'error'
        return {'error': 'No professors found for route /prof-info/' + pUID + '.'}

    prof_data = cursor.fetchall()[0][0]    # Fetch all the professor data
    # Store professor data in the full professor data json that will be returned
    professor_data = json.loads(prof_data)

    cursor.close()
    conn.close()
    return professor_data


@app.route('/prof-courses/<pUID>', methods=['GET', 'POST'])
def professor_courses(pUID):
    """
    Returns all courses (with their data) taught by a professor associated with the given pUID.

    Args:
        pUID (str): The pUID of the professor whose courses are to be returned.

    Returns:
        full_course_data_json (dict): A dictionary containing all courses (with their data) taught by the professor associated with the given pUID.
    """
    conn = engine.raw_connection()
    cursor = conn.cursor()

    # Get the course ID data from teaches table
    cursor.execute("SELECT cUID FROM teaches WHERE pUID = %s", (pUID,))
    list_courseID = cursor.fetchall()

    if cursor.rowcount == 0:  # If no rows are returned, return an empty dictionary with key 'error'
        return {'error': 'No courses found for route /prof-courses/' + pUID + '.'}

    full_course_data_json = {}

    # For each course, get the course data from the courses table
    for courseID in list_courseID:
        courseID = str(courseID[0])
        cursor.execute(
            "SELECT cName, cSubject, cCode, cCredits, cDescription, cReq FROM courses WHERE cUID = %s", (courseID,))
        course_data = cursor.fetchall()

        # Store course data in dictionary
        course_json_data = {'cName': None, 'cSubject': None, 'cCode': None,
                            'cCredits': None, 'cDescription': None, 'cReq': None}
        course_data = course_data[0]
        course_json_data['cName'] = course_data[0]
        course_json_data['cSubject'] = course_data[1]
        course_json_data['cCode'] = course_data[2]
        course_json_data['cCredits'] = course_data[3]
        course_json_data['cDescription'] = course_data[4]
        course_json_data['cReq'] = course_data[5]

        # If a course already exists in the dictionary wtih the same 'cName', do not add it to the dictionary
        unique_course = True
        for key in full_course_data_json.keys():
            if course_json_data['cName'] == full_course_data_json[key]['cName']:
                unique_course = False
                break
        if unique_course:
            full_course_data_json[courseID] = course_json_data

    cursor.close()
    conn.close()
    return full_course_data_json


if __name__ == '__main__':
    app.run(port=5000)
