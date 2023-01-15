/**
 * Authors: Aidan Shine, Bryan Li, Jarvis Jia, Peter Bryant, Swathi Annamaneni, Tong Yang
 * Revision History: 11/01/2022:12/13/2022
 * Organization: Madgers
 * Version: 1.0.0
 */

/* eslint-disable cypress/no-unnecessary-waiting */

/**
 * Instructor.cy.js
 * End to End Test: Instructor.jsx
 * Tests making connection with backend and retrieving data in instructor page
 */

// Test to make sure that visiting instructor pages are working
describe("Test Visiting Instructor Page", () => {
  it("T1: Visiting Marc Renault ", () => {
    cy.visit("http://localhost:3000/instructor?id=149553");
  });
});

// Test to make sure that content on instructor page is rendered
describe("Test Contents of instructor Page", () => {
  it("T1: Contains Instructor Name", () => {
    cy.visit("http://localhost:3000/instructor?id=149553");
    cy.wait(1000); // Wait for endpoint to load data
    cy.contains("Marc Renault");
  });

  it("T2: Contains Instructor Department", () => {
    cy.visit("http://localhost:3000/instructor?id=149553");
    cy.wait(1000); // Wait for endpoint to load data
    cy.contains("Computer Science");
  });

  it("T3: Contains RateMyProfessor", () => {
    cy.visit("http://localhost:3000/instructor?id=149553");
    cy.wait(1000); // Wait for endpoint to load data
    cy.contains("RateMyProfessor");
  });

  it("T4: Contains Previously Taught", () => {
    cy.visit("http://localhost:3000/instructor?id=79922");
    cy.wait(1000); // Wait for endpoint to load data
    cy.contains("Previously Taught instructors");
  });
});
