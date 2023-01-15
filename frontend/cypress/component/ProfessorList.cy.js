/**
 * Authors: Aidan Shine, Bryan Li, Jarvis Jia, Peter Bryant, Swathi Annamaneni, Tong Yang
 * Revision History: 11/01/2022:12/13/2022
 * Organization: Madgers
 * Version: 1.0.0
 */

import ProfessorList from "../../src/components/ProfessorList";

/**
 * ProfessorList.cy.js
 * Component Test: ProfessorList.jsx
 * Tests component render
 */

describe("ProfessorList", () => {
  // Test component rendered on page
  it("Rendered", () => {
    // Test data to pass into ProfessorList
    var professor = {};
    professor[150940] = {
      aCount: 1215,
      abCount: 1250,
      bCount: 967,
      bcCount: 446,
      cCount: 203,
      crCount: 0,
      dCount: 68,
      fCount: 36,
      iCount: 4,
      nCount: 0,
      name: "John Wild",
      nrCount: 8,
      nwCount: 3,
      otherCount: 1,
      pCount: 0,
      sCount: 55,
      total: 4260,
      uCount: 4,
    };
    cy.mount(<ProfessorList professorList={professor} />);
    cy.get("div").should("have.class", "recharts-wrapper");
  });
});
