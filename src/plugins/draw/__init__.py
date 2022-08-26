from nonebot import get_driver, on_shell_command
from nonebot.adapters.onebot.v11 import Message, Bot, MessageEvent, MessageSegment
from nonebot.internal.params import ArgStr
from nonebot.params import CommandArg, ShellCommandArgs
from nonebot.typing import T_State
from nonebot.utils import run_sync

from . import translate
from .config import Config
from .txt2img import get_parser

# global_config = get_driver().config
# config = Config.parse_obj(global_config)

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass


parser = get_parser()
command = on_shell_command(
    "draw", aliases={"画", "绘画"}, priority=5, block=True, parser=parser
)


@command.handle()
async def _(state: T_State, opt=ShellCommandArgs()):
    if opt.prompt is not None:
        state["txt"] = " ".join(opt.prompt)


@command.got("txt", prompt="你想要生成什么样的图片？")
async def _(txt_str: str = ArgStr("txt"), opt=ShellCommandArgs()):
    # 检测语言
    language = translate.langDetect(txt_str)
    # 若语言不是英语，则翻译
    if language != "en":
        txt_str = translate.translate(txt_str)

    await command.send("正在创作中,请等待大约1分钟: " + txt_str, at_sender=True)
    opt.prompt = txt_str
    img_out_path = await txt2img.txt2img(opt)
    msg_image = MessageSegment.image(
        "file:///Users/zhenyue/Projects/stable-diffusion-bot/" + img_out_path
    )
    await command.send(msg_image, at_sender=True)
