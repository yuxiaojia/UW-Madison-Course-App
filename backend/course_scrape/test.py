__author__ = "Jarvis Jia"
__credits__ = ["Peter Bryant", "Jarvis Jia", "Bryan Li", "Swathi Annamaneni", "Aidan Shine"]
__version__ = "1.0.0"
__maintainer__ = "Jarvis Jia"

import json
from fetch import ScrapeCourses
def ScrapeCoursesTest():

    # open the goldenStandard.json file
    with open("goldenStandard.json", "r") as f1:
        file1 = json.loads(f1.read())
    
    # call the scrape course function in fetch
    ScrapeCourses()

    # open the test file generated
    with open("test_file.json", "r") as f2:
        file2 = json.loads(f2.read())

    for item in file2:
        if item not in file1:
            print(f"Found difference: {item}")
        
    print('success')

if __name__ == '__main__':
    ScrapeCoursesTest()