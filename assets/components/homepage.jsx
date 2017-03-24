import React from "react";
import {Link, IndexLink} from "react-router";
import "whatwg-fetch";
import YouthTracker from "./youth-tracker.jsx";

import "../css/main.css";

export default class extends React.Component {
      constructor(props) {
          super(props);
          this.state = {};
      }
      
      render() {
          return (
              <div className="container">
                  <h1>Homepage</h1>
                  <div>
                      <IndexLink className="progress-link" to="/progress" activeClassName="active">Progress Report</IndexLink>
                      <a href="#presentation" className="presentation-link">Presentation View</a>
                  </div>
                  <YouthTracker />
              </div>
          );
      }
 }