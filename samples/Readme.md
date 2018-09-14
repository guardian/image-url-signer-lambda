image url signer Example
========================
This is a basic html page with a box to put a media.guim url in, 
which is then turned into a signed url, with a preview. To run it 
you need to replace the placeholder values in config-example.js and rename
it to config.js. Then open url_sign.html in a browser.

When specifying the media.guim url you should pick the master url from the grid
and include the `width=` query parameter on the end of it to set the width of 
the resulting image (you can actually use any of the [fastly io parameters](https://docs.fastly.com/api/imageopto/))

The tool will set the resulting image compression to be 85%, you can override this by 
specifying `quality=X` in the url.  