import React from "react";
// polyfill for Safari and older browser
import "whatwg-fetch";

import "../css/main.css";

export default class extends React.Component {
      constructor(props) {
          super(props);
          this.state = {};
      }
      
    //   render() {
    //       return (
    //           <h2>Running React hot compiler - edited again!</h2>
    //       );
    //   }
      
      render() {
          return (
              <div className="mdl-layout mdl-js-layout mdl-layout--fixed-header">
                  <header className="mdl-layout__header">
                      <div className="mdl-layout__header-row">
                          <span className="mdl-layout-title">Youth Haven Portal</span>
                          <div className="mdl-layout-spacer"></div>
                          <nav className="mdl-navigation">
                              <a className="mdl-navigation__link" href="#">Home</a>
                              <div className="header-divider"></div>
                              <a className="mdl-navigation__link" href="#">Admin</a>
                              <div className="header-divider"></div>
                              <a className="mdl-navigation__link" href="#">Logout</a>
                          </nav>
                      </div>
                  </header>
                  <main>
                      {this.props.children}
                  </main>
              </div>
          );
      }
 }
