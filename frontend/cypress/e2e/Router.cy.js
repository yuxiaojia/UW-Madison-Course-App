/**
 * Authors: Aidan Shine, Bryan Li, Jarvis Jia, Peter Bryant, Swathi Annamaneni, Tong Yang
 * Revision History: 11/01/2022:12/13/2022
 * Organization: Madgers
 * Version: 1.0.0
 */

/**
 * Router.cy.js
 * End to End Test: Router.jsx
 * Tests connectivity of router
 */

// Test that routes visit each page successfully
describe("Router", () => {
  beforeEach(() => {
    cy.visit("localhost:3000/");
  });
  it("Visit Home page", () => {
    cy.visit("localhost:3000/");
  });
  it("Visit Course page", () => {
    cy.visit("localhost:3000/course");
  });
  it("Visit Instructor page", () => {
    cy.visit("localhost:3000/instructor");
  });
});
