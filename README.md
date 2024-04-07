# hse_mlds_recsys_project

## Начало работы
* Установка зависимостей `pip install -r requirements.txt`
* Тестирование `pytest -v tests/`
* Перед запуском сервиса в `.env` указать токен бота
* Запуск сервиса `docker compose build` и `docker compose up` 

## Описание данных

**Данные состоят из 2 [файлов](https://drive.google.com/drive/folders/1Z8uIxxGSSsER22x4Uh546jXuE8NUIUNz?usp=sharing):**
* *products.csv*  - товары с их характеристиками
* *transactions.csv*  - транзакции покупателей

**products.csv** 49688 строк
* *product_id* : int - уникальный идентификатор товара
* *product_name* : str - название товара
* *aisle_id* : int - уникальный идентификатор подкатегории
* *department_id* : int - уникальный идентификатор категории
* *aisle* : str - название подкатегории
* *department* : str - название категории

**transactions.csv** 26408073 строк
* *order_id* : int - уникальный идентификатор транзакции
* *user_id* : int - уникальный идентификатор покупателя
* *order_number* : int - номер транзакции в истории покупок данного пользователя
* *order_dow* : int - день недели транзакции
* *order_hour_of_day* : int - час совершения транзакции
* *days_since_prior_order* : float (1045204 None)- количество дней с совершения предыдущей транзакции данным пользователем
* *product_id* : int - уникальный идентификатор товара
* *add_to_cart_order* : float - номер под которым данный товар был добавлен в корзину
* *reordered* : float - был ли товар "перезаказан"


## Модели и результаты:

В ходе работы были реализованы 4 различных подхода к построению рекомендательных систем:

|  | MAP@k | MNAP@k | Hitrate@k | AVG_nDSG@k|  AVG_Precision@k | 
| --- | --- | --- | --- | --- |--- |
| Baseline Pop-based | 0.006 | 0.008 | 0.438 | 0.015 | 0.062 |
| Collaborative fitering | 0.007 | 0.013 | 0.505 | 0.017 | 0.074 |
| LightFM | 0.008 | 0.013 | 0.45 | 0.018 | 0.067 |
| EASE | 0.007 | 0.012 | 0.63 | 0.018 | 0.11 |


## Реализован [API](http://149.154.70.151:8000/docs):
![](https://github.com/poskryobik/hse_mlds_recsys_project/blob/main/img/API.gif)

## Реализован [Telegram Bot](https://t.me/hse_recsys_project_bot) @hse_recsys_project_bot:
![](https://github.com/poskryobik/hse_mlds_recsys_project/blob/main/img/bot.gif)

## План последующей работы:

* Реализовать рекомендательную систему с использованием нейросетевого подхода с целью прироста метрики качества.
