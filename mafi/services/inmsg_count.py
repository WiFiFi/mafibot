'''
消息计数
消息计数的需求为：

统计过去 60 秒内机器人收到的消息数目
统计上一秒内机器人收到的消息数目
可以想到此功能需要每秒都运行。如果使用一个表示过去一分钟每一秒的消息数的数组的话，每当有一条消息被收到则对应数组计数加一，而每秒钟还要归零第 61 秒前的计数。过去 60 秒内的计数就是数组里数字的和
'''
import asyncio
from datetime import datetime
from typing import Dict, Optional

from .broadcast import broadcast
from .log import logger


_counts = [0 for _ in range(61)]

_epoch = datetime.now()


def _get_offset() -> int:
    return int((datetime.now() - _epoch).total_seconds()) % 61


async def get_count(curr_s: Optional[int] = None) -> Dict[str, int]:
    'Gets report that counts number of messages received in last 60s and last second.'
    if curr_s is None:
        curr_s = _get_offset()
    return {
        'lastMin': sum(_counts),
        'lastSec': _counts[curr_s - 1], # note [-1] indexes to [60]!
    }


async def increase_now():
    _counts[_get_offset()] += 1


async def init():
    'Kickstarts the message counting service (removing old counts) and brocasting.'
    loop = asyncio.get_event_loop()
    def _service():
        curr_s = _get_offset()
        # 归零第 61 秒前的计数
        _counts[curr_s + 1 if curr_s != 60 else 0] = 0
        # 把计数消息广播出去，然后等一秒钟再继续这个循环
        # logger.info('reset')  # 取消试试
        asyncio.create_task(broadcast('messageLoad', lambda: get_count(curr_s)))
        loop.call_at(int(loop.time()) + 1, _service)

    _service()
    logger.info('Message load count loaded successfully!')
