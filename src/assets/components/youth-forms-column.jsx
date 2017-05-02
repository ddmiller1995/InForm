import React from "react";
import {Link, IndexLink} from "react-router";
import YouthFormsCategory from "./youth-forms-category.jsx";
import "whatwg-fetch";

let form_categories = ["Intake", "Psych", "Outtake"];

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
    }

    getFormCategories() {
        let temp = {};
        for(let i = 0; i < form_categories.length; i++) {
            temp[form_categories[i]] = [];
        }
        for(let i = 0; i < this.props.forms.length; i++) {
            let form = this.props.forms[i];
            temp[form.form_type].push(form);
        }
        let category_components = [];
        for(let i = 0; i < form_categories.length; i++) {
            let current = form_categories[i];
            console.log(current);
            category_components.push(<YouthFormsCategory key={current} category={current} forms={temp[current]} />)
        }

        return category_components;
    }

      
    render() {
        let categories = this.getFormCategories();

        return (
            <div className="col">
                <header className="mdl-layout__header is-casting-shadow">
                    <div className="mdl-layout__header-row">
                        <span className="mdl-layout-title">{this.props.status}</span>
                    </div>
                </header>
                {categories}
            </div>
        );
    }
}