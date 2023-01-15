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
import { useParams } from "react-router-dom";
import GPAGraph from "./GPAGraph";
import Reddit from "./Reddit";
import ProfessorList from "./ProfessorList";

/**
 * Course: displays Header and all course info: basic course info, cumulative
 * GPA graph, list of reddit comments, and info on instructors that teach that
 * course.
 * @returns Course React element
 *
 * @component
 */
const Course = () => {
  const courseID = useParams().id; // get the value of the id param

  const [courseInfo, setCourseInfo] = useState({}); // useState hook to store the courseInfo
  const [redditList, setRedditList] = useState([]); // useState hook to store the redditList
  const [graphInfo, setGraphInfo] = useState({}); // useState hook to store the graphInfo
  const [professorList, setProfessorList] = useState([]); // useState hook to store the professorList
  const [profGraphInfo, setProfGraphInfo] = useState([]); // useState hook to store the profGraphInfo

  // fetch course info for a particular courseID
  useEffect(() => {
    fetch("https://3.145.22.97/course-info/" + courseID).then((response) =>
      response
        .json()
        .then((json) => {
          setCourseInfo(json);
        })
        .catch((e) => console.log("error loading courses from backend ", e))
    );
  }, [courseID]);

  // fetch professor graph info for a particular courseInfo, courseID to be used in fetching from /course-profs
  // fetch overall gpa graph info for a particular courseInfo, courseID
  // The returned gpa graph distribution for this course is converted into the
  //    required format for our graph API
  useEffect(() => {
    fetch("https://3.145.22.97/grade-distribution/" + courseID)
      .then((response) => response.json())
      .then((json) => {
        // if the response is valid
        if (json && json["professor_cumulative_grade_distribution"])
          setProfGraphInfo(json["professor_cumulative_grade_distribution"]);
        else setProfGraphInfo({});

        // if the graph is not empty
        if (
          json &&
          json.cumulative &&
          !(
            json.cumulative.aCount === 0 &&
            json.cumulative.abCount === 0 &&
            json.cumulative.bCount === 0 &&
            json.cumulative.bcCount === 0 &&
            json.cumulative.cCount === 0 &&
            json.cumulative.dCount === 0 &&
            json.cumulative.fCount === 0
          )
        )
          setGraphInfo([
            { name: "A", grade: json.cumulative.aCount },
            { name: "AB", grade: json.cumulative.abCount },
            { name: "B", grade: json.cumulative.bCount },
            { name: "BC", grade: json.cumulative.bcCount },
            { name: "C", grade: json.cumulative.cCount },
            { name: "D", grade: json.cumulative.dCount },
            { name: "F", grade: json.cumulative.fCount },
          ]);
        else setGraphInfo([]);
      })
      .catch((e) => console.log("error while calling grade-distribution API"));
  }, [courseInfo, courseID]);

  // fetch professor list and professor GPA info for a particular profGraphInfo, courseID to be used in ProfessorList component
  useEffect(() => {
    fetch("https://3.145.22.97/course-profs/" + courseID)
      .then((response) =>
        response.json().then((json) => {
          var professors = [];
          // For professor course in the json response, create a new object with
          // the professor name, rate my professor rating, department, rate my
          // professor rating class, and professor ID
          for (var key in json) {
            const name = json[key].name;
            const RMPRating = json[key].RMPRating;
            const dept = json[key].dept;
            const RMPRatingClass = json[key].RMPRatingClass;
            const id = key;

            let graph = {}; // populate professor graph with prof-specific GPA's
            if (profGraphInfo.hasOwnProperty(id)) {
              const temp = profGraphInfo[id];
              if (
                // if no prof graph info exists, make an empty graph
                temp.aCount === 0 &&
                temp.abCount === 0 &&
                temp.bCount === 0 &&
                temp.bcCount === 0 &&
                temp.cCount === 0 &&
                temp.dCount === 0 &&
                temp.fCount === 0
              )
                graph = [];
              // otherwise, set the values of graph to
              else
                graph = [
                  { name: "A", grade: temp.aCount ?? 0 },
                  { name: "AB", grade: temp.abCount ?? 0 },
                  { name: "B", grade: temp.bCount ?? 0 },
                  { name: "BC", grade: temp.bcCount ?? 0 },
                  { name: "C", grade: temp.cCount ?? 0 },
                  { name: "D", grade: temp.dCount ?? 0 },
                  { name: "F", grade: temp.fCount ?? 0 },
                ];
            }
            professors.push({
              // push the new object to the professors list
              name,
              RMPRating,
              dept,
              RMPRatingClass,
              id,
              graph,
            });
          }
          setProfessorList(professors); //set the ProfessorList state as the professors array
        })
      )
      .catch((e) => console.log("error while calling course-profs API", e));
  }, [profGraphInfo, courseID]);

  // fetch Reddit comments for a particular courseInfo, courseID to be used in Reddit component, sorting by popularity
  useEffect(() => {
    fetch("https://3.145.22.97/reddit-comments/" + courseID)
      .then((response) =>
        response.json().then((json) => {
          var comments = [];
          // for each comment in the json response, create a new object with the comment body, comment link, and number of votes
          for (var key in json) {
            const id = key;
            const body = json[key].comBody;
            const link = json[key].comLink;
            const votes = json[key].comVotes;

            comments.push({ id, body, link, votes }); // push the new object to the comments list
          }
          comments.sort((a, b) => {
            // Sorting in descending order based on upvotes
            return b.votes - a.votes;
          });
          setRedditList(comments); // set the RedditList state as the comments array
        })
      )
      .catch((e) => console.log("error while loading reddit threads ", e));
  }, [courseInfo, courseID]);

  return (
    <Container className="full">
      <Row>
        <Header />
      </Row>

      <Container className="grey-box full">
        {
          /* Course Name */
          courseInfo.cName && (
            <Row>
              <h3 className="bold-heading-style">{courseInfo.cName}</h3>
            </Row>
          )
        }

        {
          /* Course Code */
          courseInfo.cCode && (
            <Row className="heading-style">
              <h3>{courseInfo.cCode}</h3>
            </Row>
          )
        }

        <Row>
          {
            /* Course Subject */
            courseInfo.cSubject && (
              <Col>
                <Row>
                  <h5 className="bold-heading-style">Subject</h5>
                </Row>
                <Row>
                  <h5 className="heading-style">{courseInfo.cSubject}</h5>
                </Row>
              </Col>
            )
          }

          {
            /* Course Credits */
            courseInfo.cSubject && (
              <Col>
                <Row>
                  <h5 className="bold-heading-style">Credits</h5>
                </Row>
                <Row>
                  <h5 className="heading-style">{courseInfo.cCredits}</h5>
                </Row>
              </Col>
            )
          }
        </Row>

        {
          /* Course Description */
          courseInfo.cSubject && (
            <>
              <Row>
                <h5 className="bold-heading-style">Description</h5>
              </Row>
              <Row>
                <h5 className="heading-style">{courseInfo.cDescription}</h5>
              </Row>
            </>
          )
        }

        {
          /* Course Requisites */
          courseInfo.cReq && (
            <Row>
              <h5 className="heading-style">
                <b>Requisites</b>
                {": " + courseInfo.cReq}
              </h5>
            </Row>
          )
        }

        {/* Cumulative Course GPA Graph and Reddit*/}
        <Row>
          {graphInfo && // if there is graph data and reddit data, make a row to
          // hold them
          graphInfo.length > 0 &&
          redditList &&
          redditList.length > 0 ? (
            <Col>
              {graphInfo && graphInfo.length > 0 ? ( // if there is graph data, display the graph
                <div xs={12} lg={6} className="graph-box">
                  <GPAGraph graphInfo={graphInfo} />
                </div>
              ) : (
                <></>
              )}

              {redditList && redditList.length > 0 ? ( // if there is reddit info display reddit comments
                <Row xs={12} md={6} className="reddit-box">
                  <Reddit redditList={redditList} />
                </Row>
              ) : (
                <></>
              )}
            </Col>
          ) : (
            <></>
          )}

          {/* Professor List and Associating Professor GPA Graph(s) */}
          {professorList && professorList.length > 0 ? (
            <Col xs={12} lg={6}>
              <Row>
                <h5 className="bold-heading-style">Instructors</h5>
              </Row>
              <Row xs={12} lg={6} className="professor-list-container">
                {<ProfessorList professorList={professorList} />}
              </Row>
            </Col>
          ) : (
            // if there is no prof info, tell the user
            <>
              <h5 className="heading-style">
                No Intructor Info found for this course
              </h5>
            </>
          )}
        </Row>
      </Container>
    </Container>
  );
};

export default Course;
