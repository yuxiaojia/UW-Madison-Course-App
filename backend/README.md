# MadCourseEvaluator Back End Web API

The back end web API for our MadCourseEvaluator application is built using Python3 and Flask. The API is hosted on AWS EC2 and is accessible at [http://3.145.22.97/](http://3.145.22.97/).

## Running the API Locally

### 1. Create a python virtual environment, activate it, then install the dependencies.

Make sure you have python3 and pip3 installed on your machine before running the following commands.

If you do not have virtualenv installed, run `pip3 install virtualenv` in your terminal before running the following commands.

```bash
python3 -m venv venv             # create a virtual environment
source venv/bin/activate         # activate the virtual environment
pip3 install -r requirements.txt # install all dependencies
```

### 2. Run the API

```bash
flask run
```

### 3. Routes

The back end is hosted on a AWS EC2 instance with public IP [3.145.22.97](3.145.22.97) and a RDS MySQL database connection. The following routes are publicly accessible:

http://3.145.22.97/ + route

route:
- `/all-courses` - returns all courses records in the database
- `/all-profs` - returns all professor records in the database'
- `/course-info/<cUID>` - returns a course record with the given course id
- `/course-profs/<cUID>` - returns all professor records who have taught a given course id
- `/reddit-comments/<cUID>` - returns all reddit comments for the given course id
- `/grade-distribution/<cUID>` - returns the grade distribution for the given course id
- `/prof-info/<pUID>` - returns a professor record with the given professor id
- `/prof-courses/<pUID>` - returns all course records taught by a given professor id

## Populating the Database

- Make sure you have the virtual environment activated before running the following commands.

- The database configuration is set in `config.py`; as long as the database is being hosted and the connection configuration is correct, the API will be able to connect to the database. 

- You should only run `populate_db.py` when you want to populate the database with new data, when the database has not been populated yet, so it has no records (failure may result with duplicate entries). At the moment, we have different scripts to scrape and create JSON files with 
the data we would like to use, and then `populate_db.py` will depend on them to populate the database tables with the data.

### 1. Run populate_db.py to populate the database with the scraped data
Not necessary if the database has already been populated.

```bash
python3 populate_db.py
```

### 2. Run course_scrape/fetch_all.py to scrape the course information to a JSON file

If you want to rescrape UW course data: When the `fetch_all.py` script is run, it will scrape the course information from the [UW Course Guide](https://guide.wisc.edu/courses/) and save it to a JSON file `all_courses.json` in the back end root directory.

```bash
python3 course_scrape/fetch_all.py # to scrape the course information
```

### 3. Run rmp_scrape/fetch_all.py to scrape the RMP data to a JSON file.

If you want to rescrape RMP data: When the `fetch_all.py` script is run, it will scrape the RMP data from [RMP](https://www.ratemyprofessors.com/) and save it to a JSON file `all_professors.json` in the back end root directory. *Note* Under maintenance, the script will not be able to scrape the RMP data consistently.

```bash
python3 rmp_scrape/fetch_all.py # to scrape the RMP data
```





