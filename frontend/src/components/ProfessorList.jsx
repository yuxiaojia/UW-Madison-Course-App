/**
 * Authors: Aidan Shine, Bryan Li, Jarvis Jia, Peter Bryant, Swathi Annamaneni, Tong Yang
 * Revision History: 11/01/2022:12/12/2022
 * Organization: Madgers
 * Version: 1.0.0
 */

import React from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { useNavigate } from "react-router-dom";
import {
  BarChart,
  CartesianGrid,
  YAxis,
  XAxis,
  Tooltip,
  Legend,
  Bar,
} from "recharts";

/**
 * ProfessorList: Contains each instructor that teaches a particular course, as
 * well as their department, rate my professor rating, average GPA, and a graph
 * showing their average grade distribution for the class (GPAGraph).
 * This component is used by Course.
 * @param {*} professorList list containing name, RMPRating, dept,
 * RMPRatingClass, id, and GPAgraph info for each professor that teaches a
 * certain course--determined in Course
 * @returns ProfessorList React element
 *
 * @component
 * @example
 * professor = { name, RMPRating, dept, RMPRatingClass, id, graph }
 * professorList = [professor]
 * <ProfessorList professorList={professorList} />
 */
const ProfessorList = ({ professorList }) => {
  const navigate = useNavigate(); // useNavigate hook which is used to navigate to a different route

  return (
    <div className="professor-list">
      {/* Map each professor to a seperate container */}
      {professorList.map((prof) => (
        <Container key={prof.id} className="professor-list-item">
          <Row
            onClick={() => {
              // Navigates to corresponding professor upon clicking instructor box
              navigate({
                pathname: `/instructor/${prof.id}`,
              });
            }}
          >
            <Col xs={prof.graph && prof.graph.length > 0 ? undefined : 12}>
              {/* Professor Name */}
              <Row>
                <h6 className="center">
                  {/* Professor Name */}
                  <b>{prof.name}</b>
                </h6>
              </Row>
              <Row>
                <p> </p>
              </Row>

              {/* Professor Department */}
              <Row>
                <h6 className="center">
                  <b>{"Dept"}</b>
                </h6>
              </Row>
              <Row>
                {/* Professor Department */}
                <h6 className="center">{prof.dept}</h6>
              </Row>

              {/* Professor Rating */}
              <Row>
                <h6 className="center">
                  <b>{"Rating"}</b>
                </h6>
              </Row>
              <Row>
                <h6 className="center">
                  {/* Professor rating out of 5 */}
                  {prof.RMPRating + "/5, " + prof.RMPRatingClass}
                </h6>
              </Row>
            </Col>

            {/* Professor Graph */}
            {prof.graph && prof.graph.length > 0 && (
              <Col xs={8}>
                <BarChart width={300} height={200} data={prof.graph}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />{" "}
                  {/**XAxis displays the name label of each object in the array **/}
                  <YAxis dataKey="grade" />{" "}
                  {/**XAxis displays the grade label of each object in the array **/}
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="grade" fill="#FF7787" />
                </BarChart>
              </Col>
            )}
          </Row>
        </Container>
      ))}
    </div>
  );
};

export default ProfessorList;
