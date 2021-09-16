import axios from "axios"
import {ROOT_URL} from "./shared"

const suggestApiUrl = `${ROOT_URL}/api/suggest`

function doGet(url) {
    axios.get(url).then(res => {
        return res
    })
}

function doPost(url, data) {
    axios.post(url, data).then(res => {
        return res
    })
}

export function callSuggestAPI(textInput) {
    let result = ''
    try {
        const requestData = {
            q: textInput
        }
        const response = doPost(suggestApiUrl, requestData)
        if (response.status != 200) {
            throw Error('Invalid HTTP response status code returned - ' + response.status)
        }
        result = { response: response.data, error: null }
    } catch (error) {
        console.log('Request error', suggestApiUrl, error);
        result = { response: null, error }
    }
    return result
}
