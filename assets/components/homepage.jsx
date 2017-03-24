import React from "react";
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
                  <YouthTracker />
              </div>
          );
      }
 }