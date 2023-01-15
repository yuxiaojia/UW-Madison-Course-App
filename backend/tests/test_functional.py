import requests
import unittest
import os
import sys
import inspect
import json
import test_config

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from app import app

"""
Functional Unit Tests: View Functions respond to nominal and non-nominal inputs (e.g. 404, 500, 200, etc.)

RUN: python3 tests/test_functional.py
"""
class TestCourseRoutes(unittest.TestCase):
    """
    Tests for Course Flask API Routes in app.py 
    """
    def test_all_courses(self): 
        """
        Test /all-courses endpoint
        """
        request = app.test_client().get('/all-courses')   # Make a request to the /all-courses endpoint
        self.assertEqual(request.status_code, 200)        # Assert that the request was successful (200)
        self.assertEqual(request is not None, True)       # Assert that the request is not None
        self.assertEqual(request.json is not None, True)  # Assert that the request.json is not None

        # Assert that the first 5 courses contain all fields
        i = 0
        for key in request.json.keys():
            self.assertEqual(request.json[key]['cUID'] is not None, True)
            self.assertEqual(request.json[key]['cName'] is not None, True)
            self.assertEqual(request.json[key]['cCode'] is not None, True)
            self.assertEqual(key, str(request.json[key]['cUID']))
            i += 1
            if i == 5:
                break

    def test_course_info(self):
        """
        Test /course-info endpoint
        """
        cs577_cUID = test_config.cs577_cUID
        route = '/course-info/'
        full_request = route + cs577_cUID
        request = app.test_client().get(full_request)     # Make a request to the /course-info/58786 endpoint
        self.assertEqual(request.status_code, 200)        # Assert that the request was successful (200)

        # Assert the json contains all keys
        self.assertEqual("cUID" in request.json.keys(), True)
        self.assertEqual("cName" in request.json.keys(), True)
        self.assertEqual("cCode" in request.json.keys(), True)
        self.assertEqual("cDescription" in request.json.keys(), True)
        self.assertEqual("cReq" in request.json.keys(), True)
        self.assertEqual("cCredits" in request.json.keys(), True)
        self.assertEqual("cSubject" in request.json.keys(), True)

        # Assert that the course info contains all required fields
        self.assertEqual(request.json['cUID'] is not None, True)
        self.assertEqual(request.json['cName'] is not None, True)
        self.assertEqual(request.json['cCode'] is not None, True)

        # Assert that the JSON returned contains only data from one course (7 keys total per course)
        self.assertEqual(len(request.json.keys()), 7)

    def test_course_profs(self):
        """
        Test /course-profs endpoint
        """
        cs577_cUID = test_config.cs577_cUID
        route = '/course-profs/'
        full_request = route + cs577_cUID
        request = app.test_client().get(full_request)     # Make a request to the /course-info/58786 endpoint
        self.assertEqual(request.status_code, 200)        # Assert that the request was successful (200)

        # Assert the json contains at least one key
        self.assertEqual(len(request.json.keys()) > 0, True)

        # Assert that every professor entry contains all keys (6 total) and required fields (3)
        contains_marc_renault = False
        contains_eric_bach = False
        for key in request.json.keys():
            self.assertEqual("name" in request.json[key].keys(), True)
            self.assertEqual("dept" in request.json[key].keys(), True)
            self.assertEqual("RMPID" in request.json[key].keys(), True)
            self.assertEqual("RMPRating" in request.json[key].keys(), True)
            self.assertEqual("RMPRatingClass" in request.json[key].keys(), True)
            self.assertEqual("RMPTotalRatings" in request.json[key].keys(), True)
            self.assertEqual("name" in request.json[key].keys(), True)
            self.assertEqual("dept" in request.json[key].keys(), True)
            self.assertEqual("RMPID" in request.json[key].keys(), True)
            self.assertEqual(request.json[key]['name'] is not None, True)
            self.assertEqual(request.json[key]['dept'] is not None, True)
            self.assertEqual(request.json[key]['RMPID'] is not None, True)
            if request.json[key]['name'] == "Marc Renault":
                contains_marc_renault = True
            if request.json[key]['name'] == "Eric Bach":
                contains_eric_bach = True

        # Assert that the JSON returned contains at least the two known professors for this course
        self.assertEqual(contains_marc_renault, True)
        self.assertEqual(contains_eric_bach, True)

    def test_course_reddit_comments(self):
        """
        Test /reddit-comments endpoint
        """
        cs577_cUID = test_config.cs577_cUID
        route = '/reddit-comments/'
        full_request = route + cs577_cUID
        request = app.test_client().get(full_request)     # Make a request to the /course-info/58786 endpoint
        self.assertEqual(request.status_code, 200)        # Assert that the request was successful (200)

        # Assert the json contains at least one key
        self.assertEqual(len(request.json.keys()) > 0, True)

        # Assert that every professor entry contains all keys (3 total) and required fields (3)
        i=0
        for key in request.json.keys():
            if i == 1:
                break
            i += 1
            self.assertEqual("comBody" in request.json[key].keys(), True)
            self.assertEqual("comLink" in request.json[key].keys(), True)
            self.assertEqual("comVotes" in request.json[key].keys(), True)
            self.assertEqual(request.json[key]['comBody'] is not None, True)
            self.assertEqual(request.json[key]['comLink'] is not None, True)
            self.assertEqual(request.json[key]['comVotes'] is not None, True)

            # Assert that the link is a valid URL
            self.assertEqual(request.json[key]['comLink'].startswith("https://"), True)

            # Make a request to the link and assert that it is a valid URL (200)
            link_request = requests.get(request.json[key]['comLink'])
            self.assertEqual(link_request.status_code, 200)

    def test_course_grade_distribution(self):
        """
        Test /grade-distribution endpoint
        """
        cs577_cUID = test_config.cs577_cUID
        route = '/grade-distribution/'
        full_request = route + cs577_cUID
        request = app.test_client().get(full_request)     # Make a request to the /course-info/58786 endpoint
        self.assertEqual(request.status_code, 200)        # Assert that the request was successful (200)

        # Assert the json contains at least one key
        self.assertEqual(len(request.json.keys()) > 0, True)

        # Assert that JSON contains expected keys
        self.assertEqual('courseOfferings' in request.json.keys(), True)
        self.assertEqual('courseUuid' in request.json.keys(), True)
        self.assertEqual('cumulative' in request.json.keys(), True)
        self.assertEqual('professor_cumulative_grade_distribution' in request.json.keys(), True)


        # Assert that the per term course grade distribution data for courseOfferings contains expected keys
        for info in request.json['courseOfferings']:
            self.assertEqual('cumulative' in info.keys(), True)
            self.assertEqual('sections' in info.keys(), True)
            self.assertEqual('termCode' in info.keys(), True)

            # Assert that the per section course grade distribution data for courseOfferings contains instructors key with id and name for professor
            prof_list = []
            marc_flag = 0 
            for section in range(len(info['sections'])):
                self.assertEqual(info['sections'][section]['instructors'][0]['id'] is not None, True)
                self.assertEqual(info['sections'][section]['instructors'][0]['name'] is not None, True)
                prof_list.append(info['sections'][section]['instructors'][0]['name'].lower().strip())

                print(info['sections'][section]['instructors'][0]['name'].lower().strip)

                if 'marc renault' in info['sections'][section]['instructors'][0]['name'].lower().strip():
                    marc_flag = 1
        
            self.assertEqual(marc_flag, 1)

