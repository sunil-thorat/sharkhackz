import axios from "axios"
import {ROOT_URL} from "./shared"

const suggestApiUrl = `${ROOT_URL}/api/suggest`

const doGet = async(url) => {
    return await axios.get(url)
}

const doPost = async(url, data) => {
    return await axios.post(url, data)
}

export function callSuggestAPI(textInput) {
    let result = ''
    try {
        console.log("**textInput**" + textInput + "**")
        const geturl = `${suggestApiUrl}?q=${textInput}`
        console.log("**geturl**" + geturl + "**")
        const suggestions = doGet(geturl)
        console.log("**suggestions**" + suggestions + "**")
        result = { response: suggestions, error: null }
    } catch (error) {
        console.log('Request error', suggestApiUrl, error);
        result = { response: null, error }
    }
    return result
}
