from tortoise.models import Model
from tortoise import fields

class CommandUse(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64, null=False)
    date = fields.DateField(null=False)
    use_count = fields.IntField(null=False, default=0)

    class Meta:
        table = 'command_uses'
        unique_together = ('name', 'date')
        indexes = ('name', 'date')

    def __str__(self):
        return 'Command：' + self.name + '，Date：' + str(self.date) + '，Use Count：' + str(self.use_count)
