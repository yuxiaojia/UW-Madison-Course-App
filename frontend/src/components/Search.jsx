/**
 * Authors: Aidan Shine, Bryan Li, Jarvis Jia, Peter Bryant, Swathi Annamaneni, Tong Yang
 * Revision History: 11/01/2022:12/12/2022
 * Organization: Madgers
 * Version: 1.0.0
 */

import React, { useEffect, useState } from "react";
import { Typeahead } from "react-bootstrap-typeahead";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { useNavigate } from "react-router-dom";

/**
 * Search: search bar for users to search by course or instructor.
 * This component is used by Home and Course.
 * @returns Search React element
 *
 * @component
 */
const Search = () => {
  const navigate = useNavigate(); // useNavigate hook which is used to navigate to a different route

  // Initialize class list and professor list
  const [classList, setClassList] = useState([]); // useState hook to store the classList
  const [profList, setProfList] = useState([]); // useState hook to store the profList
  const [selected, setSelected] = useState([]); // useState hook to store the selected

  // fetch class and professor lists
  useEffect(() => {
    // fetch the course list
    fetch("https://3.145.22.97/all-courses").then((response) =>
      response.json().then((json) => {
        var classes = [];
        // for each course in the json response, create a new object with the course code and the course name
        for (var key in json) {
          const code = json[key].cCode;
          const name = json[key].cName;
          const id = json[key].cUID;
          // concatenate class code and name so that either can be used in search
          const classFull = {
            result: code.concat(" - " + name), // Course code is modified to be displayed in Bootstrap Typeahead
            id: id,
          };
          classes.push(classFull); // push the new object to the classes list
        }
        setClassList(classes); // set the class state as the classes array
      })
    );

    // fetch the professor list
    fetch("https://3.145.22.97/all-profs").then((response) =>
      response.json().then((json) => {
        var professors = [];
        // for each professor in the json response, create a new object with the professor name
        for (var key in json) {
          const name = json[key].name;
          const id = key;
          const professorFull = {
            result: name,
            id: id,
          };
          professors.push(professorFull); // push the new object to the professors list
        }
        setProfList(professors); // set the professorList state as the profList array
      })
    );
  }, []);

  const options = classList.concat(profList); // Set Bootstrap Typeahead display options to the classList and profList

  // Submit button navigation
  const submit = (e) => {
    e.preventDefault(); // Prevents page from reloading to blank state
    if (classList.includes(selected[0])) {
      // if selected option is a class
      navigate({
        pathname: `/course/${selected[0].id}`,
      });
    } else if (profList.includes(selected[0])) {
      // if selected option is a professor
      navigate({
        pathname: `/instructor/${selected[0].id}`,
      });
    }
    window.location.reload(true); // Allows page updates
  };

  return (
    // Wrapper for Typeahead to allow submission
    <Form onSubmit={submit}>
      <Form.Group>
        {/* Search box dropdown / Bootstrap Typeahead */}
        <Typeahead
          id="search"
          onChange={setSelected}
          labelKey={(option) => option.result}
          options={options} // Use options list as data
          placeholder="Course or Professor (Ex: COMP SCI 300)"
          selected={selected}
        />
      </Form.Group>
      {/* Submit button */}
      <Button type="submit" hidden></Button>
    </Form>
  );
};

export default Search;
