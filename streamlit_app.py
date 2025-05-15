import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("💬 Chatbot")
# Configure the Gemini API key
GOOGLE_API_KEY ="AIzaSyABEoJi0SpQrt7iVXKMnyklgnGWXx31sew"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize session state variables
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'knowledge_assessment_done' not in st.session_state:
    st.session_state.knowledge_assessment_done = False

def get_gemini_response(prompt, conversation_history=None):
    """Sends a prompt to the Gemini API and returns the generated response."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        if conversation_history is None:
            chat = model.start_chat(history=[])
        else:
            chat = model.start_chat(history=conversation_history)
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "I'm having trouble connecting to the AI service. Please try again later."

def assess_user_knowledge():
    """Asks the user basic questions to gauge their knowledge."""
    # This is now just a prompt, the actual assessment happens in the main UI
    return st.radio("Have you used an auto-level before?", ('Yes', 'No'))

def get_response(user_input, has_used_before):
    """Generates a response based on the user input."""
    user_input = user_input.lower()

    #Construct a prompt for Gemini - Use has_used_before info

    if has_used_before == "yes":
        prompt = f"You are a helpful chatbot assisting someone experienced with auto-levels.  Answer the following question concisely:\n\n{user_input}"
    else:
        prompt = f"You are a helpful chatbot assisting someone new to auto-levels.  Answer the following question in a clear, simple way:\n\n{user_input}"
    gpt_response = get_gemini_response(prompt, st.session_state.conversation_history)
    return gpt_response

# Streamlit UI
st.title("Explore Auto-Level")

# Display conversation history in a chat-like format
for chat in st.session_state.conversation_history:
    if chat["role"] == "user":
        with st.chat_message("user"):
            st.markdown(chat["parts"][0])
    else:
        with st.chat_message("assistant"):  # Use "assistant" for chatbot
            st.markdown(chat["parts"][0])

#Assess knowledge only once - before chat
if not st.session_state.knowledge_assessment_done:
   with st.sidebar:
        st.session_state.has_used_before = assess_user_knowledge()
        st.session_state.knowledge_assessment_done = True  #Mark it as done
else:
    #Retrieve from session state
    has_used_before = st.session_state.has_used_before

# Chat input
prompt = st.chat_input("Say something")  # Dedicated chat input

if prompt:
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.conversation_history.append({"role": "user", "parts": [prompt]})

    # Get and display assistant message
    response = get_response(prompt, has_used_before) #Pass has_used_before
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.conversation_history.append({"role": "model", "parts": [response]})
