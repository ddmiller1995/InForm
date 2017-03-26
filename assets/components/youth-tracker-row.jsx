import React from 'react';
import {Link, IndexLink} from "react-router";
import "whatwg-fetch";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    handleClick(youth) {
        console.log(youth.name + " was clicked");
        this.setState({youth: youth});
    }

    render() {
        return (
            <tr>
                <td className="mdl-data-table__cell--non-numeric">
                    <IndexLink 
                        className="mdl-navigation__link" 
                        to="/youth"
                        key={this.props.youth.name} 
                        onClick={event => this.handleClick(this.props.youth)}>
                        {this.props.youth.name}
                    </IndexLink>
                </td>
                <td>11/12/2001</td>
                <td>2/13/2017</td>
                <td>Progress</td>
                <td>Progress</td>
                <td>Progress</td>
                <td>3/2/2017</td>
            </tr>
        );
    } 
}