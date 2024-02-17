import pytest
from handlers.different_types import cmd_start, message_with_text
from handlers.different_types import message_with_sticker
from handlers.different_types import message_with_gif, message_with_photo
from handlers.reccom import get_reccom_str, get_multiple_reccom_str
from handlers.reccom import cmd_reccom, Reccom
from handlers.reccom import reccom_chosen, reccoms_chosen
from handlers.reccom import food_chosen_incorrectly
from handlers.statistic import calc_avg_grade
from handlers.statistic import mk_review
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE
from aiogram.filters import Command
from aiogram.methods import SendMessage


# Тесты для different_types.py
@pytest.mark.asyncio
async def test_cmd_start():
    requester = MockedBot(
        request_handler=MessageHandler(cmd_start, Command(commands=["start"])))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="/start"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message.split(" ")[0] == "Приветствую"


@pytest.mark.asyncio
async def test_message_with_text():
    requester = MockedBot(request_handler=MessageHandler(message_with_text))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="text"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message.split(" ")[0] == "Команда"


@pytest.mark.asyncio
async def test_message_with_sticker():
    requester = MockedBot(request_handler=MessageHandler(message_with_sticker))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="sticker"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message.split(" ")[0] == "Стикер"


@pytest.mark.asyncio
async def test_message_with_gif():
    requester = MockedBot(request_handler=MessageHandler(message_with_gif))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="gif"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message.split(" ")[0] == "GIF"


@pytest.mark.asyncio
async def test_message_with_photo():
    requester = MockedBot(request_handler=MessageHandler(message_with_photo))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text='photo'))
    answer_message = calls.send_message.fetchone().text
    assert answer_message.split(" ")[0] == "Изображение"


# Тесты для reccom.py
@pytest.mark.asyncio
async def test_cmd_reccom():
    requester = MockedBot(
        request_handler=MessageHandler(cmd_reccom,
                                       Command(commands=["reccom"])))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="/reccom"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Выберете способ рекомендации:"


@pytest.mark.asyncio
async def test_reccom_chosen():
    requester = MockedBot(MessageHandler(reccom_chosen,
                                         state=Reccom.choosing_reccom))
    calls = await requester.query(MESSAGE.as_object(text="Одному пользовател"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Пожалуйста, введите uid пользователя:"


@pytest.mark.asyncio
async def test_reccoms_chosen():
    requester = MockedBot(MessageHandler(reccoms_chosen,
                                         state=Reccom.choosing_reccom))
    calls = await requester.query(
        MESSAGE.as_object(text="Списку пользователей"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Пожалуйста, введите список с uid пользователей:"


@pytest.mark.asyncio
async def test_chosen_incorrectly():
    requester = MockedBot(MessageHandler(food_chosen_incorrectly,
                                         state=Reccom.choosing_uid))
    calls = await requester.query(
        MESSAGE.as_object(text="Первому пользователю"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message.split(" ")[:2] == ["В", "тексте"]


@pytest.mark.asyncio
async def test_get_reccom_str():
    ans = get_reccom_str(['Soda', 'Cola'])
    assert ans == "1: Soda\n2: Cola\n"


@pytest.mark.asyncio
async def test_get_multiple_reccom_str():
    ans = get_multiple_reccom_str({'1': 'Cola', '21': 'Soda'})
    assert ans == "1: Cola\n21: Soda\n"


# Тесты statistic.py
@pytest.mark.asyncio
async def test_calc_avg_grade():
    ans = calc_avg_grade({'1': 1, '2': 1, '3': 1,
                          '4': 1, '5': 1})
    assert ans == 3


@pytest.mark.asyncio
async def test_mk_review():
    requester = MockedBot(
        request_handler=MessageHandler(mk_review,
                                       Command(commands=["make_review"])))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="/make_review"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Выберете оценку, которую заслжуил бот:"


if __name__ == '__main__':
    pytest.main()
