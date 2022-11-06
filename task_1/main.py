import random

import pandas as pd
from numba import njit, types
from numba.typed import Dict
import numpy as np

time_user_map = {}


def _define_session(row: np.ndarray, session_duration: float) -> int:
    """
    Функция для определения сессии

    :param row: текущая строка dataframe, переведенная в формат numpy-массива
    :param session_duration: предельная длина сессии, секунд

    :return: id сессии
    """
    if row[1] not in time_user_map:
        session_id = random.randint(1, 2 ** 63 - 1)
        time_user_map[row[1]] = {"event_time": row[0],
                                 "session_id": session_id}
        return session_id

    prev_event_time = time_user_map[row[1]]["event_time"]

    if (row[0] - prev_event_time).seconds > session_duration:
        session_id = random.randint(1, 2 ** 63 - 1)
        time_user_map[row[1]]["session_id"] = session_id
    else:
        session_id = time_user_map[row[1]]["session_id"]

    time_user_map[row[1]]["event_time"] = row[0]

    return session_id


@njit
def _define_session_numba(df_numpy: np.ndarray, session_duration: float) -> np.ndarray:
    """
    Функция для определения сессии

    :param df_numpy: dataframe, переведенный в формат numpy-массива
    :param session_duration: предельная длина сессии, секунд

    :return: массив id-сессий, длиной df_numpy.shape[0]
    """

    user_time_map = Dict.empty(
        key_type=types.int64,
        value_type=types.float64
    )

    user_session_map = Dict.empty(
        key_type=types.int64,
        value_type=types.int64
    )

    session_ids = np.empty(df_numpy.shape[0])

    for i in range(df_numpy.shape[0]):

        user_id = int(df_numpy[i][1])

        if user_id not in user_time_map:
            session_id = random.randint(1, 2 ** 63 - 1)

            user_time_map[user_id] = df_numpy[i][0]
            user_session_map[user_id] = session_id
            session_ids[i] = session_id
            continue

        prev_event_time = user_time_map[user_id]

        if (df_numpy[i][0] - prev_event_time) > session_duration:
            session_id = random.randint(1, 2 ** 63 - 1)
            user_session_map[user_id] = session_id
        else:
            session_id = user_session_map[user_id]

        session_ids[i] = session_id
        user_time_map[user_id] = df_numpy[i][0]

    return session_ids


def main(df: pd.DataFrame, session_duration: float = 180, use_numba: bool = True) -> pd.DataFrame:
    """
    Метод для проставления id сессии в DataFrame

    :param df: исходный DataFrame без id сессии
    :param session_duration: предельная длина сессии, секунд
    :param use_numba: использовать ли быстрый метод расчета с Numba
    :return: DataFrame с проставленным id сессии

    """
    if not use_numba:
        df["session_id"] = df[["event_time", "user_id"]].apply(_define_session, raw=True, axis=1,
                                                               args=(session_duration,))
        return df

    # numba не поддерживает datetime
    df["event_time_secs"] = (df["event_time"] - pd.Timestamp("1970-01-01", tz='UTC')) / pd.Timedelta('1s')
    df["session_id"] = _define_session_numba(df[["event_time_secs", "user_id"]].values,
                                             session_duration=session_duration)
    del df["event_time_secs"]

    return df


if __name__ == "__main__":
    import time

    start = time.time()

    use_numba = True
    session_duration = 180

    init_df = pd.read_parquet('df.parquet.gzip')

    df = main(init_df, session_duration, use_numba)

    print(time.time() - start)

    df.to_csv("result.csv")
