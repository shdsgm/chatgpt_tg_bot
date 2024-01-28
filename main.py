import logging
from aiogram import Bot, Dispatcher, types
import g4f
from aiogram.filters.command import Command
import asyncio


# Logging on
logging.basicConfig(level=logging.INFO)

# Bot init
API_TOKEN = 'INSERT YOUR TOKEN HERE'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Dict for chat history
conversation_history = {}

# Function for trim chat history
def trim_history(history, max_length=4096):
    current_length = sum(len(message["content"]) for message in history)
    while history and current_length > max_length:
        removed_message = history.pop(0)
        current_length -= len(removed_message["content"])
    return history

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Hi {message.from_user.full_name}, this is a ChatGPT bot. To use it just simply send me a message and i will try to answer.")


@dp.message(Command("clear"))
async def process_clear_command(message: types.Message):
    user_id = message.from_user.id
    conversation_history[user_id] = []
    await message.reply("Dialog history deleted.")

@dp.message(Command("help"))
async def bot_info_details(message: types.Message):
    await message.answer("""
This bot has some limitations with 4096 max tokens. If you exceed this number please use /clear command.

If you want to clear context of the dialog or start new one please use /clear command.

It uses ChatGPT 3.5 model and gpt4free library, so sometimes it can be unstable and will not work. 

If you have any questions, please dm me: @shdsgm
    """)

# Handler for every new message
@dp.message()
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_input = message.text

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({"role": "user", "content": user_input})
    conversation_history[user_id] = trim_history(conversation_history[user_id])

    chat_history = conversation_history[user_id]

    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=chat_history,
            provider=g4f.Provider.GeekGpt,
        )
        chat_gpt_response = response
    except Exception as e:
        print(f"{g4f.Provider.GeekGpt.__name__}:", e)
        chat_gpt_response = "Sorry. Error occurred. Please try again or later. "

    conversation_history[user_id].append({"role": "assistant", "content": chat_gpt_response})
    print(conversation_history)
    length = sum(len(message["content"]) for message in conversation_history[user_id])
    print(length)
    await message.answer(chat_gpt_response)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
