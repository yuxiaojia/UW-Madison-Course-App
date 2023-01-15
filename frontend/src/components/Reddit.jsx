/**
 * Authors: Aidan Shine, Bryan Li, Jarvis Jia, Peter Bryant, Swathi Annamaneni, Tong Yang
 * Revision History: 11/01/2022:12/12/2022
 * Organization: Madgers
 * Version: 1.0.0
 */

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";

/**
 * Reddit: This component shows Reddit comments about a certain class, using
 * comment specified by redditList.
 * This component is used by Course.
 * @param {*} redditList contains the id, body, link, and number of votes for
 * the Reddit comments about a certain class
 * @returns Reddit React element
 *
 * @component
 * @example
 * comment = { id, body, link, votes }
 * redditList = [comment]
 * <Reddit redditList={redditList} />
 */
const Reddit = ({ redditList }) => {
  return (
    <>
      {/* Reddit box */}
      {redditList && redditList.length > 0 ? ( // if Reddit data exists, display it
        <Container>
          {/* Reddit Logo */}
          <Row className="reddit-box-header">
            <img
              height="124px"
              width="220px"
              src="/Reddit.png"
              alt="reddit-logo"
            />
          </Row>

          <Row className="reddit-box-body">
            {/* Map each professor to a seperate container */}
            {redditList.map((thread) => (
              <p
                onClick={() => {
                  // set the onClick function to link to the URL of the Reddit
                  // comment
                  window.open(thread.link, "_blank");
                }}
                className="reddit-list-item"
                key={thread.id}
              >
                {thread.body}
              </p>
            ))}
          </Row>
        </Container>
      ) : (
        <></>
      )}
    </>
  );
};

export default Reddit;
