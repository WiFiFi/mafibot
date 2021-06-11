import asyncio
import random
from datetime import datetime
from io import BytesIO
from base64 import b64encode

from PIL import Image, ImageDraw, ImageFont

from .log import logger
from .processpool import processpool_executor
from models.group_user import GroupUser
from tortoise.transactions import in_transaction
from config.service_config import RESOURCES_DIR


async def group_user_check_in(user_qq: int, belonging_group: int) -> str:
    'Returns string describing the result of checking in'
    present = datetime.now()
    async with in_transaction() as connection:
        # 取得相应用户
        user = (await GroupUser.get_or_create(user_qq=user_qq, belonging_group=belonging_group))[0]
        # 如果同一天签到过，特殊处理
        if user.checkin_time_last.date() == present.date():
            return _handle_already_checked_in(user)
        return await _handle_check_in(user, present)


def _handle_already_checked_in(user: GroupUser) -> str:
    return f'已经签到过啦~ 当前积分：{user.credit}'


async def _handle_check_in(user: GroupUser, present: datetime) -> str:
    credit_added = random.choice((1, 2, 3, 4, 5, 6, 7, 8, 9))
    new_credit = user.credit + credit_added
    message = random.choice((
        '谢谢，你是个好人！',
        '对了，来喝杯茶吗？',
        '给阿姨倒一杯卡布奇诺~',
    ))
    if credit_added > 7:
        message = '⊙o⊙你就是天选之子吗？'
    elif credit_added < 3:
        message = '心疼你，摸摸~~~'

    user.checkin_count = user.checkin_count + 1
    user.checkin_time_last = present
    user.credit = new_credit
    await user.save()

    # 顺便打印此事件的日志
    logger.info(f'(USER {user.user_qq}, GROUP {user.belonging_group}) CHECKED IN successfully. score: {new_credit} (+{credit_added}).')

    return f'{message} 当前积分：{new_credit} (+{credit_added})'


async def group_user_check(user_qq: int, belonging_group: int) -> str:
    # heuristic: if users find they have never checked in they are probable to check in
    user = (await GroupUser.get_or_create(user_qq=user_qq, belonging_group=belonging_group))[0]
    return '当前积分：{}\n历史签到数：{}\n上次签到日期：{}'.format(
        user.credit,
        user.checkin_count,
        user.checkin_time_last.strftime('%Y-%m-%d') if user.checkin_time_last != datetime.min else '从未',
    )


############################################################################################################
########################################CPU密集型参考用######################################################
############################################################################################################
async def group_user_check_use_b64img(user_qq: int, belonging_group: int, user_name: str) -> str:
    'Returns the base64 image representation of the user check result.'
    user = (await GroupUser.get_or_create(user_qq=user_qq, belonging_group=belonging_group))[0]

    # expensive operation!
    return await asyncio.get_event_loop().run_in_executor(
        processpool_executor,
        _create_user_check_b64img,
        user_name, user,
    )


def _create_user_check_b64img(user_name: str, user: GroupUser) -> str:
    # 图像的参数是凭感觉来的
    # TODO: we have a lot of byte copies. we have to optimise them.
    bg_dir = f'{RESOURCES_DIR}/group_user_check_bg.png'
    font_dir = f'{RESOURCES_DIR}/SourceHanSans-Regular.otf'

    image = Image.open(bg_dir)
    draw = ImageDraw.ImageDraw(image)
    font_title = ImageFont.truetype(font_dir, 33 if len(user_name) < 8 else 28)
    font_detail = ImageFont.truetype(font_dir, 22)

    txt_user = f'{user_name} ({user.user_qq})'
    draw.text((530, 65), txt_user, fill=(255, 255, 255), font=font_title, stroke_width=1, stroke_fill='#7042ad')

    txt_detail = (
        f'群: {user.belonging_group}\n'
        f'积分: {user.credit}\n'
        f'签到数: {user.checkin_count}\n'
        f'上次签到: {user.checkin_time_last.strftime("%Y-%m-%d") if user.checkin_count else "从未"}'
    )
    draw.text((530, 115), txt_detail, fill=(255, 255, 255), font=font_detail, stroke_width=1, stroke_fill='#75559e')

    buff = BytesIO()
    image.save(buff, 'jpeg')
    return b64encode(buff.getvalue()).decode()