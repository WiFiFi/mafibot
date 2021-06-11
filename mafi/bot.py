from os import path
import nonebot

from config import bot_config
from config import db_config
from services import inmsg_count
from controllers import add_controllers


nonebot.init(bot_config)
# 第一个参数为插件路径，第二个参数为插件前缀（模块的前缀）
nonebot.load_plugins(path.join(path.dirname(__file__), 'bot_plugins'), 'bot_plugins')

# 如果使用 asgi
bot = nonebot.get_bot()
app = bot.asgi
add_controllers(bot.server_app)
nonebot.on_startup(db_config.init)
nonebot.on_startup(inmsg_count.init)

if __name__ == '__main__':
    nonebot.run()