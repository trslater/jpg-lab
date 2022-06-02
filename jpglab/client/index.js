// 8x8 RGB pixel blocks take 192 bytes; base64 encoding is 4:3
const block_size = 256
const apiURL = "http://localhost:8888"

const fileInput = document.getElementById("image-file")
const fullImage = document.getElementById("full-image")
const closeUp = document.getElementById("close-up")

fileInput.onchange = async event => {
    const formData = new FormData()
    formData.append("upload", event.target.files[0])

    const response = await fetch(`${apiURL}/upload`, {
        method: "POST",
        body: formData
    })
    
    const reader = response.body
        .pipeThrough(new TextDecoderStream())   // Turns bytes into strings
        .getReader()

    while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        // Sometimes multiple chunks are read at once, so we break them up
        // I think this happens when the server delivers them faster than the
        // client can read them
        let remaining = value
        while (remaining.length > 0) {
            const image = document.createElement("img")
            const block = remaining.slice(0, block_size)
            image.src = `${apiURL}/block.png?s=${encodeURIComponent(block)}`
            image.onmouseover = event => {
                closeUp.src = event.target.src
            }
            fullImage.append(image)

            remaining = remaining.slice(block_size)
        }
    }
}
