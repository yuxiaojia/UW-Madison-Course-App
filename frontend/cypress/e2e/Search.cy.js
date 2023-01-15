/**
 * Authors: Aidan Shine, Bryan Li, Jarvis Jia, Peter Bryant, Swathi Annamaneni, Tong Yang
 * Revision History: 11/01/2022:12/13/2022
 * Organization: Madgers
 * Version: 1.0.0
 */

/* eslint-disable cypress/no-unnecessary-waiting */

/**
 * Search.cy.js
 * End to End Test: Search.jsx
 * Tests making connection with backend and retrieving data in search bar
 */

// Test search bar retrieves correct number of courses and professors
describe("Search", () => {
  it("Search bar successfully retrieves all courses and professors", () => {
    cy.visit("localhost:3000/");
    cy.get("input").then((search_bar) => {
      search_bar.click();
      cy.wait(1000); // Wait for endpoint to load data
      cy.get("div[id='search']").then((result) => {
        const search = result[1].children;
        expect(search).to.have.length(102); // This number is the expected length of the array that is populated when the search bar is created
      });
    });
  });
});
