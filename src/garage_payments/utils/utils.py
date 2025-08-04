from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
from pandas import Series, to_datetime, DataFrame, notna
from pytz import timezone


def get_number_column(object: DataFrame, pattern: str) -> int | None:
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


def tz(
    object: DataFrame, old: str, new: str, format: str = "%d.%m.%Y %H:%M"
) -> DataFrame:
    """
    Задает нужную временную зону в дате платежа

    :param object: pandas DataFrame
    :param old: Название временной зоны (начальное)
    :param new: Название временной зоны (итоговое)
    :param format: Формат даты
    :return: Столбец DataFrame в формате datetime
    """
    return (
        to_datetime(object, format=format)
        .dt.tz_localize(old)
        .dt.tz_convert(new)
        .dt.tz_localize(None)
    )


def to_float(object: Series, replacements: list[tuple[str, str]]) -> DataFrame:
    """
    Преобразовывает все значения в столбце сумм в тип float

    :param object: pandas DataFrame
    :param replacements: Список кортежей с паттернами для замены
    :return: Столбец DataFrame в формате float
    """

    def process_value(x):
        if isinstance(x, (int, float)):
            return float(x)
        elif isinstance(x, str):
            result = (
                Series([x])
                .str.extract(r"([+-]?\d+\s?\d*,\d+|\d+\s?\d*,\d+)")
                .iloc[0, 0]
            )
            if notna(result):
                for old, new in replacements:
                    result = result.replace(old, new)
                try:
                    return float(result)
                except (ValueError, TypeError):
                    return None
            return None
        return None

    return object.apply(process_value)


def next_payment_datetime(
    object: DataFrame,
    current_datetime: datetime,
    offset: int = 1,
    zone: str = "Asia/Novosibirsk",
) -> Series:
    """
    Вычисляет дату платежа в любой из n периодов

    :param object:
    :param current_datetime:
    :param offset:
    :param zone:
    :return:
    """
    current_datetime = current_datetime.astimezone(timezone(zone=zone))

    month_delta = (
        (current_datetime.year - object.initial_datetime.dt.year) * 12
        + (current_datetime.month - object.initial_datetime.dt.month)
        + offset
    )

    return Series(
        [
            d + relativedelta(months=m)
            for d, m in zip(object.initial_datetime, month_delta)
        ],
        index=object.initial_datetime.index,
    )
