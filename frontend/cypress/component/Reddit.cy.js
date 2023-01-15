/**
 * Authors: Aidan Shine, Bryan Li, Jarvis Jia, Peter Bryant, Swathi Annamaneni, Tong Yang
 * Revision History: 11/01/2022:12/13/2022
 * Organization: Madgers
 * Version: 1.0.0
 */

import Reddit from "../../src/components/Reddit";

/**
 * Reddit.cy.js
 * Component Test: Reddit.jsx
 * Tests component render
 */

describe("Reddit", () => {
  // Test component rendered on page
  it("Rendered", () => {
    cy.mount(<Reddit />);
    cy.get("div").should("have.class", "reddit-box-body");
  });
});
