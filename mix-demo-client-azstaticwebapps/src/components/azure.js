import axios from "axios"
import {ROOT_URL} from "./shared"

const suggestApiUrl = `${ROOT_URL}/api/suggest`
const autoCompleteApiUrl = `${ROOT_URL}/api/autocomplete`
const translateApiUrl = `${ROOT_URL}/api/translate`

const doGet = async(url) => {
    return await axios.get(url)
}

const doPost = async(url, data) => {
    return await axios.post(url, data)
}

export const callSuggestAPI = async (textInput) => {
    let result = ''
    try {
        //console.log("**textInput**" + textInput + "**")
        const geturl = `${suggestApiUrl}?q=${textInput}`
        //console.log("**geturl**" + geturl + "**")
        const response = await doGet(geturl)
        //console.log("**response**" + JSON.stringify(response) + "**")
        //console.log("**response.data**" + JSON.stringify(response.data) + "**")
        result = { response: response.data, error: null }
    } catch (error) {
        console.log('Request error', suggestApiUrl, error);
        result = { response: null, error }
    }
    return result
}

export const callAutocompleteAPI = async (textInput) => {
    let result = ''
    try {
        //console.log("**textInput**" + textInput + "**")
        const geturl = `${autoCompleteApiUrl}?q=${textInput}`
        //console.log("**geturl**" + geturl + "**")
        const response = await doGet(geturl)
        //console.log("**response**" + JSON.stringify(response) + "**")
        //console.log("**response.data**" + JSON.stringify(response.data) + "**")
        result = { response: response.data, error: null }
    } catch (error) {
        console.log('Request error', autoCompleteApiUrl, error);
        result = { response: null, error }
    }
    return result
}

export const callTranslateAPI = async (textInput, toLang, fromLang) => {
    let result = ''
    try {
        // console.log("**textInput**" + textInput + "**")
        const geturl = `${translateApiUrl}?q=${textInput}&to=${toLang}&from=${fromLang}`
        // console.log("**geturl**" + geturl + "**")
        const response = await doGet(geturl)
        //console.log("**response**" + JSON.stringify(response) + "**")
        //console.log("**response.data**" + JSON.stringify(response.data) + "**")
        result = { response: response.data, error: null }
    } catch (error) {
        console.log('Request error', translateApiUrl, error);
        result = { response: null, error }
    }
    return result
}
