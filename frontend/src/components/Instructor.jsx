/**
 * Authors: Aidan Shine, Bryan Li, Jarvis Jia, Peter Bryant, Swathi Annamaneni, Tong Yang
 * Revision History: 11/01/2022:12/12/2022
 * Organization: Madgers
 * Version: 1.0.0
 */

import React, { useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Header from "./Header";
import { useParams, useNavigate } from "react-router-dom";

/**
 * Instructor: component that shows instructor info as well as a list of all
 * classes taught by the instructor (and links to each one).
 * @returns Instructor React element
 *
 * @component
 */
const Instructor = () => {
  const navigate = useNavigate(); // useNavigate hook which is used to navigate to a different route

  const professorID = useParams().id; // get the value of the id param

  const [courses, setCourses] = useState([]); // useState hook to store the courses
  const [professor, setProfessor] = useState({}); // useState hook to store the professor

  // fetch professor info and professor courses for a particular professorID
  useEffect(() => {
    // fetch the professor RMP data
    fetch("https://3.145.22.97/prof-info/" + professorID)
      .then((response) =>
        response.json().then((json) => {
          setProfessor(json);
        })
      )
      .catch((e) =>
        console.log("error loading professor info from backend ", e)
      );

    // fetch the courses RMP data
    fetch("https://3.145.22.97/prof-courses/" + professorID).then((response) =>
      response
        .json()
        .then((json) => {
          var classes = [];
          // for each course in the json response, create a new object with the course code and the course name
          for (var key in json) {
            const classFull = {
              code: json[key].cCode,
              name: json[key].cName,
              id: key,
            };
            classes.push(classFull); // push the new object to the classes list
          }
          setCourses(classes);
        })
        .catch((e) =>
          console.log("error loading professor courses info from backend ", e)
        )
    );
  }, [professorID]);

  return (
    <>
      <Row>
        <Header />
      </Row>

      <Container className="black-box2">
        {/* Add a white card around prof information */}
        <div className="card">
          {/* Create a container to display the professor information and centers the information*/}
          <table
            className="professor-info"
            align="center"
            style={{ width: "100%" }}
          >
            {/* Professor Name */}
            <tr style={{ textAlign: "center" }}>
              <td>
                <h1 style={{ fontSize: "xxx-large" }}>{professor.name}</h1>
              </td>
            </tr>

            {/* Department Information */}
            <tr>
              <td style={{ textAlign: "center" }}>
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <h5 className="bold-heading-style">Department</h5>
                  <h5 className="heading-style">{"  : " + professor.dept}</h5>
                </div>
              </td>
            </tr>

            {/* RMP Rating */}
            <tr>
              <td style={{ textAlign: "center" }}>
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <h5 className="bold-heading-style">
                    {"RateMyProfessor Rating (" +
                      professor.RMPTotalRatings +
                      " total ratings)"}
                  </h5>
                  <h5 className="heading-style">
                    {"  : " + professor.RMPRating + "/5"}
                  </h5>
                </div>
              </td>
            </tr>

            {/* RMP Rating Class */}
            <tr>
              <td style={{ textAlign: "center" }}>
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <h5 className="bold-heading-style">
                    {"RateMyProfessor Rating Class"}
                  </h5>
                  <h5 className="heading-style">
                    {" "}
                    {"  : " + professor.RMPRatingClass}{" "}
                  </h5>
                </div>
              </td>
            </tr>
          </table>
        </div>

        <div style={{ textAlign: "center", paddingTop: "50px" }}>
          {/* Add a header that says Recently Taught Courses */}
          <h5 className="bold-heading-style">
            Previously Taught Courses ({courses.length} courses found):
          </h5>
        </div>

        {/* For each course in the courses array, create a new row with the course code and the course name */}
        {courses.length > 0 && (
          // Create a column with content centered
          <table
            className="course-info"
            align="center"
            style={{ width: "100%" }}
          >
            <Col className="d-flex justify-content-center">
              <tr className="course-list">
                <td>
                  {courses.map(
                    (
                      course // map the courses array to a new array of rows
                    ) => (
                      <p
                        className="course-list-item" // set the class of the row to course-list-item
                        key={course.id} // set the key as the course id
                        onClick={() => {
                          // set the onClick function to navigate to the course page for the course at the course id
                          navigate({
                            pathname: `/course/${course.id}`,
                          });
                        }}
                      >
                        <h6 className="course-id">
                          {course.code + " : "}{" "}
                          <bold style={{ color: "#FF7787" }}>
                            {course.name}
                          </bold>
                        </h6>
                      </p>
                    )
                  )}
                </td>
              </tr>
            </Col>
          </table>
        )}
      </Container>
    </>
  );
};

export default Instructor;
