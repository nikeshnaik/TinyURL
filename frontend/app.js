document.getElementsByClassName("shorten-link--primary")[0].style.display = 'none'
document.getElementsByClassName("btn--copy")[0].style.display = 'none'





function generateLink(event) {



    longurl = document.getElementsByClassName("input-text")[0].value
    console.log(longurl)
    getLongURL(longurl)
    document.getElementsByClassName("btn--copy")[0].textContent = "Copy!"
    cleanUpText()
}

function onEnterTextbox(event) {
    if (event.which == 13 | event.keyCode == 13) {
        longurl = document.getElementsByClassName("input-text")[0].value
        console.log(longurl)
        getLongURL(longurl)
    }


}

function cleanUpText() {
    document.getElementsByClassName("input-text")[0].value = ""
}

function copyText(event) {
    textarea_element = document.getElementsByClassName("shorten-link--primary")[0]
    navigator.clipboard.writeText(textarea_element.textContent).then(function () {
        document.getElementsByClassName("btn--copy")[0].textContent = "Copied!!!"
    })
}

document.getElementsByClassName("btn--copy")[0].addEventListener("click", copyText)
document.getElementsByClassName("btn")[0].addEventListener("click", generateLink)
document.getElementsByClassName("input-text")[0].addEventListener("keyup", onEnterTextbox)



function getLongURL(longurl) {
    if (longurl) {
        const post_data = {
            api_dev_key: "6f41c86d-2622-4752-80aa-8d28849aeb1d",
            original_url: longurl
        }

        backend_server_url = "https://www.cloned-link.com"
        fetch(backend_server_url + "/v1/encode-url/", {
            method: 'POST',
            credentials:true,
            headers: {
                'Content-Type': 'application/json',


            },
            body: JSON.stringify(post_data)

        }).then(response => response.json()).then(data => { console.log({ "Success": data }) }).then(err => { console.error({ 'err': err }) })

        // console.log(response)
        console.log(data)
        encodeURI = data["msg"]
        



        document.getElementsByClassName("btn--copy")[0].style.display = 'inline-block'
        document.getElementsByClassName("shorten-link--primary")[0].textContent = encodedURL
        document.getElementsByClassName("shorten-link--primary")[0].style.display = 'inline-block'


        document.getElementsByClassName('')
    }
}