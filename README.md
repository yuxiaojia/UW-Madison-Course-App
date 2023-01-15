# MadCourseEvaluator

## Back End Documentation

### Tech Stack

- Flask (backend web API)
- MySQL (relational database)

### Features

- Extracts data from madgrades, rate my professors, and reddit API 
- ETL data procressing to populate a MySQL database
- Loads data from a MySQL database formatted in json 

### Environment Variables

To run this project, you will need to add the following environment variables to your .env file

```bash
python3 -m venv ./env
```

## Getting Started

### Prerequisites

This project must run in a virtual environment: 

```bash
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

```bash
env/Scripts/activate
```
### Installation

Install any updates requirements in requirments.txt

```bash
python -m pip install -r requirements.txt
```

```bash
pip install flask
```

```bash
pip install requests
```

```bash
pip install -U Flask-SQLAlchemy
```

### Running Tests

To run tests, run the following command

```bash

```
### Run Locally

Clone the project

```bash
git clone https://git.doit.wisc.edu/cdis/cs/courses/cs506/madcourseevaluator.git
```

Go to the project directory

```bash
cd madcourseevaluator
```

```bash
cd backend
```

Install dependencies

```bash

```

Start the server

```bash
python ./app.py
```

```bash
python populateDB.py
```
## Usage

### 1.1 populateDB.py

populateDB.py is a stand alone script used for populating our MySQL database. The back-end team decided this script would be very useful because having a database with most of our application data will reduce the amount of API requests we will need to make everytime a user requests a page. This script populates courses, professors, reddit comment data into a MySQL relational database for the front-end team to utilize when providing important information that the user needs when evaluating courses and professors. 

#### 1.1.1 Functions

#### 1.1.1.1 PopCourses()
Function to populate the courses table with all courses at UW-Madison. The data is stored as a tuple in the database table (cUID (course unique identifier), the course's name, the course's subject, the course's 'course code', the course's credits, the course's description).

#### 1.1.1.2 PopProfessors()
Function to populate the professors table with all professors at UW-Madison. The data is stored as a tuple in the database table (pUID (professor unique identifier), the professor's full name, and pDate (where pDate is a dictionary of all RateMyProfessor data)). 

#### 1.1.1.3 PopRedditComments()
Function to populate the reddit comment table with top-level comments that are relevant to a certain course that were posted to r/UWMadison. The data is stored as a tuple into reddit comment table (comment ID, the comment's text, a link to the comment, the comment's upvotes, and the cUID of the course the comment is about). 

#### 1.1.1.4 PopTeaches()
Function to populate the teaches table with course ID and professor ID for each course. The data is stored as a tuple into the teaches table (course ID, professor ID).

#### 1.1.1.5 PopDB()
Function calling every function necessary to populate data into MYSQL relational database.

### 1.1.2 Notes

#### 1.1.2.1 UW-Madison RateMyProfessor Object ID
It seems like RateMyProfessor.com has multiple unique ID #'s for UW-Madison associated with different records. These records are not the same, but they may contain overlapping information (i.e. Same professor names, same department, but with different reviews). We want to account for sets of reviews so that we have the most possible, so we use both UIDs ```1256``` and ```18418```

#### 1.1.2.2 RateMyProfessor Public API + Modifications
This project uses a public API found from <a href="https://github.com/tisuela/ratemyprof-api"> this Github repository</a> which has two files to create a Professor object and another to scrape RateMyProfessor for professor information who taught at a particular school. We have made slight modifications to their code to allow scraping for any school given a RateMyProfessor school ID, allowing us to make an instance of a RateMyProfApi object for each of the RateMyProfessor unique school IDs that contain records of information about professors at UW-Madison. 

#### 1.1.2.3 Scraping Professors Data
Here we are scraping all professor data from each of the RateMyProfessor school endpoints associated with UW-Madison, and storing it in a large array object. Where we will use that data to populate our DB in the helper function.
 
#### 1.1.2.4 Creating Course Acronym
When we were trying to search for relevent Reddit comments about a course, we realized that all comments don't usually state the entire course code (i.e. COMP SCI 506). When comments do directly reference a course, the usually us an abbreviation of the course name (i.e. CS506 or CS 506). We want to get relevant search results from more Reddit comments so we build the acronym for each course.


### 1.2 app.py
This is our back-end API to extract data from our database, transform, and load data into JSON. It returns JSON format for front-end components. 

### 1.2.1 API Endpoints 

#### 1.2.1.1 ~/all-courses
Returns JSON of all courses at the university along with all fields associated with each course. Each course stores (cUID, cName, cSubject, cCode, cCredits, cDescription, cReq).

#### 1.2.1.2 ~/all-profs
Returns JSON of all professors at the university along with their data from RateMyProfessor. Each professor stores their name, deptartment, RMPID (RateMyProfessorID), RMPRating, RMPTotalRatings, and RMPRatingClass.

#### 1.2.1.3 ~/course-info/<cUID>
Returns JSON of course info corresponding to a unique course ID. The course info includes the course's: cUID, name, subject, course code, number of credits, description, and requisites. 

#### 1.2.1.4  ~/course-profs/<cUID>
Returns JSON of professor data for professors who have taught a course corresponding to a unique course ID recently. Each professor stores their name, deptartment, RMPID (RateMyProfessorID), RMPRating, RMPTotalRatings, and RMPRatingClass.
 
#### 1.2.1.5 ~/reddit-comments/<cUID>
Returns JSON of reddit comment data from comments on r/UWMadison relevant to the course corresponding to the unique course ID. The comments include description, link, and votes. 

#### 1.2.1.6 ~/grade-distribution/<cUID>
Returns JSON of grade distributions, section, and instructor of a course specified by course code ID.

#### 1.2.1.7 ~/prof-info/<pUID>
Returns JSON of professor information specified by profressor code ID.

#### 1.2.1.8 ~/prof-courses/<pUID>
Returns JSON of course information specificied by profressor code ID.

### 1.3 config.py
This configuration information provides credentials for MySQL database, Reddit API Qrapper, Reddit Bot and MadGrades API Token.

### 1.4 madgrades.py
This returns a JSON of grade distributions from the madgrades API.

### 1.5 RMP_professor.py
This extracts data from the rate my professor API and loads it into JSON format (professor's name, dept, id, rating, total rating, rating class).

Documentation can be found [here](backend/README.md)

## Front End Documentation
Documentation can be found [here](frontend/README.md)

## Roadmap

* [ ]  Todo 1
* [ ]  Todo 2

## Acknowledgements

 - [Shields.io](https://shields.io/)
 - [Awesome README](https://github.com/matiassingers/awesome-readme)
 - [Emoji Cheat Sheet](https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md#travel--places)
 - [Readme Template](https://github.com/othneildrew/Best-README-Template)