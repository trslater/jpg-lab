// 8x8 RGB pixel blocks take 192 bytes; base64 encoding is 4:3
const block_size = 256

const fileInput = document.getElementById("image-file")

fileInput.onchange = async event => {
    const formData = new FormData()
    formData.append("upload", event.target.files[0])

    const response = await fetch("http://localhost:8888/upload", {
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
            console.log(remaining.slice(0, block_size))
            remaining = remaining.slice(block_size)
        }
    }
}
