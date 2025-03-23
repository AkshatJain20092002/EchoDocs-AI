import asyncio
import json
import os
import websockets
import base64
from google import genai
from markitdown import MarkItDown

os.environ['GOOGLE_API_KEY'] = 'your-api-key-here'
gemini_api_key = os.environ['GOOGLE_API_KEY']
MODEL = "gemini-2.0-flash-exp"

client = genai.Client(
  http_options={
    'api_version': 'v1alpha',
  }
)

class InterviewManager:
    
    def __init__(self, path="File path"):
        self.path = path
            
    def get_system_prompt(self):        
        pdf_extractor = MarkItDown()
        extracted_text = pdf_extractor.convert(self.path).text_content
  
        # return system_prompt
        return extracted_text

# Initialize interview manager
interview_manager = InterviewManager()

async def gemini_session_handler(client_websocket: websockets.WebSocketServerProtocol):
    """Handles the interaction with Gemini API within a websocket session."""
    try:
        config_message = await client_websocket.recv()
        config_data = json.loads(config_message)
        config = config_data.get("setup", {})
        
        # Modified system instruction for the interviewer
        config["system_instruction"] = interview_manager.get_system_prompt()

        # config["tools"] = [tool_query_docs]

        async with client.aio.live.connect(model=MODEL, config=config) as session:
            print("Connected to Gemini API")
            
            
            async def send_to_gemini():
                """Sends messages from the client websocket to the Gemini API."""
                try:
                    async for message in client_websocket:
                        try:
                            data = json.loads(message)
                            
                            # Handle file uploads
                            if "realtime_input" in data:
                                # Handle media chunks if present
                                if "media_chunks" in data["realtime_input"]:
                                    for chunk in data["realtime_input"]["media_chunks"]:
                                        if chunk["mime_type"] == "audio/pcm":
                                            await session.send(input={
                                                "mime_type": "audio/pcm",
                                                "data": chunk["data"]
                                            })

                                # Add to the send_to_gemini() function where you process messages
                                    if "finish_session" in data:
                                        print("Interview finished by client")
                                        # Send a final message to Gemini if needed
                                        await session.send(input={
                                            "mime_type": "text/plain",
                                            "data": "[INTERVIEW_COMPLETE]"
                                        })
                                        # Break the loop to close the connection
                                        break                
                                    
                        except Exception as e:
                            print(f"Error sending to Gemini: {e}")
                    print("Client connection closed (send)")
                except Exception as e:
                    print(f"Error sending to Gemini: {e}")
                finally:
                    print("send_to_gemini closed")

            async def receive_from_gemini():
                """Receives responses from the Gemini API and forwards them to the client."""
                try:
                    while True:
                        try:
                            print("receiving from gemini")
                            async for response in session.receive():

                                model_turn = response.server_content.model_turn
                                if model_turn:
                                    for part in model_turn.parts:
                                        if hasattr(part, 'text') and part.text is not None:
                                            await client_websocket.send(json.dumps({"text": part.text}))
                                        elif hasattr(part, 'inline_data') and part.inline_data is not None:
                                            base64_audio = base64.b64encode(part.inline_data.data).decode('utf-8')
                                            await client_websocket.send(json.dumps({
                                                "audio": base64_audio,
                                            }))
                                            print("audio received")

                                if response.server_content.turn_complete:
                                    print('\n<Turn complete>')
                        except websockets.exceptions.ConnectionClosedOK:
                            print("Client connection closed normally (receive)")
                            break  # Exit the loop if the connection is closed
                        except Exception as e:
                            print(f"Error receiving from Gemini: {e}")
                            break # exit the loop

                except Exception as e:
                    print(f"Error receiving from Gemini: {e}")
                finally:
                    print("Gemini connection closed (receive)")

            # Start send loop
            send_task = asyncio.create_task(send_to_gemini())
            # Launch receive loop as a background task
            receive_task = asyncio.create_task(receive_from_gemini())
            await asyncio.gather(send_task, receive_task)

    except Exception as e:
        print(f"Error in Gemini session: {e}")
    finally:
        print("Gemini session closed.")

async def main() -> None:
    async with websockets.serve(gemini_session_handler, "localhost", 9084):
        print("Running websocket server localhost:9084...")
        await asyncio.Future()  # Keep the server running indefinitely

if __name__ == "__main__":
    asyncio.run(main())
