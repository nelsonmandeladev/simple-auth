import axios from "axios";
const BASE_URL = "https://serv-prov-auth.herokuapp.com/api/v1/";

export default axios.create({
    baseURL: BASE_URL
});

export const privateRequest = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-type': 'application/json'
    },
    withCredentials: true
})