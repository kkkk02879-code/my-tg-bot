import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

TOKEN = os.getenv("BOT_TOKEN", "ВАШ_ТОКЕН_БОТА")

RIDDLES = [
    {
        "question": "Загадка 1/3: Без рук, без ног, а ворота отворяет.",
        "answers": {"ветер"},
    },
    {
        "question": "Загадка 2/3: Зимой и летом одним цветом.",
        "answers": {"ель", "ёлка", "сосна"},
    },
    {
        "question": "Загадка 3/3: Висит груша — нельзя скушать.",
        "answers": {"лампочка", "лампа"},
    },
]


class BacktrackingGame(StatesGroup):
    playing = State()


dp = Dispatcher()


@dp.message(Command("backtracking"))
async def cmd_backtracking(message: Message, state: FSMContext) -> None:
    await state.set_state(BacktrackingGame.playing)
    await state.update_data(index=0, attempt=1)
    await message.answer(
        "Начинаем! Ответь на 3 загадки. На каждую даётся до 2 попыток.\n\n"
        f"{RIDDLES[0]['question']}"
    )


@dp.message(BacktrackingGame.playing, F.text)
async def handle_answer(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    index = data.get("index", 0)
    attempt = data.get("attempt", 1)

    user_answer = message.text.strip().lower()
    current_riddle = RIDDLES[index]

    if user_answer in current_riddle["answers"]:
        next_index = index + 1
        if next_index < len(RIDDLES):
            await state.update_data(index=next_index, attempt=1)
            await message.answer(f"Верно!\n\n{RIDDLES[next_index]['question']}")
        else:
            await state.clear()
            await message.answer("Молодец, ты справился!")
        return

    if attempt < 2:
        await state.update_data(attempt=2)
        await message.answer("Попробуй еще! Это твоя 2-я попытка.")
    else:
        await state.clear()
        await message.answer("Попробуй еще! Попытки закончились — введи /backtracking, чтобы начать заново.")


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())