from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from typing import Union

from ..data import (
    get_films,
    get_film,
    save_film
)

from ..keyboards import (
    build_films_keyboard,
    build_film_details_keyboard,
    build_menu_keyboard
)

from ..fsm import FilmCreateForm

from .Utils import edit_or_answer
film_router = Router()



@film_router.callback_query(F.data == "films")
@film_router.message(Command("films"))
@film_router.message(F.text.casefold() == "films")
async def show_films_command(message: Union[CallbackQuery, Message], state: FSMContext) -> None:
    films = get_films()
    if isinstance(message, Message):
        if films:
            keyboard = build_films_keyboard(films)
            await edit_or_answer(message, "Виберіть будь-який фільм", keyboard)
        else:
            await edit_or_answer(message,
             "Нажаль зараз відсутні фільми. Спробуйте /filmcreate для створення нового.",
              ReplyKeyboardRemove())
    elif isinstance(message, CallbackQuery):
        if films:
            keyboard = build_films_keyboard(films)
            await edit_or_answer(
                message.message,
            "Виберіть будь-який фільм",
                 keyboard)
        else:
            await edit_or_answer(
                message.message,
          "Нажаль зараз відсутні фільми. Спробуйте /filmcreate для створення нового.")


@film_router.message(Command("filmcreate"))
@film_router.callback_query(F.data == "filmcreate")
@film_router.message(F.text.casefold() == "filmcreate")
@film_router.message(F.text.casefold() == "create film")
async def create_film_command(message: Union[Message, CallbackQuery], state: FSMContext) -> None:
    await state.clear()
    await state.set_state(FilmCreateForm.title)
    await edit_or_answer(message, "Яка назва фільму?", ReplyKeyboardRemove())


# from aiogram.utils.markdown import hbold
@film_router.callback_query(F.data.startswith("film_"))
async def show_film_details(callback: CallbackQuery, state: FSMContext) -> None:
    film_id = int(callback.data.split("_")[-1])
    film = get_film(film_id)
    text = (f"Назва: {hbold(film.get('title'))}\n"
            f"Опис: {hbold(film.get('desc'))}\n"
            f"Рейтинг: {hbold(film.get('rating'))}")
    photo_id = film.get('photo')
    url = film.get('url')
    await callback.message.answer_photo(photo_id)
    await edit_or_answer(callback.message, text, build_film_details_keyboard(url))


@film_router.message(FilmCreateForm.title)
async def proces_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(FilmCreateForm.desc)
    await edit_or_answer(message, "Який опис фільму?", ReplyKeyboardRemove())

@film_router.message(FilmCreateForm.desc)
async def proces_description(message: Message, state: FSMContext) -> None:
    data = await state.update_data(desc=message.text)
    await state.set_state(FilmCreateForm.url) # error
    await edit_or_answer(
        message,
        f"Введіть посилання на фільм: {hbold(data.get('title'))}",
        ReplyKeyboardRemove(),
    )

@film_router.message(FilmCreateForm.url)
@film_router.message(F.text.contains('http'))
async def procees_url(message: Message, state: FSMContext) -> None:
    data = await state.update_data(url=message.text)
    await state.set_state(FilmCreateForm.photo)
    await edit_or_answer(
        message,
        f"Надайте фото для афіши фільму: {hbold(data.get('title'))}",
        ReplyKeyboardRemove(),
    )

@film_router.message(FilmCreateForm.photo)
@film_router.message(F.photo)
async def proces_photo(message: Message, state: FSMContext) -> None:
    photo = message.photo[-1]
    photo_id = photo.file_id

    data = await state.update_data(photo=photo_id)
    await state.clear()
    save_film(data)
    return await show_films_command(message, state)

@film_router.callback_query(F.data == "back")
@film_router.message(Command("back"))
async def back_handler(callback: Union[CallbackQuery, Message], state: FSMContext) -> None:
    await state.clear()
    return await show_films_command(callback.message, state)

