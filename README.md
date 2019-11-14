# xiaoaiTTS

小爱同学智能音箱TTS服务API

## 需求

@王旭 驱动智能音箱的工具。

## 询问具体场景

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
  
- 双十一期间快递速度慢

## 目前找到的资料

- [经验分享] 分享一下关于小爱音响的几个接口文件：https://bbs.hassbian.com/thread-4996-1-1.html
- [新奇玩法]【1014更新】小爱音箱系统破解实现更多功能（重大进展）：https://bbs.hassbian.com/thread-4961-1-1.html
- [插件发布] 小爱同学TTS服务（2019年5月29日更新可用版本）：https://bbs.hassbian.com/forum.php?mod=viewthread&tid=3669&extra=&authorid=1417&page=1