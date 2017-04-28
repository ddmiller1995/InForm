import React from "react";
import {Link, IndexLink} from "react-router";
import "whatwg-fetch";

import "../css/main.css";

export default class extends React.Component {
      constructor(props) {
          super(props);
          this.state = {};
      }
      
      render() {
          return (
              <div className="container">
                  <h3>Progress Report</h3>
              </div>
          );
      }
 }