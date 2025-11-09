# chatbot_demo.py
# This is the main file that creates the chatbot user interface
# It uses Streamlit to create a web-based chat interface

import streamlit as st
from response_engine import ResponseEngine
import os

# ===== MANUALLY LOAD .ENV FILE =====
# For some reason python-dotenv doesn't work automatically in Streamlit on Windows
# So we load it explicitly here
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load the .env file
    print(f"✅ Token loaded: {os.getenv('HUGGINGFACE_API_TOKEN', 'NOT FOUND')[:20]}...")  # Debug print (only show first 20 chars for security)
except ImportError:
    print("python-dotenv not installed. Trying to read .env manually...")
    # Manual fallback: read .env file directly
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
        print(f"✅ Token loaded manually: {os.getenv('HUGGINGFACE_API_TOKEN', 'NOT FOUND')[:20]}...")
    except Exception as e:
        print(f"Could not load .env file: {e}")
# ==================== PAGE CONFIGURATION ====================
# This sets up how the webpage looks and behaves

st.set_page_config(
    page_title="BSU Advisor AI",  # Title shown in browser tab
    layout="centered",  # Content is centered on page (not full width)
    page_icon="bsu_logo.png",  # Icon in browser tab
    initial_sidebar_state="expanded"  # Sidebar is open when page loads
)

# ==================== CUSTOM STYLING ====================
# This adds custom CSS to make the chat look better

st.markdown("""
    <style>
    /* Style for chat message bubbles */
    .stChatMessage {
        padding: 1rem;  /* Space inside messages */
        border-radius: 0.5rem;  /* Rounded corners */
    }
    /* Style for main content area */
    .main {
        padding: 2rem;  /* Space around content */
    }
    </style>
""", unsafe_allow_html=True)  # Allow HTML/CSS in markdown

# # ==================== HEADER ====================
# # The main title at the top of the page

# st.title("🎓 BSU Graduate Advisor AI")
# st.caption("Your intelligent assistant for BSU CS graduate advising")

# ==================== HEADER ====================
# Logo and title at the top of the page

# Create columns for logo + title layout
col1, col2 = st.columns([1, 7])

with col1:
    # BSU Logo (replace "bsu_logo.png" with your logo filename)
    st.image("bsu_logo.png", width=80)

with col2:
    st.title("BSU Graduate Advisor AI")
    st.caption("Your intelligent assistant for BSU CS graduate advising")

# ==================== SIDEBAR ====================
# The sidebar contains information about the project

with st.sidebar:
    # Section 1: About current demo
    st.header("About This Demo")
    st.markdown("""
    **Current Phase: Smart Conversational Interface**
    
    This demo showcases:
    - Natural Language Processing
    - Context-aware conversations
    - Advising-focused dialogue
    
    **Try asking:**
    - "Hello, how are you?"
    - "Who does AI research?"
    - "Which professors are available?"
    - "Tell me about Dr. Jun Zhuang"
    - "How do I choose an advisor?"
    """)
    
    st.divider()  # Horizontal line separator
    
    # Section 2: Future plans
    st.header("Coming Next")
    st.markdown("""
    **Phase 2: RAG Integration**
    - Retrieval-Augmented Generation
    - SentenceTransformers embeddings
    - FAISS vector database
    - Real-time professor data retrieval
    """)
    
    st.divider()  # Another horizontal line
    
    # Section 3: Project info
    st.markdown("**Built for BSU CS Graduate Students**")
    st.caption("CS557 - Natural Language Processing Project")

# ==================== API TOKEN CHECK ====================
# Make sure the HuggingFace API token is loaded before continuing

if not os.getenv("HUGGINGFACE_API_TOKEN"):
    # If token is missing, show error and stop
    st.error("HUGGINGFACE_API_TOKEN not found!")
    st.info("Please create a .env file with your HuggingFace API token")
    st.stop()  # Stop the app here - don't continue without token

# ==================== SESSION STATE INITIALIZATION ====================
# Session state keeps data persistent across page reloads
# Think of it as the chatbot's "memory"

# Initialize message history
if "messages" not in st.session_state:
    # If this is the first time loading the page, create empty message list
    st.session_state.messages = []
    
    # Add a welcome message from the assistant
    welcome_msg = {
        "role": "assistant",  # This message is from the AI
        "content": "Hi! I'm your BSU Graduate Advisor AI. I can help you learn about CS faculty, their research areas, availability, and guide you through the advisor selection process. What would you like to know?"
    }
    st.session_state.messages.append(welcome_msg)

# Initialize the response engine (our AI)
if "generator" not in st.session_state:
    # If this is first time, create the ResponseEngine
    with st.spinner("Initializing AI assistant..."):  # Show loading message
        st.session_state.generator = ResponseEngine()  # Create the AI engine
        #st.success("AI assistant ready!", icon="🎉")  # Show success message

# ==================== DISPLAY CHAT HISTORY ====================
# Show all previous messages in the conversation

for message in st.session_state.messages:
    # For each message in history, display it in a chat bubble
    with st.chat_message(message["role"]):  # "user" or "assistant"
        st.write(message["content"])  # The actual message text

# ==================== CHAT INPUT ====================
# This is where the user types their question

if user_query := st.chat_input("Ask me anything about graduate advising at BSU..."):
    # The := is "walrus operator" - assigns AND checks in one line
    # This runs when user presses Enter after typing
    
    # STEP 1: Display the user's message immediately
    with st.chat_message("user"):
        st.write(user_query)
    
    # STEP 2: Add user's message to history
    # This ensures the AI remembers what the user just asked
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })
    
    # STEP 3: Generate AI response
    with st.chat_message("assistant"):
        # Show "thinking" spinner while waiting for response
        with st.spinner("Thinking..."):
            # Call the response engine to generate an answer
            # Pass conversation history so AI has context
            answer = st.session_state.generator.generate_answer(
                user_query,  # The current question
                history=st.session_state.messages[:-1]  # All previous messages (not including the one we just added)
            )
        # Display the AI's response
        st.write(answer)
    
    # STEP 4: Add AI's response to history
    # This ensures future responses remember what the AI said
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# ==================== FOOTER ====================
# Bottom of page with project info

st.markdown("---")  # Horizontal line
col1, col2, col3 = st.columns(3)  # Create 3 columns for footer info

with col1:
    st.caption("Powered by Mistral-7B")
with col2:
    st.caption("Phase 1: Conversation")
with col3:
    st.caption("Phase 2: RAG (Coming Soon)")
# # chatbot_demo.py
# import streamlit as st
# from response_engine import ResponseEngine

# st.set_page_config(page_title="BSU Advisor AI Chatbot", layout="centered")
# st.title("🎓 BSU Advisor AI Chatbot")
# st.caption("Chat with BSU's Graduate Advisor AI. Ask about research, advisors, or anything!")

# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "generator" not in st.session_state:
#     st.session_state.generator = ResponseEngine()

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# if user_query := st.chat_input("Ask a question:"):
#     st.chat_message("user").write(user_query)
#     st.session_state.messages.append({"role": "user", "content": user_query})

#     answer = st.session_state.generator.generate_answer(user_query)
#     st.chat_message("assistant").write(answer)
#     st.session_state.messages.append({"role": "assistant", "content": answer})
