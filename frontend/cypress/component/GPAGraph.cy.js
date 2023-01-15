/**
 * Authors: Aidan Shine, Bryan Li, Jarvis Jia, Peter Bryant, Swathi Annamaneni, Tong Yang
 * Revision History: 11/01/2022:12/13/2022
 * Organization: Madgers
 * Version: 1.0.0
 */

import GPAGraph from "../../src/components/GPAGraph";

/**
 * GPAGraph.cy.js
 * Component Test: GPAGraph.jsx
 * Tests component render
 */

describe("GPAGraph", () => {
  // Test component rendered on page
  it("Rendered", () => {
    cy.mount(<GPAGraph />);
    cy.get("div").should("have.class", "recharts-wrapper");
  });
});
