Image Url Signer Lambda
=======================

This app has been thrown together as a way to make it easy to generated signed URLs for the guardian's image resizer service (Fastly IO). It provides a HTTP endpoint which takes a single parameter - `url` and an api key (passed as a header called `x-api-key`) and returns the signature of the passed url.

# How to use
Requests to the signer require an api key passed as a header, and an image url (typically from media.guim, but sport.guim, static.guim, uploads.guim should also work). You'll also need to decide which features of the resizer you want to use, and build a query string accordingly - e.g. if you want an image 500 pixels wide, you need to add `width=200` to the query string of your image url.

For example, lets say you want to resize this image:  https://media.guim.co.uk/e198ba4ebf78fa6f99437be1cc15bd4c665fcb4e/0_346_5184_3110/master/5184.jpg  (Note the /master/ part of the URL - master assets should always be used when using the resizer)

Let's say we want it at width 200 with 50% compression (pretty high), and to crop it to a 1:1 aspect ratio in javascript the API call would look like this. Note the use of `btoa` to base64 encode the url we're passing in the query string.

```
const mediaUrl = "https://media.guim.co.uk/e198ba4ebf78fa6f99437be1cc15bd4c665fcb4e/0_346_5184_3110/master/5184.jpg?width=1000&crop=1:1&quality=50";
const imageResizerUrl = `${IMAGE_SIGNER_HOST}?url=${btoa(mediaUrl)}`
const resizedUrl = fetch(imageResizerUrl, {
        headers: {"x-api-key": <API_KEY>}
    }).then(resp => resp.json()).then(json => json.iguim_url));
```

For a full list of features available in Fastly IO see the API documentation [here](https://docs.fastly.com/api/imageopto/).
