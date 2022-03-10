# _*_ coding: utf-8 _*_
import asyncio
import json
import traceback
from functools import wraps
from typing import Coroutine

from loguru import logger

# TODO 断网处理


def retry_if_exception(ex: Exception, retry: int, wait: int = 1, out_exc: bool = True):
    """捕获异常进行重试 装饰器
    Args:
        ex (Exception): 异常
        retry (int): 重试次数
        wait (int, optional): 重试间隔. Defaults to 1.
        out_exc (bool, optional): 输出错误信息. Defaults to True.
    """
    def outer(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            assert retry > 0
            cnt = retry + 1
            while cnt := cnt - 1:
                try:
                    return await func(*args, **kwargs)
                except ex as e:
                    logger.warning(f'{func.__module__ }.{func.__name__ }:{e.__class__}{e.args}')
                    out_exc and logger.error(traceback.format_exc())
                    await asyncio.sleep(wait)
        return wrapper
    return outer


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