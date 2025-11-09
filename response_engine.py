# response_engine.py
from transformers import pipeline

class ResponseEngine:
    def __init__(self):
        # Try a larger or more conversational model if possible
        # Options (ranked by fluency):
        # 1. mistralai/Mistral-7B-Instruct-v0.2  (GPU needed)
        # 2. google/flan-t5-large
        # 3. google/flan-t5-base  (default light version)
        try:
            self.generator = pipeline(
                "text2text-generation",
                model="google/flan-t5-large"
            )
        except Exception:
            self.generator = pipeline("text2text-generation", model="google/flan-t5-base")

        # Core persona prompt: defines how the assistant behaves
        self.system_prompt = (
            "You are BSU's Graduate Advisor AI Assistant.\n"
            "You are friendly, professional, and helpful.\n"
            "You can respond to any kind of question, "
            "but always try to relate your responses to BSU research, graduate life, "
            "faculty, or advisor guidance when appropriate.\n"
            "Be conversational and concise, like a real person helping a student.\n"
        )

    def generate_answer(self, user_query, history=None):
        """
        Generates a conversational, context-aware answer.
        history: list of {'role': 'user'/'assistant', 'content': str}
        """

        # Build conversation memory from recent messages
        context = ""
        if history:
            last_turns = history[-3:]  # last 3 exchanges for context
            formatted = []
            for msg in last_turns:
                role = "Student" if msg["role"] == "user" else "Advisor"
                formatted.append(f"{role}: {msg['content']}")
            context = "\n".join(formatted)

        # Construct final prompt
        prompt = (
            f"{self.system_prompt}\n"
            f"{context}\n"
            f"Student: {user_query}\n"
            f"Advisor:"
        )

        # Generate text with tuned parameters for more natural responses
        try:
            result = self.generator(
                prompt,
                max_new_tokens=200,
                do_sample=True,
                temperature=0.9,
                top_p=0.9,
                repetition_penalty=1.05
            )
            answer = result[0]["generated_text"].strip()
        except Exception as e:
            answer = (
                "I'm sorry, something went wrong while generating a response. "
                "Could you please repeat or rephrase your question?"
            )
        return answer
