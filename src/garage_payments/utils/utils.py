from datetime import datetime, timedelta
from pytz import timezone
from dateutil.relativedelta import relativedelta

import pandas as pd


def get_number_column(object: pd.DataFrame, pattern: str) -> int | None:
    """
    Находит индекс первого столбца, содержащего значение, соответствующее заданному шаблону.

    :param object: pandas DataFrame
    :param pattern: Шаблон регулярного выражения для поиска (регистронезависимый)
    :return: Индекс первого подходящего столбца или None, если совпадений нет
    """
    matches = object.apply(
        lambda col: col.astype(str).str.contains(pattern, regex=True, case=False)
    )

    idx = [
        object.columns.get_loc(col)
        for row in matches.index
        for col in matches.columns
        if matches.loc[row, col]
    ]

    try:
        return idx[0]
    except:
        return None


def tz(object: pd.DataFrame, old: str, new: str, format: str = "%d.%m.%Y %H:%M") -> pd.DataFrame:
    """

    :param object: pandas DataFrame
    :param old: Название временной зоны (начальное)
    :param new: Название временной зоны (итоговое)
    :param format: Формат даты
    :return: Столбец DataFrame в формате datetime
    """
    return pd.to_datetime(object, format=format).dt.tz_localize(old).dt.tz_convert(new)


def to_float(object, replacements: list[tuple[str, str]]) -> pd.DataFrame:
    """

    :param object: pandas DataFrame
    :param replacements: Список кортежей с паттернами для замены
    :return: Столбец DataFrame в формате float
    """
    result = object.str.extract(r"([+-]?\d+\s?\d*,\d+|\d+\s?\d*,\d+)")[0]
    for old, new in replacements:
        result = result.str.replace(old, new)
    return result.astype(float)


def next_payment_datetime(object: pd.DataFrame, current_datetime: datetime, tz: str = "Asia/Novosibirsk") -> pd.DataFrame:
    init_date = object['initial_datetime']
    next_payment = current_datetime.astimezone(timezone(zone=tz))

    # Получаем разницу в месяцах между текущей датой оплаты и начальной датой
    months_diff = (next_payment.year - init_date.year) * 12 + next_payment.month - init_date.month

    # Вычисляем следующую дату оплаты (следующий месяц)
    next_payment += relativedelta(months=1)

    # Корректировка для високосного года (29 февраля)
    if init_date.day == 29 and init_date.month == 2:
        if not (next_payment.year % 4 == 0 and (next_payment.year % 100 != 0 or next_payment.year % 400 == 0)):
            next_payment = next_payment.replace(day=28)

    # Добавляем 3 дня к дате оплаты
    next_payment += timedelta(days=3)

    # Проверяем, что следующая дата оплаты позже текущей даты
    if next_payment.date() <= current_datetime.date():
        next_payment = next_payment + relativedelta(months=1)
        # Повторная корректировка для високосного года
        if init_date.day == 29 and init_date.month == 2:
            if not (next_payment.year % 4 == 0 and (next_payment.year % 100 != 0 or next_payment.year % 400 == 0)):
                next_payment = next_payment.replace(day=28)
        next_payment = next_payment + timedelta(days=3)

    return next_payment