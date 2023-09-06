import asyncio
import concurrent.futures
from functools import partial
from functools import wraps
from typing import Any
from typing import Callable
from typing import Optional


def wrap_sync_to_async(func: Callable) -> Callable:
    """
    Декоратор, который принимает синхронную функцию и выполняет её в отдельном потоке,
    которая запускает исходную функцию в отдельном потоке.

    :param func: исходная асинхронная функция
    :return: новая асинхронная функция, которая запускает исходную функцию в отдельном потоке
    """

    @wraps(func)
    async def run(
        *args,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        executor: Optional[concurrent.futures.Executor] = None,
        **kwargs,
    ) -> Any:
        """
        Функция, которая запускает исходную функцию в отдельном потоке.

        :param args: Позиционные аргументы для исходной функции
        :param loop: event loop, который будет использоваться для запуска исходной функции
        :param executor: executor, который будет использоваться для запуска исходной функции
        :param kwargs: именованные аргументы для исходной функции
        :return: результат выполнения исходной функции
        """
        if loop is None:
            loop = asyncio.get_running_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


__all__ = ["wrap_sync_to_async"]
