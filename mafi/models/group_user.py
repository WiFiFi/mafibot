from datetime import datetime
from tortoise.models import Model
from tortoise import fields


class GroupUser(Model):
    id = fields.IntField(pk=True)
    user_qq = fields.BigIntField(null=False)
    belonging_group = fields.BigIntField(null=False)
    checkin_count = fields.IntField(null=False, default=0)
    checkin_time_last = fields.DatetimeField(null=False, default=datetime.min)
    credit = fields.IntField(null=False, default=0)

    class Meta:
        table = 'group_users'
        unique_together = ('user_qq', 'belonging_group')
        indexes = ('user_qq', 'belonging_group')

    def __str__(self):
        return 'QQ：' + str(self.user_qq) + '，群：' + str(self.belonging_group) + '，积分：' + str(self.credit)