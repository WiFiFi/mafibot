from models.group_user import GroupUser
from tortoise.transactions import in_transaction


async def _credit_check(user_qq: int, belonging_group: int) -> str:
    user = (await GroupUser.get_or_create(user_qq=user_qq, belonging_group=belonging_group))[0]
    return user.credit


async def _credit_add(user_qq: int, belonging_group: int, credit_get: int):
    async with in_transaction() as connection:
        user = (await GroupUser.get_or_create(user_qq=user_qq, belonging_group=belonging_group))[0]
        user.credit = user.credit + credit_get
        await user.save()


async def _credit_lose(user_qq: int, belonging_group: int, credit_need: int) -> bool:
    async with in_transaction() as connection:
        user = (await GroupUser.get_or_create(user_qq=user_qq, belonging_group=belonging_group))[0]
        if user.credit < credit_need:
            return False
        else:
            user.credit = user.credit - credit_need
        await user.save()
        return True
