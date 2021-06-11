from .common import fetch_json


async def setu(r18: int = 0) -> str:
    try:
        res = await fetch_json(f'https://api.lolicon.app/setu?r18={r18}')
        setu_title=res['data'][0]['title']
        setu_url=res['data'][0]['url']
        setu_pid=res['data'][0]['pid']
        setu_author=res['data'][0]['author']
        local_img_url = "title:" + setu_title + "[CQ:image,file=" + setu_url + "]" + "pid:" + str(setu_pid) + " 画师:" + setu_author
        return local_img_url.strip()
    except Exception as e:
        print(e)
        return '阿这，好像出了一点问题'