# MadCourseEvaluator

# Abstract 

Our project will be a web application that allows a user to search and view unique pages for each
course at UW-Madison. Each page will contain aggregated information from DARS course
information, Mad Grades, RateMyProfessor, and Reddit. This information will consist of course
requirements, grade distributions for courses, professor ratings (including a base rating out of 5
and instructor specific grade distribution for the course), and general mentions that are found on
the r/UWMadison subreddit. The user can also search up professors and look up the list of
courses the professor teaches/has taught.

# Customer

The customer for this software is any UW-Madison student who is trying to plan what courses
they would like to take. In a typical semester, students usually do their own research into
different courses and the professors teach them before their enrollment date. As students, we
have all had our own experiences doing this, and we see a lot of utility in building a system that
will serve as a one-stop shop for all the information we would typically take into account when
making our course schedule selections for any given semester.

# MadCourseEvaluator Front End React Application

The front end web app for our MadCourseEvaluator application is built using React. The application is hosted on Netlify and is accessible at [https://madgers.netlify.app/](https://madgers.netlify.app/).

## Running React locally
### 1. Prerequisite Installations

1. [Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
2. [Yarn (Optional)](https://classic.yarnpkg.com/lang/en/docs/install/#windows-stable)

### 2. Initialize node_modules

1. Change into the madcourseevaluator directory and run `yarn`
2. Change into the madcourseevaluator/frontend directory and run `yarn`

React application should now be ready to be ran.

### 3. Running React

1. Change into the madcourseevaluator/frontend directory
2. Run `yarn start`

## Available Scripts 

### `yarn start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `yarn flask`

Runs the backend flask application located [here](../backend/app.py)\
Note: The React application is currently pointed to our AWS solution. If you want to use the local backend, you **must** change the endpoint names located in:

1. [Course.jsx](src/components/Course.jsx)
2. [Instructor.jsx](src/components/Instructor.jsx)
3. [Search.jsx](src/components/Search.jsx)

### `yarn cypress open`
Opens the Cypress tesing framework to run component and end to end tests. 

### `yarn build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `yarn eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.




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