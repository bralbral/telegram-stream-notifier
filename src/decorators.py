import asyncio
import concurrent.futures
from functools import partial
from functools import wraps
from typing import Any
from typing import Callable
from typing import Optional


def wrap_sync_to_async(func: Callable) -> Callable:
    """
    :param func:
    :return:
    """

    @wraps(func)
    async def run(
        *args,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        executor: Optional[concurrent.futures.Executor] = None,
        **kwargs,
    ) -> Any:
        """
        :param args:
        :param loop:
        :param executor:
        :param kwargs:
        :return:
        """
        if loop is None:
            loop = asyncio.get_running_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


__all__ = ["wrap_sync_to_async"]
