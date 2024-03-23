from aiogram.utils.keyboard import InlineKeyboardBuilder

def build_films_keyboard(films: list):
    builder = InlineKeyboardBuilder()
    for index, film in enumerate(films):
        builder.button(text=film.get('title'),
                       callback_data=f"film_{index}")
    return builder.as_markup()

def build_film_details_keyboard(url):
    builder = InlineKeyboardBuilder()
    builder.button(text="Перейти за посиланням", url=url)
    builder.button(text="Перейти назад", callback_data="back")
   # builder.button(text="Перейти назад", callback_data="back")
    return builder.as_markup()

def build_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Перелік фільмів", callback_data=f"films")
    builder.button(text="Додати новий фільм", callback_data=f"filmcreate")
    return builder.as_markup()
