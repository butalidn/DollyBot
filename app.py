import streamlit as st
from dollybot import ChatBot
from config import SYSTEM_PROMPT
import base64

def main():
    st.set_page_config(page_title="DollyBot - Dollywood AI Assistant", page_icon="🎡")

    st.title("Welcome to Dollywood! 🎢")

    st.markdown("""
    ### Hello! I'm DollyBot, your personal AI Assistant at Dollywood!

    I'm here to make your visit as fun and smooth as possible. Ask me about:
    
    - 🎢 Exciting rides and attractions
    - 🍽️ Delicious dining options and menus
    - 🎭 Entertaining shows and their schedules
    - 🎟️ Park hours and ticket information
    - 📍 Navigation around the park
    - And much more!

    How can I help make your Dollywood experience amazing today?
    """)


    if "messages" not in st.session_state:
        map_image_path = '/mnt/c/Users/nzbutalid/Documents/School/MSAI_5513/dollywood_map.png'
        map_data = None
        with open(map_image_path, "rb") as map_file:
            map_data = base64.b64encode(map_file.read()).decode('utf-8')

        st.session_state.messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": map_data
                        }
                    },
                    {
                        "type": "text",
                        "text": """
                            This is a map of Dollywood. Please first refer to this in order to direct visitors to certain locations or to aid in navigation.
                            Please do not mention this map to the visitor going forward. This should be a part of your base knowledge. And please do not use the
                            numbers in the map to refer to locations.
                        """
                    }
                ]
            },
            {'role': "user", "content": SYSTEM_PROMPT},
        ]

    chatbot = ChatBot(st.session_state)

    # Display user and assistant messages skipping the first two
    for message in st.session_state.messages[2:]:
         # ignore tool use blocks
         if isinstance(message["content"], str):
              with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    if user_msg := st.chat_input("Type your message here..."):
         st.chat_message("user").markdown(user_msg)

         with st.chat_message("assistant"):
            with st.spinner("DollyBot is thinking..."):
                response_placeholder = st.empty()
                full_response = chatbot.process_user_input(user_msg)
                response_placeholder.markdown(full_response)

if __name__ == "__main__":
    main()
