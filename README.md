Image Url Signer Lambda
=======================

This app has been thrown together as a way to make it easy to generated signed URLs for the guardian's image resizer service (Fastly IO). It provides a HTTP endpoint which takes a single parameter - `url` and an api key (passed as a header called `x-api-key`) and returns the signature of the passed url.

