# xiaoaiTTS

小爱同学智能音箱TTS服务API

## 使用

1. 注册小米账户 https://account.xiaomi.com

2. 将小爱音箱与账户关联（下载米家APP）

3. 从源码安装

   ```bash
   pip install wheel
   python setup.py bdist_wheel
   pip install dist/xiaoaitts-0.0.0-py3-none-any.whl
   ```

4. 具体使用查看`demo.py`文件

## 初始需求

@王旭 驱动智能音箱的工具。

## 实际需求

@王畅 演示的时候有个喝咖啡的应用，煮好咖啡后会有个提示。北大那边的需求是给智能设备发条消息，智能设备发出提示音。

## 不被采纳的建议

监控以及控制智能设备需要有台机器跑后端程序，用这台机器发声：

```bash
# Linux
echo "Text to speak"|espeak
# macOS
say "Text to speak"
```

## 问题

- 查阅[开发文档](https://123.125.102.180/documents/Home?type=/api/doc/render_markdown/VoiceserviceAccess/Reference/ProtocolDocument/APIReference/SpeechSynthesizer)，只有人给命令->唤醒音箱->音箱解析给服务器->服务器应答->音箱响应的开发场景。

  而让音箱主动发声（不唤醒）是特殊需求，实现起来很麻烦。
  
- 周三提出来，音箱周四晚上到

## 相关资料

- 小爱开放平台：https://123.125.102.180/documents/Home?type=/api/doc/render_markdown/VoiceserviceAccess/Reference/ProtocolDocument/APIReference/SpeechSynthesizer
- 分享一下关于小爱音响的几个接口文件：https://bbs.hassbian.com/thread-4996-1-1.html
- 【1014更新】小爱音箱系统破解实现更多功能（重大进展）：https://bbs.hassbian.com/thread-4961-1-1.html
- 小爱同学TTS服务（2019年5月29日更新可用版本）：https://bbs.hassbian.com/forum.php?mod=viewthread&tid=3669&extra=&authorid=1417&page=1