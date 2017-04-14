import Patch from 'react-hot-loader/patch';
import React from "react";
import {AppContainer} from 'react-hot-loader';
import {render} from "react-dom";

import App from "./components/app.jsx";
import Homepage from "./components/homepage.jsx";
import Presentation from "./components/presentation.jsx";
import ProgressReport from "./components/progress-report.jsx";
import Youth from "./components/youth.jsx";
import YouthInfo from "./components/youth-info.jsx";
import YouthProgress from "./components/youth-progress.jsx";
import AddYouth from "./components/add-youth.jsx";

import {Router, Route, IndexRoute, hashHistory} from "react-router";

"use strict";

var router = (
    <Router history={hashHistory}>
        <Route path="/" component={App}>
            <IndexRoute component={Homepage}></IndexRoute>
            <Route path="/progress" component={ProgressReport}></Route> 
            <Route path="/presentation" component={Presentation}></Route> 
            <Route path="/add" component={AddYouth}></Route> 
            <Route path="/youth" component={Youth}>
                <IndexRoute component={YouthInfo}></IndexRoute>
                <Route path="/youth/progress" component={YouthProgress}></Route> 
            </Route> 
        </Route> 
    </Router>
);

render(router, document.getElementById("app"));
