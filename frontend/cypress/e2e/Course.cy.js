/**
 * Authors: Aidan Shine, Bryan Li, Jarvis Jia, Peter Bryant, Swathi Annamaneni, Tong Yang
 * Revision History: 11/01/2022:12/13/2022
 * Organization: Madgers
 * Version: 1.0.0
 */

/**
 * Course.cy.js
 * End to End Test: Course.jsx
 * Tests making connection with backend and retrieving data in course page
 */

// Test to make sure that visiting course pages are working
describe("Test Visiting Courses", () => {
  it("T1: Visits MATH 221 and displays entire course page information", () => {
    cy.visit("http://localhost:3000/course?id=79922");
  });

  it("T2: Visits CS200 and displays entire course page information", () => {
    cy.visit("http://localhost:3000/course?id=79778");
  });

  it("T3: Visits CS202 and displays entire course page information", () => {
    cy.visit("http://localhost:3000/course?id=79779");
  });

  it("T4: Visits CS300 and displays entire course page information", () => {
    cy.visit("http://localhost:3000/course?id=79785");
  });

  it("T5: Visits CS400 and displays entire course page information", () => {
    cy.visit("http://localhost:3000/course?id=79794");
  });
});

// Test to make sure that content on course page is rendered
describe("Test Contents of Course Page", () => {
  it("T1: Contains Web Page Title", () => {
    cy.visit("http://localhost:3000/course?id=79922");
    cy.contains("Madger Courses");
  });

  it("T2: Contains Subject", () => {
    cy.visit("http://localhost:3000/course?id=79922");
    cy.contains("Subject");
  });

  it("T3: Contains Credits", () => {
    cy.visit("http://localhost:3000/course?id=79922");
    cy.contains("Credits");
  });

  it("T4: Contains Description", () => {
    cy.visit("http://localhost:3000/course?id=79922");
    cy.contains("Description");
  });

  it("T5: Contains Instructors", () => {
    cy.visit("http://localhost:3000/course?id=79922");
    cy.contains("Instructors");
  });

  it("T6: Contains Instructors", () => {
    cy.visit("http://localhost:3000/course?id=79922");
    cy.contains("Instructors");
  });

  it("T7: Contains Course Title", () => {
    cy.visit("http://localhost:3000/course?id=79922");
    cy.get("[class$=bold-heading-style]");
    cy.get("[class$=heading-style]");
  });

  it("T8: Contains Reddit Icon", () => {
    cy.visit("http://localhost:3000/course?id=79922");
    cy.get("[alt$=reddit-logo]");
  });

  it("T9: Contains Graph", () => {
    cy.visit("http://localhost:3000/course?id=79922");
    cy.get("[class$=recharts-wrapper]");
  });

  it("T10: Contains Reddit Box", () => {
    cy.visit("http://localhost:3000/course?id=79922");
    cy.get("[class$=reddit-box-body]");
  });

  it("T11: Contains Search bar", () => {
    cy.visit("http://localhost:3000/course?id=79922");
    cy.get("[class$=rbt]");
  });

  it("T12: Contains Professor List", () => {
    cy.visit("http://localhost:3000/course?id=79922");
    cy.get("[class$=professor-list]");
  });
});
