from json import dumps

from quart import Quart, websocket, send_file

from config.service_config import RESOURCES_DIR
from services import command_use_count, inmsg_count
from services.broadcast import listen_to_broadcasts, as_payload


def add_controllers(app: Quart):

    @app.route('/dashboard', ['GET'])
    async def _dashboard_get():
        return await send_file(f'{RESOURCES_DIR}/dashboard.html')

    @app.websocket('/expose')
    async def _expose_ws():
        # 主动调用 API，打上类型标签，填充完整的命令调用信息 (bootstrap)
        await websocket.send(dumps(as_payload('messageLoad', await inmsg_count.get_count())))
        await websocket.send(dumps(as_payload('pluginUsage', await command_use_count.get_count())))
        # 然后再接入消息队列被动获取信息
        with listen_to_broadcasts('messageLoad', 'pluginUsage') as get:
            while True:
                payload = await get()
                await websocket.send(dumps(payload))
