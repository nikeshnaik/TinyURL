document.getElementById("shorten-link--primary").style.display = 'none'
document.getElementsByClassName("btn--copy")[0].style.display = 'none'
var decorator = document.getElementById("shorten-link--primary").textContent
var longurl_element = document.getElementsByClassName("input-text")[0]
var longurl = "";
var encodedURL = "";




function generateLink(event) {



    longurl = document.getElementsByClassName("input-text")[0].value
    console.log(longurl)
    getLongURL(longurl)
    document.getElementsByClassName("btn--copy")[0].textContent = "Copy!"
    cleanUpText()
}

function onEnterTextbox(event) {
    if ((event.which == 13 || event.keyCode == 13) && (longurl_element.value!==longurl)) {
        longurl = longurl_element.value
        console.log(longurl)
        getLongURL(longurl).then(console.log)
        

    }


}

function cleanUpText() {
    document.getElementsByClassName("input-text")[0].value = ""

}

function copyText(event) {
    textarea_element = document.getElementById("shorten-link--primary")
    short_link = "www.cloned-link.com/"+ encodedURL
    console.log(short_link)
    navigator.clipboard.writeText(short_link).then(function () {
        
        document.getElementsByClassName("btn--copy")[0].textContent = "Copied!!"
        cleanUpText()

        
    })
}

function resetNewState(event){
    textarea_element = document.getElementById("shorten-link--primary")
    textarea_element.textContent = decorator
    textarea_element.style.display = "none"
    document.getElementsByClassName("btn--copy")[0].textContent = "Copy"
    document.getElementsByClassName("btn--copy")[0].style.display = 'none'
}

document.getElementsByClassName("btn--copy")[0].addEventListener("click", copyText)
document.getElementsByClassName("btn")[0].addEventListener("click", generateLink, {"once":true})
document.getElementsByClassName("input-text")[0].addEventListener("keyup", onEnterTextbox)
document.getElementsByClassName("input-text")[0].addEventListener("input", resetNewState)





async function getLongURL(longurl) {
    
    if (longurl) {
        const post_data = {
            api_dev_key: "6f41c86d-2622-4752-80aa-8d28849aeb1d",
            original_url: longurl
        }
        
        backend_server_url = "https://www.cloned-link.com/encode-url";
        let response = await fetch(backend_server_url, {
            method: 'POST',
            mode:"cors",
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Max-Age' : 600

            },
            body: JSON.stringify(post_data)
        })

        encodedURL = await response.json()

        console.log("encoded data",encodedURL)
        encodedURL = encodedURL["msg"]
        short_url = "www.cloned-app.com/" + encodedURL
        


        document.getElementsByClassName("btn--copy")[0].style.display = 'inline-block'
        document.getElementById("shorten-link--primary").textContent = decorator + short_url
        document.getElementById("shorten-link--primary").style.display = 'inline-block'


        // document.getElementsByClassName('')
    }
}