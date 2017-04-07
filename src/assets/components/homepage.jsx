import React from "react";
import {Link, IndexLink} from "react-router";
import YouthTracker from "./youth-tracker.jsx";
import "whatwg-fetch";

export default class extends React.Component {
      constructor(props) {
          super(props);
          this.state = {};
      }
      
      render() {
          return (
              <div className="container">
                  <div>
                      <IndexLink className="progress-link" to="/progress" activeClassName="active">Progress Report</IndexLink>
                      <a href="#presentation" className="presentation-link">Presentation View</a>
                  </div>
                  <YouthTracker />
              </div>
          );
      }
 }