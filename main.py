from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import astrbot.api.message_components as Comp
from astrbot.api import logger
import os
import json
import random
import time
import requests

@register("astrbotAudio", "cc", "一个简单的 Audio 插件", "1.0.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.wav_dir = '/AstrBot/data/plugins/astrbotaudio/wav'
        self.wav_q = 'fl_'
        # 服务器地址配置
        # self.comfyui_api_url = "http://38.55.205.201:12347/"  # 默认本地地址，可根据实际情况修改
        
    # 注册指令的装饰器。指令名为 comfyui。注册成功后，发送 `/comfyuitxt` 就会触发这个指令
    # @filter.command("comfyuitxt")
    @filter.command_group("audio")
    def audio():
        pass
    
    @audio.group("yulv") # 请注意，这里是 group，而不是 command_group
    def yulv():
        pass
    @yulv.command("help")
    async def help(self, event: AstrMessageEvent):
        s = ["用于播放月绿语录。",
             "指令：",
             "- /audio yulv all--列出所有语录",
             "- /audio yulv select xxx--选择一个语录",
             "- /audio yulv random--随机一个语录",
             "- /audio yulv ai xxx--ai克隆 待开放"
             ]
        chain = [
            Comp.Plain(json(s)),
        ]
        yield event.chain_result(chain)
    @yulv.command("all")
    async def all(self, event: AstrMessageEvent):
        logger.info("列出所有音频")
        mp3_files = self.get_wav_files()
        if mp3_files:
            chain = [
                Comp.Plain("现有语录："),
                Comp.Plain("\n".join(mp3_files)),
            ]
            yield event.chain_result(chain)
        else:
             yield event.plain_result("没有音频")
    @yulv.command("random")
    async def random1(self, event: AstrMessageEvent):
        logger.info("随机一个音频")
        mp3_files = self.get_wav_files()
        if mp3_files:
            random_file = random.choice(mp3_files)
            logger.info(f"随机一个音频：{random_file}")
            path = f'{self.wav_dir}/{random_file}.wav'
            # Comp.Record(file=path, url=path)
            yield event.chain_result([Comp.Record(file=path, url=path)])
        else:
             yield event.plain_result("没有音频")

    @yulv.command("select")
    async def select(self, event: AstrMessageEvent):
        message_str = event.message_str
        s = message_str.split("select ")
        mp3_files = self.get_wav_files(s[1])
        logger.info(f"选择一个音频：{mp3_files}")
        if mp3_files:
            path = f'{self.wav_dir}/{mp3_files[0]}.wav'
            # Comp.Record(file=path, url=path)
            yield event.chain_result([Comp.Record(file=path, url=path)])
        else:
             yield event.plain_result("没有音频")

    @yulv.command("ai")
    async def ai(self, event: AstrMessageEvent):
        message_str = event.message_str
        s = message_str.split("yulv ai ")
        logger.info(f"克隆一个音频：{s}")
        yield event.plain_result("本地服务器暂未部署，云端要钱不想部署")
    def get_wav_files(self,s:str=None):
        wav_folder = self.wav_dir  # 文件夹路径 
        try:
            # 确保文件夹存在
            if not os.path.exists(wav_folder):
                logger.warning(f"指定的音频文件夹不存在: {wav_folder}")
                return []                
            mp3_files = []
            logger.info(f"获取wav文件列表")
            # 遍历文件夹中的所有文件
            if s:
                for file in os.listdir(wav_folder):
                    if file.startswith(s):
                        if file.endswith('.wav'):  # 检查文件扩展名是否为 .wav
                            # 使用 os.path.splitext 移除扩展名
                            filename_without_extension = os.path.splitext(file)[0]
                            filename = filename_without_extension.replace(self.wav_q, ' ')
                            if s in filename_without_extension:
                                mp3_files.append(filename_without_extension)
                                break
                if mp3_files:
                    return mp3_files
                else:
                    return []
            else:    
                for file in os.listdir(wav_folder):
                    if file.endswith('.wav'):  # 检查文件扩展名是否为 .wav
                        # 使用 os.path.splitext 移除扩展名
                        filename_without_extension = os.path.splitext(file)[0]
                        filename = filename_without_extension.replace(self.wav_q, ' ')
                        mp3_files.append(filename)
                return mp3_files       
        except Exception as e:
            logger.error(f"读取wav文件列表时发生错误: {e}")
            return []  # 发生异常时也返回空列表以保证接口一致性