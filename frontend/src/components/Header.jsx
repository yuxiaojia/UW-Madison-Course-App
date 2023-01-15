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
import { LinkContainer } from "react-router-bootstrap";

/**
 * header: white bar with Madger Courses text that links back to homepage
 * contains search bar on left.
 * This component is used by Course, Instructor and Home.
 * @returns Header React element
 *
 * @component
 */
const Header = () => {
  return (
    <Container className="full">
      <Row>
        <LinkContainer to="/">
          {/* Team Logo and Header Text */}
          <Col className="header-start">
            <img className="header-logo" src="/teamLogo.png" alt="team-logo" />
            <h3 className="header-text"> UW </h3>
          </Col>
        </LinkContainer>
      </Row>
    </Container>
  );
};

export default Header;
