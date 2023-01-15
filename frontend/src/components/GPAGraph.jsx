/**
 * Authors: Aidan Shine, Bryan Li, Jarvis Jia, Peter Bryant, Swathi Annamaneni, Tong Yang
 * Revision History: 11/01/2022:12/12/2022
 * Organization: Madgers
 * Version: 1.0.0
 */

import React from "react";
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
 * GPAGraph: displays a BAR graph based on info passed in through graphInfo.
 * This component is used by Course.
 * @param {*} graphInfo data to be displayed in graph, determined in Course
 * @returns GPAGraph React element
 *
 * @component
 * @example
 * graphInfo = [
 *  { name: "A", grade: 0 },
 *  { name: "AB", grade: 0 },
 *  { name: "B", grade: 0 },
 *  { name: "BC", grade: 0 },
 *  { name: "C", grade: 0 },
 *  { name: "D", grade: 0 },
 *  { name: "F", grade: 0 }]
 * <GPAGraph graphInfo={graphInfo} />
 */
const GPAGraph = ({ graphInfo }) => {
  // graphInfo set in Course component
  return (
    <BarChart width={400} height={250} data={graphInfo}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />{" "}
      {/**XAxis displays the name label of each object in the array **/}
      <YAxis dataKey="grade" />{" "}
      {/**XAxis displays the grade label of each object in the array **/}
      <Tooltip />
      <Legend />
      <Bar dataKey="grade" fill="#FF7787" />
    </BarChart>
  );
};

export default GPAGraph;
