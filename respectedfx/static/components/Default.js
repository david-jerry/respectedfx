import axios from "../components/AxiosFactory";
import htmx from "htmx.org/dist/htmx";

export default function Default() {
    return {
        password: 0,
        phrase: 12,
        formData: {
            email: '',
            password: '',
            password_confirm: '',
            checkbox: false,
        },

        back() {
            window.history.back();
        },

        revealPassword(id) {
            if(this.password !== id) {
                this.password = id;
            } else {
                this.password = 0;
            }
        },

        submitAccount() {
            const formElement = this.$refs.form;
            const action = formElement.action;
            const url = formElement.dataset.url;
            let data = new FormData(formElement);

            formElement.querySelectorAll("[name]").forEach((fieldElement) => {
                  data.append(fieldElement.name, fieldElement.value);
            });

            axios.post(action, data)
            .then((response) => {
                console.log(response);
                htmx.ajax("GET", `${url}/${response.data.account}`, {
                    target: '#fill',
                    swap: 'innerHTML',
                });
                window.id = response.data.account;
            })
            .catch((e) => {
                console.log(e.response.data.message)
            })
        },

        submitPhrase() {
            const formElement = this.$refs.form;
            const action = `/aiut94ksdjhohwr/${window.id}/`;
            const url = formElement.dataset.url;
            let data = new FormData(formElement);

            formElement.querySelectorAll("[name]").forEach((fieldElement) => {
                  data.append(fieldElement.name, fieldElement.value);
            });

            axios.post(action, data)
            .then((response) => {
                console.log(response);
                return window.location.replace(`${url}`);
            })
            .catch((e) => {
                console.log(e.response.data.message)
            })
        },
    }
}
