class PCMProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this.buffer = new Float32Array();

        // Correct way to handle messages in AudioWorklet
        this.port.onmessage = (e) => {
            const newData = e.data;
            const newBuffer = new Float32Array(this.buffer.length + newData.length);
            newBuffer.set(this.buffer);
            newBuffer.set(newData, this.buffer.length);
            this.buffer = newBuffer;
        };
    }

    process(inputs, outputs, parameters) {
        const output = outputs[0];
        const channelData = output[0];

        if (this.buffer.length >= channelData.length) {
            channelData.set(this.buffer.slice(0, channelData.length));
            this.buffer = this.buffer.slice(channelData.length);
            return true;
        }

        return true;
    }
}

registerProcessor('pcm-processor', PCMProcessor);




// class PCMProcessor extends AudioWorkletProcessor {
//     constructor() {
//         super();
//         this.buffer = new Float32Array(1024); // Pre-allocate a buffer with reasonable size
//         this.bufferLength = 0;

//         this.port.onmessage = (event) => {
//             const newData = event.data;
//             const totalLength = this.bufferLength + newData.length;

//             if (totalLength > this.buffer.length) {
//                 // Expand buffer size if needed
//                 let newBuffer = new Float32Array(totalLength * 2);
//                 newBuffer.set(this.buffer.subarray(0, this.bufferLength));
//                 this.buffer = newBuffer;
//             }

//             // Append new data to the buffer
//             this.buffer.set(newData, this.bufferLength);
//             this.bufferLength = totalLength;
//         };
//     }

//     process(inputs, outputs, parameters) {
//         const output = outputs[0];
//         if (!output || output.length === 0 || this.bufferLength === 0) {
//             return true; // No output channels available or buffer empty
//         }

//         const channelData = output[0];
//         const chunkSize = Math.min(channelData.length, this.bufferLength);

//         channelData.set(this.buffer.subarray(0, chunkSize));

//         // Shift buffer to remove processed samples
//         this.buffer.copyWithin(0, chunkSize, this.bufferLength);
//         this.bufferLength -= chunkSize;

//         return true;
//     }
// }

// registerProcessor('pcm-processor', PCMProcessor);
