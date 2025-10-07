使用和制作mod的前提:
1.删除游戏根目录内files.json和packages.json,不删除无法通过文件校验.会导致游戏启动失败
2.游戏离线,正版从steam启动项设置,学习版快捷方式后面加offline=1
3.解压cfg子目录内所有N2PK文件并删除源文件,保留解压后的cfg文件,这游戏会先读取解压后的cfg,此方法并不影响游戏运行,或者单独解压某N2PK文件后修改cfg文件重新打包N2PK替换源文件,推荐前者,因为CFG文件夹下N2PK文件很多,每个N2PK文件里面包括的CFG也很多,这里我根据github作者的单个N2PK文件解压工具自制了一键解压并打包的python程序

可以实现的功能:
1.技能倍率
关联文件:\Cfg\SkillTree\skills.cfg解压后修改value的值即可
2.主线任务奖励
关联文件
Cfg\OpenWorld\missions.cfg 此文件是UI显示的奖励
JSON\quest\meta.quest.json 此文件是实际的奖励
同时json目录下其他几个文件夹应该是DLC之类的配置文件,搜索reward有很多结果,自己对应查找修改
JSON\campaignStates\ 目录下应该是对应地图的奖励,搜索characterXp自行对应修改

JSON\shopDescriptions.json 商店刷新间隔
Cfg\Artifact\inventoryitems.cfg 商店盒子和物品属性 价格是Value和FateValue=2
Damage_reduceBonus=(0;1),(0;2),(1;3),(2;4),(3;5),(0;0)这种格式是词条最低属性和最高属性区间

Cfg\Artifact\enchantments.cfg 附魔
Values=(7;10),(8;12),(10;13),(11;15),(12;17),(13;18),(14;20),(15;22) 这种格式是附魔区间

Cfg\Config\tarotcards.cfg 塔罗牌

最后希望大家善用ai工具,免费的智谱清言,可以集成到VS code的通义千问,或者付费的chatgpt和GitHub Copilo都可以解释代码或者帮你一键生成py程序
