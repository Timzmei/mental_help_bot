import os
from dotenv import load_dotenv
import g4f, asyncio

g4f.debug.logging = True # enable logging
g4f.check_version = False # Disable automatic version checking


class Chat_bot:
  # Загрузить переменные окружения из .env файла
  load_dotenv()


  semaphore = asyncio.Semaphore(1)

  @classmethod
  async def create_chat_completion(cls, messages):
      try:
          print("Начало create_chat_completion")
          async with cls.semaphore:
            completion = await g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_35_turbo,
                # model=g4f.models.gpt_4,
                messages=messages
            )
          print("Завершение create_chat_completion")
          return completion
      except Exception as e:
          # Обработка ошибки
          print(f"Произошла ошибка: {e}")
          return None  # Возврат None или другого значения, чтобы показать, что произошла ошибка
  
  
# async def main():
#   text = await Nova_bot.create_chat_completion([{"role": "user", "content": "Hello"}])
#   print(text)

# if __name__ == "__main__":
#     asyncio.run(main())
          