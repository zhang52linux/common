# _*_ coding:utf-8 _*_
"""
*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
Author: zhangsanyong
Date: 2022-02-11 22:04:47
LastEditors: zhangsanyong
LastEditTime: 2022-02-11 22:04:48
Description: aiohttp:RuntimeError:Event loop is closed.解决
默认python3.8后, windows默认采用ProactorEventLoop事件循环, 程序退出释放内存时自动调用其_ProactorBasePipeTransport.__del__方法关闭循环
而使用asyncio.run()是也会自动关闭循环, 从而报Event loop is closed异常, 重写__del__方法, 捕获异常
*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
"""

from functools import wraps

from asyncio.proactor_events import _ProactorBasePipeTransport


def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper


_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
