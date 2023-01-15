import requests
import config

# Instantiate Madgrades API Token
madgrades_api_token = config.madgrades_api_token
auth_header = {'Authorization': 'Token ' + madgrades_api_token} # Authorization header, required for API call

# URL Constants
madGrades_query_url = 'https://api.madgrades.com/v1/courses/?query='

def mad_grades(courseCode):
    """
    Pulls grade distribution data for a course corresponding to a courseCode offered at UW-Madison.
    Example Course Code: "COMP SCI 577"

    Args:
        courseCode (str): Course code of the course for which grade distribution data is desired (ex. COMP SCI)

    Returns:
        dict: Dictionary containing grade distribution data for the course
    """
    search = courseCode
    response = requests.get(madGrades_query_url + search, headers=auth_header) # API request to access list of courses matching search query
    course_listings = response.json()
    if course_listings == {'error': 'Unauthorized'}:                           # If API token is invalid, return
        return('Error: Regenerate MadGrades API Token')
    try:
        course_url = course_listings['results'][0]['url']                      # Endpoint of first course in list (i.es. the course matching the course code)
    except Exception as e:
        return
    response = requests.get(course_url, headers=auth_header)                   # API request to get course data associated with the course
    full_course_data = response.json()                                  
    grades_url = full_course_data['gradesUrl']                                 # Endpoint of the grade distribution associated with the course                                            
    response = requests.get(grades_url, headers=auth_header)                   # API request to get grade distribution data
    courses = response.json()                                                 
    return(courses)