class TestProfRoutes(unittest.TestCase):
    """
    Tests for Professor Flask API Routes in app.py 
    """
    def test_all_profs(self): 
        """
        Test /all-profs endpoint
        """
        request = app.test_client().get('/all-profs')     # Make a request to the /all-courses endpoint
        self.assertEqual(request.status_code, 200)        # Assert that the request was successful (200)
        self.assertEqual(request is not None, True)       # Assert that the request is not None
        self.assertEqual(request.json is not None, True)  # Assert that the request.json is not None

        # Assert that the first 5 professors contain all fields (6 total)
        i = 0
        for key in request.json.keys():
            self.assertEqual(request.json[key] is not None, True)
            self.assertEqual(request.json[key]['name'] is not None, True)
            self.assertEqual(request.json[key]['dept'] is not None, True)
            # self.assertEqual(key, str(request.json[key]['RMPID'])) # We may want to make it so we are returning the pUID for each professor too
            self.assertEqual("RMPID" in request.json[key].keys(), True)
            self.assertEqual("RMPRating" in request.json[key].keys(), True)
            self.assertEqual("RMPRatingClass" in request.json[key].keys(), True)
            self.assertEqual("RMPTotalRatings" in request.json[key].keys(), True)
            i += 1
            if i == 5:
                break

    def test_prof_info(self): 
        """
        Test /prof-info endpoint
        """
        pUID_marc_renault = test_config.marc_renault_pUID
        route = '/prof-info/'
        full_request = route + pUID_marc_renault
        request = app.test_client().get(full_request)     # Make a request to the /all-courses endpoint
        self.assertEqual(request.status_code, 200)        # Assert that the request was successful (200)
        self.assertEqual(request is not None, True)       # Assert that the request is not None
        self.assertEqual(request.json is not None, True)  # Assert that the request.json is not None

        # Assert that the professor data contains all fields (6 total)
        self.assertEqual(len(request.json.keys()) == 6, True)
        self.assertEqual(request.json['name'] is not None, True)
        self.assertEqual(request.json['dept'] is not None, True)
        self.assertEqual("RMPID" in request.json.keys(), True)
        self.assertEqual("RMPRating" in request.json.keys(), True)
        self.assertEqual("RMPRatingClass" in request.json.keys(), True)
        self.assertEqual("RMPTotalRatings" in request.json.keys(), True)
        self.assertEqual(request.json['name'], "Marc Renault")
        self.assertEqual(request.json['dept'], "Computer Science")

    def test_prof_courses(self):
        """
        Test /prof-courses endpoint
        """
        pUID_marc_renault = test_config.marc_renault_pUID
        route = '/prof-courses/'
        full_request = route + pUID_marc_renault
        request = app.test_client().get(full_request)     # Make a request to the /all-courses endpoint
        self.assertEqual(request.status_code, 200)        # Assert that the request was successful (200)
        self.assertEqual(request is not None, True)       # Assert that the request is not None
        self.assertEqual(request.json is not None, True)  # Assert that the request.json is not None

        course_list = []
        for course in request.json:
            self.assertEqual(request.json[course]['cCode'] is not None, True)
            self.assertEqual(request.json[course]['cName'] is not None, True)
            self.assertEqual(request.json[course]['cSubject'] is not None, True)
            self.assertEqual('cReq' in request.json[course].keys(), True)
            self.assertEqual('cCredits' in request.json[course].keys(), True)
            self.assertEqual('cDescription' in request.json[course].keys(), True)
            course_list.append(request.json[course]['cCode'].strip())
        
        # Ensure that the courses that Marc Renault teaches are in the list of courses returned
        self.assertEqual('COMP SCI 200' in course_list, True)
        self.assertEqual('COMP SCI 577' in course_list, True)

if __name__ == '__main__':
    unittest.main() # Run all unit tests