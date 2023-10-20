import '../sass/project.scss';
// import "izitoast/dist/css/iziToast.min.css";

import htmx from "htmx.org/dist/htmx";
import Alpine from "alpinejs";

// import iziToast from "izitoast/dist/js/iziToast.min.js";
import "flowbite";

window.htmx = htmx;
// // initialize tinymce
window.tinymce = tinymce;
// initialize axios async post|get request
window.axios = axios;
// initiailize izitoast alerts
window.iziToast = iziToast;

window.Alpine = Alpine;

Alpine.start();

/* Project specific Javascript goes here. */
