import streamlit as st
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are a friendly and knowledgeable AI assistant for Dollywood theme park. Your role is to provide information about attractions, dining options, shows, and help visitors plan their visit to Dollywood. You should be able to answer questions about ride wait times, restaurant menus, show schedules, and provide recommendations based on visitor preferences.

Here are some key points to remember:
1. Dollywood is located in Pigeon Forge, Tennessee.
2. The park offers a variety of rides, shows, restaurants, and attractions.
3. You should be familiar with popular attractions like Thunderhead, Wild Eagle, and Lightning Rod.
4. Be aware of different dining options, including Aunt Granny's Restaurant and Dogs N Taters.
5. Know about shows like "Dreamland Drive-In" and "Wings of America".
6. Be prepared to provide information on operating hours, ticket prices, and special events.

Always maintain a friendly and helpful tone, and if you're unsure about specific current information, recommend that the visitor check the official Dollywood website or speak with a park representative for the most up-to-date details.
"""

class DollywoodChatBot:
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    def generate_response(self, messages):
        response = self.anthropic.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=messages
        )
        return response.content[0].text

    def process_user_input(self, user_input, conversation_history):
        conversation_history.append({"role": "user", "content": user_input})
        response = self.generate_response(conversation_history)
        conversation_history.append({"role": "assistant", "content": response})
        return response


def main():
    st.title("Dollywood Assistant")

    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = [
            {"role": "user", "content": SYSTEM_PROMPT},
        ]

    chatbot = DollywoodChatBot()

    # Display conversation history
    for message in st.session_state.conversation_history[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Add example questions in the sidebar
    st.sidebar.header("Example Questions")
    example_questions = [
        "What are the operating hours for Dollywood?",
        "Can you tell me about the Thunderhead roller coaster?",
        "What's the wait time for Wild Eagle?",
        "What dining options are available near Timber Canyon?",
        "What's the show schedule for Dreamland Drive-In?",
        "Are there any special events happening this month?",
    ]

    # Use selectbox for example questions
    selected_question = st.sidebar.selectbox(
        "Select a question or type your own:",
        ["Type your own"] + example_questions,
        key="question_select"
    )

    # Initialize user_input
    user_input = None

    # Handle input based on selection
    if selected_question == "Type your own":
        user_input = st.chat_input("Type your message here...", key="custom_input")
    elif st.sidebar.button("Ask selected question", key="ask_button"):
        user_input = selected_question

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response = chatbot.process_user_input(user_input, st.session_state.conversation_history)
            st.markdown(response)

if __name__ == "__main__":
    main()