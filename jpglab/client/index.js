const apiURL = "localhost:8888"

const fileInput = document.getElementById("image-file")
const fullImage = document.getElementById("full-image")
const closeUp = document.getElementById("close-up")
const webSocket = new WebSocket(`ws://${apiURL}/block`)

webSocket.binaryType = "arraybuffer";

var canvas = document.getElementById("full-image");
var context = canvas.getContext("2d");

webSocket.onmessage = event => {
    const typedData = new Uint8ClampedArray(event.data)
    // 2 byte ID (~65k blocks, i.e., ~250x250 block image)
    const blockNumber = typedData[0]*256 + typedData[1]
    const rgb = typedData.slice(2)
    let rgba = new Uint8ClampedArray(256)
    
    // Convert from RGB to RGBA
    for (let i = 0, j = 0; i < 256; ++i, ++j) {
        rgba[j] = rgb[i]
        if ((i + 1)%3 == 0) rgba[++j] = 255
    }

    const x = 8*(blockNumber%32)
    const y = 8*Math.floor(blockNumber/32)

    context.putImageData(new ImageData(rgba, 8), x, y)
}

fileInput.onchange = async event => {
    const formData = new FormData()
    formData.append("upload", event.target.files[0])

    const response = await fetch(`http://${apiURL}/upload`, {
        method: "POST",
        body: formData
    })
    
    const reader = response.body.getReader()

    while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        // Sometimes multiple chunks are read at once, so we break them up
        // I think this happens when the server delivers them faster than the
        // client can read them
        let remaining = value
        while (remaining.length > 0) {
            const block = remaining.slice(0, 2 + 192)
            remaining = remaining.slice(2 + 192)
            webSocket.send(block)
        }
    }
}
