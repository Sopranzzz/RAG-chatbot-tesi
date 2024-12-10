from huggingface_hub import InferenceClient

class ResponseGenerator:
    def __init__(self, api_key, model_name):
        self.client = InferenceClient(api_key=api_key)
        self.model_name = model_name

    def generate_response(self, query, relevant_chunks):
        context = " ".join([chunk['text'] for chunk in relevant_chunks])
        input_text = f"Contesto: {context}\nDomanda: {query}"

        # questo è il formato in cui Mixtral si aspetta di ricevere una domanda
        messages = [
            {
                "role": "user",
                "content": input_text
            }
        ]

        stream = self.client.chat.completions.create(
            model=self.model_name, 
            messages=messages, 
            max_tokens=500,
            stream=True
        )

        response = ""
        for chunk in stream:
            response += chunk.choices[0].delta.content
        return response