import React from "react";
// polyfill for Safari and older browser
import "whatwg-fetch";

export default class extends React.Component {
      constructor(props) {
          super(props);
          this.state = {};
      }

      render() {
          return (
              <h1>Running React hot compiler!</h1>
          );
      }
 }
