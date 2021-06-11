from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command

from services.setu import setu
from services.command_use_count import record_successful_invocation
from services.common import ServiceException
from services.credit_process import _credit_check, _credit_add, _credit_lose


__plugin_name__ = 'setu/ghs(1积分)'
__plugin_usage__ = (
    '用法：\n'
    '有好康的哦~~~'
)


setu_permission = lambda sender: (not sender.is_privatechat) or sender.is_superuser

@on_command('setu', aliases=('色图', '来张色图', '来张setu'), permission=setu_permission)
@record_successful_invocation('setu')  # 命令名 - 或者是任何表示名字的字符串
async def _(session: CommandSession):
    success = await _credit_lose(session.event.user_id, session.event.group_id, 1)
    if success:
        try:
            result = await setu(r18=0)
            credit_remain = await _credit_check(session.event.user_id, session.event.group_id)
            result = result + '\n剩余积分：' + str(credit_remain)
        except ServiceException as e:
            result = e.message
            await _credit_add(session.event.user_id, session.event.group_id, 1)
    else:
        result = '积分不足，请先获取积分'
    await session.send(result, at_sender=True)


@on_command('ghs', permission=setu_permission)
@record_successful_invocation('ghs')  # 命令名 - 或者是任何表示名字的字符串
async def _(session: CommandSession):
    success = await _credit_lose(session.event.user_id, session.event.group_id, 1)
    if success:
        try:
            result = await setu(r18=1)
            credit_remain = await _credit_check(session.event.user_id, session.event.group_id)
            result = result + '\n剩余积分：' + str(credit_remain)
        except ServiceException as e:
            result = e.message
            await _credit_add(session.event.user_id, session.event.group_id, 1)
    else:
        result = '积分不足，请先获取积分'
    await session.send(result, at_sender=True)