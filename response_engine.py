# response_engine.py - Groq API (Fast, Reliable, Free)
import requests
import os
import time

MODEL_NAME = "llama-3.3-70b-versatile"
class ResponseEngine:
    """
    Response engine using Groq API with Llama 3.
    Fast, reliable, and free tier is generous.
    """
    
    def __init__(self):
        """Initialize Groq API connection."""
        
        # Load Groq API key from environment
        self.api_key = os.getenv("GROQ_API_KEY", "")
        
        if not self.api_key:
            print("⚠️ WARNING: No GROQ_API_KEY found!")
            raise ValueError("GROQ_API_KEY required in .env file")
        
        # Groq API endpoint
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Use Llama 3.1 70B - it's fast and smart
        self.model = MODEL_NAME
        
        # System prompt - defines the AI's role and knowledge
        self.system_prompt = """You are the BSU Graduate Advisor AI Assistant for Computer Science students at Boise State University.

Your knowledge includes:

BSU CS Faculty:
- Dr. Jun Zhuang: Artificial Intelligence, Machine Learning, Human-Centered Computing (Available Spring 2026)
- Dr. Gaby Dagher: Cybersecurity, Privacy, Blockchain Technology (Available Fall 2025)
- Dr. Jerry Alan Fails: Human-Computer Interaction, CS Education, Child-Computer Interaction (Available Now)
- Dr. Elisa Barney Smith: Computer Vision, Pattern Recognition (Available Spring 2026)
- Dr. Hoda Mehrpouyan: AI Ethics, Sustainability, Systems Engineering (Not taking students currently)

Important Guidelines:
- Students must find a permanent advisor by the end of their 2nd semester
- Students should attend faculty research talks and office hours
- International students often face challenges in the advisor selection process
- Consider research interests alignment when choosing an advisor

Your role:
- Help students find suitable research advisors based on their interests
- Provide information about faculty research areas and availability
- Guide students through the advisor selection process
- Answer questions about BSU CS graduate programs
- Be friendly, conversational, and proactive in asking follow-up questions

Keep responses concise (2-4 sentences) but helpful. Always try to guide the conversation toward helping them find the right advisor."""
        
        print(f"✅ Groq API initialized with {self.model}")
    
    def generate_answer(self, user_query, history=None):
        """
        Generate intelligent response using Groq API.
        
        Args:
            user_query: Current user question
            history: Previous conversation messages
            
        Returns:
            Generated response string
        """
        
        # Build messages array for the API
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add conversation history (keep last 6 messages for context)
        if history:
            for msg in history[-6:]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Add current user query
        messages.append({
            "role": "user",
            "content": user_query
        })
        
        # Call Groq API
        answer = self._query_groq(messages)
        return answer
    
    def _query_groq(self, messages, max_retries=3):
        """Query Groq API with retry logic."""
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 300,
            "top_p": 0.9
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result["choices"][0]["message"]["content"].strip()
                    return answer
                
                elif response.status_code == 401:
                    return "❌ Authentication error. Check your GROQ_API_KEY in the .env file."
                
                elif response.status_code == 429:
                    print(f"⏳ Rate limit, waiting... (attempt {attempt + 1})")
                    time.sleep(2)
                    continue
                
                else:
                    print(f"API Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"Error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
        
        return "I'm having trouble connecting right now. Please try again in a moment."
# # response_engine.py
# # This file handles generating intelligent responses for the chatbot
# # It uses Mistral-7B AI model through HuggingFace's free API

# import requests  # To make HTTP requests to the HuggingFace API
# import os        # To read environment variables (like our API token)
# import time      # To add delays when retrying failed requests

# class ResponseEngine:
#     """
#     This class is responsible for generating AI responses.
    
#     How it works:
#     1. Takes a user's question
#     2. Sends it to Mistral-7B AI model via HuggingFace API
#     3. Gets back an intelligent response
#     4. Returns it to the chatbot
    
#     Later (Phase 2): We'll add RAG here to retrieve professor data first,
#     then pass that data to Mistral to generate accurate responses.
#     """
    
#     def __init__(self):
#         """
#         Initialize the response engine when the chatbot starts.
#         This runs once when you first load the app.
#         """
        
#         # STEP 1: Load the API token from environment variable
#         # This token lets us use HuggingFace's API for free
#         # It comes from the .env file you created
#         self.api_token = os.getenv("HUGGINGFACE_API_TOKEN", "")
        
#         # STEP 2: Check if token was loaded successfully
#         if not self.api_token:
#             print("⚠️ WARNING: No HUGGINGFACE_API_TOKEN found!")
#             print("Make sure you created .env file with your token")
        
#         # STEP 3: Set up the API endpoint
#         # This is the URL where we send requests to talk to Mistral-7B
#         # HuggingFace hosts the model for free, we just call their API
#         # Use HuggingFaceH4/zephyr-7b-beta - it's more reliable and free
#         # Use meta-llama model - it's free and stable
#         self.api_url = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"



        
#         # STEP 4: Set up authentication headers
#         # Every request needs to include our token to prove we're allowed to use the API
#         self.headers = {"Authorization": f"Bearer {self.api_token}"}
        
#         # STEP 5: Define the AI's "personality" and knowledge
#         # This tells Mistral how to behave and what it knows
#         # Think of this as the AI's instruction manual
#         self.system_context = """You are the BSU Graduate Advisor AI Assistant for Computer Science students at Boise State University.

# Your knowledge includes:

# BSU CS Faculty:
# - Dr. Jun Zhuang: Artificial Intelligence, Machine Learning, Human-Centered Computing (Available Spring 2026)
# - Dr. Gaby Dagher: Cybersecurity, Privacy, Blockchain Technology (Available Fall 2025)
# - Dr. Jerry Alan Fails: Human-Computer Interaction, CS Education, Child-Computer Interaction (Available Now)
# - Dr. Elisa Barney Smith: Computer Vision, Pattern Recognition (Available Spring 2026)
# - Dr. Hoda Mehrpouyan: AI Ethics, Sustainability, Systems Engineering (Not taking students currently)

# Important Guidelines:
# - Students must find a permanent advisor by the end of their 2nd semester
# - Students should attend faculty research talks and office hours
# - International students often face challenges in the advisor selection process
# - Consider research interests alignment when choosing an advisor

# Your role:
# - Help students find suitable research advisors based on their interests
# - Provide information about faculty research areas and availability
# - Guide students through the advisor selection process
# - Answer questions about BSU CS graduate programs
# - Be friendly, conversational, and proactive in asking follow-up questions

# Keep responses concise (2-4 sentences) but helpful. Always try to guide the conversation toward helping them find the right advisor."""

#         # NOTE: In Phase 2 (RAG), we'll replace this hardcoded knowledge
#         # with data retrieved from your professor database in real-time

#     def generate_answer(self, user_query, history=None):
#         """
#         Main method to generate a response to the user's question.
        
#         This is called every time the user sends a message.
        
#         Parameters:
#         - user_query: The question the user just asked (string)
#         - history: Previous conversation messages (list of dicts)
#                    Format: [{"role": "user", "content": "question"}, 
#                            {"role": "assistant", "content": "answer"}, ...]
        
#         Returns:
#         - answer: The AI's response (string)
#         """
        
#         # STEP 1: Build conversation context from history
#         # This helps the AI remember what was discussed before
#         # Example: If user asked "Who does AI?" and then "Tell me more"
#         #          the AI needs to remember they're asking about AI professors
        
#         conversation_context = ""  # Start with empty context
        
#         if history:  # If there are previous messages
#             # Only keep the last 4 messages (2 back-and-forth exchanges)
#             # Why? Too much history makes the prompt too long and expensive
#             recent_history = history[-4:]
            
#             # Format each message for the AI to understand
#             for msg in recent_history:
#                 # Label who said what: Student or Advisor
#                 role = "Student" if msg["role"] == "user" else "Advisor"
#                 # Add to context: "Student: Hi there\nAdvisor: Hello!..."
#                 conversation_context += f"{role}: {msg['content']}\n"
        
#         # STEP 2: Build the prompt for Mistral
#         # Mistral uses a specific format: <s>[INST] instruction [/INST]
#         # This tells Mistral: "You are an advisor, here's the context, now respond"
        
#         prompt = f"""<s>[INST] {self.system_context}

# Previous conversation:
# {conversation_context}

# Current student question: {user_query}

# Respond as the BSU Graduate Advisor AI. Be conversational, helpful, and guide them toward finding the right advisor. [/INST]"""

#         # NOTE: The [INST] and [/INST] tags are Mistral's special format
#         # They tell the model where the instruction starts and ends
        
#         # STEP 3: Send the prompt to the API and get response
#         answer = self._query_api(prompt)
        
#         # STEP 4: Return the answer to the chatbot
#         return answer
    
#     def _query_api(self, prompt, max_retries=3):
#         """
#         Send the prompt to HuggingFace API and get the AI's response.
        
#         This is a private method (note the underscore _) that handles
#         all the technical stuff of talking to the API.
        
#         Parameters:
#         - prompt: The full prompt we constructed (string)
#         - max_retries: How many times to retry if it fails (default: 3)
        
#         Returns:
#         - answer: The AI's generated response (string)
#         """
        
#         # STEP 1: Prepare the request payload
#         # This tells the API what we want and how to generate it
#         payload = {
#             "inputs": prompt,  # The prompt we built above
#             "parameters": {
#                 # These control how the AI generates text:
#                 "max_new_tokens": 300,  # Maximum length of response (in tokens ~= words)
#                 "temperature": 0.7,      # Creativity (0=boring, 1=creative, 0.7=balanced)
#                 "top_p": 0.9,           # Diversity of word choices (0.9 is good balance)
#                 "repetition_penalty": 1.1,  # Prevents repeating same words (1.1 = slight penalty)
#                 "return_full_text": False   # Only return new text, not the whole prompt back
#             }
#         }
        
#         # STEP 2: Try to send the request (with retries in case of failure)
#         for attempt in range(max_retries):  # Try up to 3 times
#             try:
#                 # Send POST request to HuggingFace API
#                 response = requests.post(
#                     self.api_url,      # Where to send (Mistral endpoint)
#                     headers=self.headers,  # Authentication (our token)
#                     json=payload,      # The prompt and parameters
#                     timeout=30         # Wait max 30 seconds for response
#                 )
                
#                 # STEP 3: Check if request was successful
#                 if response.status_code == 200:  # 200 = Success!
#                     # Parse the JSON response from the API
#                     result = response.json()
                    
#                     # Extract the generated text from the response
#                     # API returns format: [{"generated_text": "the answer"}]
#                     if isinstance(result, list) and len(result) > 0:
#                         answer = result[0].get("generated_text", "").strip()
                        
#                         # Clean up any formatting issues
#                         answer = self._clean_response(answer)
#                         return answer
#                     else:
#                         # Unexpected format - print for debugging
#                         print(f"Unexpected API response format: {result}")
                
#                 # STEP 4: Handle specific error codes
#                 elif response.status_code == 503:  # 503 = Service Unavailable
#                     # This happens when model is "cold" (not loaded yet)
#                     # First time using the API takes ~20-30 seconds to load model
#                     print(f"⏳ Model loading... (attempt {attempt + 1}/{max_retries})")
#                     time.sleep(5)  # Wait 5 seconds before retrying
#                     continue  # Try again
                
#                 elif response.status_code == 401:  # 401 = Authentication Failed
#                     # Your API token is wrong or expired
#                     return "❌ Authentication error. Please check your HUGGINGFACE_API_TOKEN in the .env file."
                
#                 else:
#                     # Some other error - print it for debugging
#                     print(f"API Error {response.status_code}: {response.text}")
            
#             # STEP 5: Handle network errors
#             except requests.exceptions.Timeout:
#                 # Request took too long (> 30 seconds)
#                 print(f"⏱️ Request timeout (attempt {attempt + 1}/{max_retries})")
#                 if attempt < max_retries - 1:  # If not last attempt
#                     time.sleep(2)  # Wait 2 seconds
#                     continue  # Try again
            
#             except Exception as e:
#                 # Some other error occurred
#                 print(f"Error querying API: {e}")
#                 if attempt < max_retries - 1:  # If not last attempt
#                     time.sleep(2)  # Wait 2 seconds
#                     continue  # Try again
        
#         # STEP 6: If all retries failed, return a fallback message
#         return ("I'm having trouble connecting to the AI service right now. "
#                 "This might be because the model is loading (first-time use takes ~30 seconds). "
#                 "Please try your question again in a moment.")
    
#     def _clean_response(self, text):
#         """
#         Clean up the AI's response by removing formatting artifacts.
        
#         Sometimes the AI includes instruction tags in its response.
#         This function removes them to make the response look clean.
        
#         Parameters:
#         - text: Raw response from the API (string)
        
#         Returns:
#         - text: Cleaned response (string)
#         """
        
#         # Remove instruction tags that sometimes appear in responses
#         if "[/INST]" in text:
#             # Split on the tag and take everything after it
#             text = text.split("[/INST]")[-1]
        
#         if "<s>" in text:
#             # Remove special start token
#             text = text.replace("<s>", "")
        
#         if "</s>" in text:
#             # Remove everything after the end token
#             text = text.split("</s>")[0]
        
#         # Remove extra whitespace and return
#         return text.strip()
    # # response_engine.py
# from transformers import pipeline

# class ResponseEngine:
#     def __init__(self):
#         # Try a larger or more conversational model if possible
#         # Options (ranked by fluency):
#         # 1. mistralai/Mistral-7B-Instruct-v0.2  (GPU needed)
#         # 2. google/flan-t5-large
#         # 3. google/flan-t5-base  (default light version)
#         try:
#             self.generator = pipeline(
#                 "text2text-generation",
#                 model="google/flan-t5-large"
#             )
#         except Exception:
#             self.generator = pipeline("text2text-generation", model="google/flan-t5-base")

#         # Core persona prompt: defines how the assistant behaves
#         self.system_prompt = (
#             "You are BSU's Graduate Advisor AI Assistant.\n"
#             "You are friendly, professional, and helpful.\n"
#             "You can respond to any kind of question, "
#             "but always try to relate your responses to BSU research, graduate life, "
#             "faculty, or advisor guidance when appropriate.\n"
#             "Be conversational and concise, like a real person helping a student.\n"
#         )

#     def generate_answer(self, user_query, history=None):
#         """
#         Generates a conversational, context-aware answer.
#         history: list of {'role': 'user'/'assistant', 'content': str}
#         """

#         # Build conversation memory from recent messages
#         context = ""
#         if history:
#             last_turns = history[-3:]  # last 3 exchanges for context
#             formatted = []
#             for msg in last_turns:
#                 role = "Student" if msg["role"] == "user" else "Advisor"
#                 formatted.append(f"{role}: {msg['content']}")
#             context = "\n".join(formatted)

#         # Construct final prompt
#         prompt = (
#             f"{self.system_prompt}\n"
#             f"{context}\n"
#             f"Student: {user_query}\n"
#             f"Advisor:"
#         )

#         # Generate text with tuned parameters for more natural responses
#         try:
#             result = self.generator(
#                 prompt,
#                 max_new_tokens=200,
#                 do_sample=True,
#                 temperature=0.9,
#                 top_p=0.9,
#                 repetition_penalty=1.05
#             )
#             answer = result[0]["generated_text"].strip()
#         except Exception as e:
#             answer = (
#                 "I'm sorry, something went wrong while generating a response. "
#                 "Could you please repeat or rephrase your question?"
#             )
#         return answer
