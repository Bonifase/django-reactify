import React from "react";
import ReactDom from "react-dom";
import App from './components/App'
import axios from "axios";
import { BrowserRouter as Router } from "react-router-dom";
import { Provider } from "react-redux";
import store from "./redux/store";

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = 'XSRF-TOKEN';

ReactDom.render(<Router><Provider store={store}><App /></Provider></Router>, document.getElementById("app"));