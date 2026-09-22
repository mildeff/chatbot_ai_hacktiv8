from openai import OpenAI
import config

def get_openai_client(api_key: str) -> OpenAI:
      return OpenAI(api_key=api_key)

def prepare_message(system_prompt: str, chat_history: list, user_input: str, enable_memory: bool) -> list:
      api_messages = [
            {
                  "role": "system",
                  "content": system_prompt
            }
      ]

      if enable_memory:
        # Hanya masukkan riwayat yang isi 'content'-nya berupa string dan tidak kosong
        for msg in chat_history:
            content = msg.get("content")
            if content and isinstance(content, str):
                api_messages.append({"role": msg["role"], "content": content})
    
      # Masukkan input terbaru dari pengguna
      if user_input:
            api_messages.append({"role": "user", "content": str(user_input)})
      
      return api_messages

def generate_triage_response(client: OpenAI, api_messages: list, temperature: float) -> str:
      response = client.chat.completions.create(
            model=config.DEFAULT_MODEL,
            messages=api_messages,
            temperature=temperature
      )
      return response.choices[0].message.content