document.addEventListener('DOMContentLoaded',function() {
    document.getElementById('url-input').oninput=changeEventHandler;
},false);

function changeEventHandler(event) {
    const imageSignerUrl = `${imageSignerPath}?url=${btoa(event.target.value)}`;
    console.log("Request url: ", imageSignerUrl);
    fetch(imageSignerUrl, {
        headers: {"x-api-key": apiKey}
    }).then(resp => resp.json()).then(json => {
        document.getElementById('signed-url').innerText = json.iguim_url;
        document.getElementById('image-preview').src = json.iguim_url;
        console.log("Response from signer API", json);
        console.log("Url using resizer", json.iguim_url);
    });

}
