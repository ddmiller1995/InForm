import React from "react";
import "whatwg-fetch";

import "../css/main.css";

export default class extends React.Component {
      constructor(props) {
          super(props);
          this.state = {};
      }
      
      render() {
          return (
              <h1>Admin page</h1>
          );
      }
 }