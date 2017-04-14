import React from "react";
import {Link, IndexLink} from "react-router";
import "whatwg-fetch";

export default class extends React.Component {
      constructor(props) {
          super(props);
          this.state = {};
      }
      
      render() {
          return (
            <div className="container">
                <form id="add-youth-form">     
                    <div id="add-youth-heading">
                        <h2>Add Youth</h2>
                    </div>

                     <div>
                        <label htmlFor="name-input">Name:</label>
                        <input id="name-input" 
                            type="text" 
                            required
                            autoFocus/>
                    </div>
                    
                    <div>
                        <label htmlFor="dob-input">Date of Birth:</label>
                        <input id="dob-input" 
                            type="date"
                            required
                            autoFocus/>
                    </div>

                    <div>
                        <label htmlFor="entry-input">Entry Date:</label>
                        <input id="entry-input" 
                            type="date"
                            required
                            autoFocus/>
                    </div>

                    <div>
                        <label htmlFor="bed-type-input">Bed Type:</label>
                        <input id="bed-type-input" 
                            type="text"
                            required
                            autoFocus/>
                    </div>

                    <button className="mdl-button mdl-js-button mdl-button--raised mdl-button--colored"
                        id="submit-youth-button" type="submit">Add</button>
                </form>
            </div>
          );
      }
 }