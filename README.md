# EchoDocs-AI

## Overview
This project is an AI-powered PDF Converser assistant that leverages Google's Gemini API to conduct technical questionaries in a conversational manner. The system reads pdf information to generate professional conversions.

## Features
- Read pdf and ask qestions from that.
- Generates system prompts based on text provided.
- Conducts real-time AI-driven technical interviews.
- Supports audio input handling.
- Uses WebSockets for real-time communication between the client and Gemini API.
- Implements structured AI interaction with proper handling with PDF

## Technologies Used
- Python
- WebSockets
- Google Gemini API
- AsyncIO
- JSON
- MarkitDown

## Installation
### Prerequisites
- Python 3.8+
- Google API Key

### Steps
1. Create virtual env:
   ```sh
   python3 -m venv venv
   .\venv\bin\activate
   ```
2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up your API Key:
   ```sh
   GOOGLE_API_KEY='your-api-key-here'
   ```
4. Ensure the required directories and files exist:
   ```sh
|   PDF_details/
│   ├── 529 Plans- Questions and answers  Internal Revenue Service.pdf
│   ├── 2503.13650v1.pdf
   ```
   Populate these files with relevant PDF details.

## Usage
1. Start the WebSocket server:
   ```sh
   python app.py
   ```
2. Install `Live Server` extension by `Ritwick Dey`, repload the VS-code.
3. Go to static/index.html and press `Open with Live Server`
4. The server will be running on `ws://localhost:9084`.
5. A WebSocket client can connect to this endpoint to conduct AI-driven interviews.

## File Structure
```sh
EchoDocs-AI/
├── PDF_details/
│   ├── 529 Plans- Questions and answers  Internal Revenue Service.pdf
│   ├── 2503.13650v1.pdf
├── app.py
├── static/
│   ├── index.html
│   ├── pcm-processor.js
├── README.md
```

## WebSocket API
### WebSocket Connection
- Connect to the WebSocket server at `ws://localhost:9084`.
- Send interview configuration as a JSON message.
- Receive AI-generated interview responses in real time.

## License
This project is licensed under the MIT License.

