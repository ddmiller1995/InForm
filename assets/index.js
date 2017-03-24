import React from "react";
import {AppContainer} from 'react-hot-loader';
import {render} from "react-dom";

import App from "./components/app.jsx";
import Homepage from "./components/homepage.jsx";

render(<AppContainer><App/></AppContainer>, document.getElementById("app"));
