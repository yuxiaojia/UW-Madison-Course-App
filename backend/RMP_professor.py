import requests
import json
from rmp_scrape.fetch_all import RateMyProfApi # Public & Modified RMP API for Professor Data

prof_json = {} 
count = 0


def PopProfessors():
    """
    Function to populate the professors table with all professors at UW-Madison. Iterates over the two RMP school UIDs and calls the helper function to populate the table.
    Entries contain a pUID, the professor's first name, last name, and pData (where pData is a dictionary of all RateMyProfessor data).

    Data: Professor data scraped from RateMyProfessorss.com.
    """

    # Instantiate UW-Madison RateMyProfessor Object (DOCS: 1.1.2.1)
    uwm_rmp_sid_1 = "1256"  # RMP School ID #1
    uwm_rmp_sid_2 = "18418" # RMP School ID #2
    
    api_1 = RateMyProfApi(uwm_rmp_sid_1) # (DOCS: 1.1.2.2)
    api_2 = RateMyProfApi(uwm_rmp_sid_2)

    # Scrape each list of professors for each school ID
    professors_data = [] 
    professors_data.append(api_1.ScrapeProfessors(True)) # (DOCS: 1.1.2.3)
    professors_data.append(api_2.ScrapeProfessors(True))

    j = 0
    prof_json = {}
    # Iterate through each list of professors and call the helper function to populate the professors table.
    for data in professors_data:
        for professor in data:
            
            # Individual professor data    
            professor = data[professor]  

            # Store the professor's data in a dictionary   
            prof_json[f'professor {j}'] = {}                   
            prof_json[f'professor {j}']['name'] = professor.first_name + " " + professor.last_name 
            prof_json[f'professor {j}']['dept'] = professor.department              
            prof_json[f'professor {j}']['RMPID'] = professor.ratemyprof_id          
            prof_json[f'professor {j}']['RMPRating'] = professor.overall_rating        
            prof_json[f'professor {j}']['RMPTotalRatings'] = professor.num_of_ratings 
            prof_json[f'professor {j}']['RMPRatingClass'] = professor.rating_class
            j = j + 1

    # save all the professor into files
    with open("all-professors.json", "a") as outfile:
        json.dump(prof_json,  outfile, indent = 4)
    outfile.close()

if __name__ == '__main__':
    PopProfessors()