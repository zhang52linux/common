# _*_ coding: utf-8 _*_
import asyncio
import json
import traceback
from functools import wraps
from typing import Coroutine

from loguru import logger


def retry_if_exception(ex: Exception, retry_cout: int = 3, wait: int = 1, out_exc=False):
    """ 捕获异常进行重试
    :param ex: 异常
    :param retry: 重试次数
    :param wait: 重试间隔(秒)
    :param out_exc: 输出错误栈
    """
    def safe_function(func):
        @wraps(func)
        async def wrapper(*arg, **kwargs):
            assert retry_cout > 0
            cnt = retry_cout + 1
            while cnt := cnt - 1:
                try:
                    result = await func(*arg, **kwargs)
                    return result
                except ex as e:
                    logger.warning(f'{func.__name__ }:{func.__doc__ }:{e.args}')
                    out_exc and logger.error(traceback.format_exc())
                    await asyncio.sleep(wait)
            return False
        return wrapper
    return safe_function


def callback_if_exception(ex: Exception, callback: Coroutine, out_exc=False):
    """捕获到指定异常时进行回调
    Args:
        ex (Exception): 捕获异常
        callback (Coroutine): 回调函数
    Returns:
        _type_: _description_
    """
    def outer(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ex as e:
                out_exc and logger.error(traceback.format_exc())
                return await callback(func, *args, **kwargs)
        return wrapper
    return outer


def json_to_obj(func):
    """ 添加 `json_load`参数 为True时将json字符串转换Python对象 """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        if kwargs.get('json_load') or kwargs.get('json_loads'):
            if isinstance(result, list):
                result = [json.loads(i) for i in result if isinstance(i, str)]
            elif isinstance(result, set):
                result = (json.loads(i) for i in result if isinstance(i, str))
            elif isinstance(result, str):
                result = json.loads(result)
        return result
    return wrapper
