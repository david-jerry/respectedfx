import axios from "axios";
import { getCSRFToken } from "./CSRFToken";

// const axios_session = axios.create({
//     xsrfCookieName : 'csrftoken',
//     xsrfHeaderName : "X-CSRFToken",
//     withCredentials : true,
//     timeout : 15000
// });
axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.timeout = 25000;

export default axios;
