import os
import gradio as gr
from fastapi import FastAPI
from calendar_service import CalendarService
from agent import CalendarAgent

# Initialize Calendar Service & Agent
calendar_service = CalendarService()
agent = CalendarAgent(calendar_service=calendar_service)


def chat_response(user_message, history):
    """
    Handler for Gradio Chatbot interaction.
    """
    if not user_message or not user_message.strip():
        return "", history

    # Convert history to tuples if using Gradio Chatbot history format
    formatted_history = []
    if history:
        for item in history:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                formatted_history.append((item[0], item[1]))

    # Process message with Calendar Agent
    bot_reply = agent.process_request(user_message, formatted_history)

    # Append to history
    updated_history = history + [(user_message, bot_reply)]
    return "", updated_history


def create_gradio_ui():
    """Build minimalist Gradio Chat Interface matching project specifications."""
    custom_css = """
    #title-container { text-align: center; margin-bottom: 20px; }
    #chatbot-box { min-height: 380px; }
    """
    
    with gr.Blocks(title="Automated Calendar Scheduling Assistant", css=custom_css) as demo:
        gr.Markdown(
            """
            # Automated Calendar Scheduling Assistant
            ### Manage your calendar using natural language.
            """,
            elem_id="title-container"
        )

        chatbot = gr.Chatbot(
            value=[(None, "Hello! How can I help you with your calendar today?")],
            elem_id="chatbot-box",
            show_label=False
        )

        with gr.Row():
            txt_input = gr.Textbox(
                show_label=False,
                placeholder="Type your request... (e.g. Schedule a meeting tomorrow at 3 PM)",
                container=False,
                scale=8
            )
            submit_btn = gr.Button("Send", variant="primary", scale=1)
            clear_btn = gr.Button("Clear", variant="secondary", scale=1)

        gr.Markdown("### Examples:")
        gr.Examples(
            examples=[
                "Schedule a meeting tomorrow at 3 PM.",
                "What meetings do I have today?",
                "Find a free slot tomorrow.",
                "Schedule a 30-minute meeting at 5 PM."
            ],
            inputs=txt_input
        )

        # Wire events
        txt_input.submit(
            fn=chat_response,
            inputs=[txt_input, chatbot],
            outputs=[txt_input, chatbot]
        )
        submit_btn.click(
            fn=chat_response,
            inputs=[txt_input, chatbot],
            outputs=[txt_input, chatbot]
        )
        clear_btn.click(
            fn=lambda: [(None, "Hello! How can I help you with your calendar today?")],
            inputs=None,
            outputs=chatbot
        )

    return demo


# Create Gradio demo instance
demo = create_gradio_ui()

# Fast API application for WSGI/ASGI mounting
app = FastAPI()

# Mount Gradio application to root path '/'
app = gr.mount_gradio_app(app, demo, path="/")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    print(f"Starting Automated Calendar Scheduling Assistant on http://0.0.0.0:{port}")
    uvicorn.run("app:app", host="0.0.0.0", port=port)
