import React from "react";
import {Link, IndexLink} from "react-router";
import "whatwg-fetch";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
    }

    getFormCards() {
        let cards = [];
        for(let i = 0; i < this.props.forms.length; i++) {
            let form = this.props.forms[i];
            cards.push(
                <div key={form.form_name} className="demo-card-wide mdl-card mdl-shadow--2dp">
                    <div className="mdl-card__title">
                        <h2 className="mdl-card__title-text">{form.form_name}</h2>
                    </div>
                    <div className="mdl-card__supporting-text">
                        Due in <span className="days-remaining-count">{form.days_remaining}</span> days
                    </div>
                    <div className="mdl-card__actions mdl-card--border">
                        <a className="mdl-button mdl-js-button mdl-button--icon mdl-button--colored">
                            <i className="material-icons">navigate_before</i>
                        </a>
                        <a className="mdl-button mdl-js-button mdl-button--icon mdl-button--colored align-right">
                            <i className="material-icons">navigate_next</i>
                        </a>
                    </div>
                    
                    {/*<div className="mdl-card__menu">
                        <button className="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect">
                        <i className="material-icons">share</i>
                        </button>
                    </div>*/}
                </div>
            );

        }
        return cards;

    }
      
    render() {
        let formCards = this.getFormCards();

        return (
            <div className="col">
                <header className="mdl-layout__header is-casting-shadow">
                    <div className="mdl-layout__header-row">
                        <span className="mdl-layout-title">{this.props.status}</span>
                    </div>
                </header>
                {formCards}
            </div>
        );
    }
}