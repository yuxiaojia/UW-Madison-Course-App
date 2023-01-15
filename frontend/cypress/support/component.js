/**
 * Authors: Aidan Shine, Bryan Li, Jarvis Jia, Peter Bryant, Swathi Annamaneni, Tong Yang
 * Revision History: 11/01/2022:12/13/2022
 * Organization: Madgers
 * Version: 1.0.0
 */

// Import commands.js using ES2015 syntax:
import "./commands";

import { mount } from "cypress/react18";
import { MemoryRouter } from "react-router-dom";

/**
 * component.js
 * Mounts router options to components when component testing
 */

// Give component access to React Router
Cypress.Commands.add("mount", (component, options = {}) => {
  const { routerProps = { initialEntries: ["/"] }, ...mountOptions } = options;
  const wrapped = <MemoryRouter {...routerProps}>{component}</MemoryRouter>;
  return mount(wrapped, mountOptions);
});
