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