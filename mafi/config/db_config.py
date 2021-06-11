from tortoise import Tortoise, run_async
from services.log import logger


DB_TYPE = 'mysql'
USERNAME = 'root'
PASSWORD = '123456'
HOST = '127.0.0.1'
PORT = 3306
DB_NAME = 'qqbot'
DB_URL = f'{DB_TYPE}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'

models = [
    'models.group_user',
    'models.command_use'
]

async def init():
    await Tortoise.init(
        db_url=DB_URL,
        modules={'models': models}
    )
    await Tortoise.generate_schemas()
    logger.info('Database loaded successfully!')
