
import streamlit as st
import random
import json

# ─────────────────────────────────────────────────────────────
# 1. 场景数据库
# ─────────────────────────────────────────────────────────────

SCENES = {
    "CG1": {
        "title": "珞珈门（正门）预约核验处",
        "subtitle": "模糊预约码",
        "npc_name": "中年游客",
        "npc_type": "tourist_middle",
        "npc_say": "同学你好！手机刚才摔了，预约码截图变模糊了，孩子盼着看武大樱花盼了好久，你看能不能通融一下？",
        "options": {
            "A": "用预约手机号帮你查系统记录，核对上就可以入校。",
            "B": "码看不清没法核验，去旁边找安保帮忙吧。",
            "C": "先让你们进去，后面碰到巡逻保安说明下手机坏了就好。",
        },
        "results": {
            "A": ("快速查到预约信息，顺利放行。游客连声道谢，孩子笑着举起樱花玩偶。", 9),
            "B": ("游客失望离开，向排队游客抱怨流程繁琐。", -1),
            "C": ("游客途中被安保拦下劝返，你因违规放行被提醒。", -5),
        },
    },
    "CG2": {
        "title": "珞珈门",
        "subtitle": "截屏预约码",
        "npc_name": "时尚年轻人",
        "npc_type": "tourist_young",
        "npc_say": "同学，快点核验吧！我昨天截的图，肯定是有效的，没必要再打开实时界面了，太麻烦了。",
        "options": {
            "A": "截图系统不认，我帮你重新进一下预约页面，很快就好。",
            "B": "截图不行我也没办法，你在旁边弄好了再回来就行。",
            "C": "赶时间是吧，那我直接用截图扫一下，能过先让你进去。",
        },
        "results": {
            "A": ("游客配合刷新，顺利核验，队伍流畅通过。", 9),
            "B": ("游客觉得你敷衍，当众吐槽，引发排队游客议论。", -1),
            "C": ("截图过期无法核验，系统弹出异常提示，游客当场烦躁，队伍拥堵。", -5),
        },
    },
    "CG3": {
        "title": "弘毅门",
        "subtitle": "虚假预约码",
        "npc_name": "神色慌张的男子",
        "npc_type": "suspicious_man",
        "npc_say": "同学，快帮我核验一下，我预约成功了，手机有点卡，你凑活看一下，赶紧放我进去，我朋友还在里面等我。",
        "options": {
            "A": "可能真是手机卡了，你别着急，在旁边缓一会儿再试。",
            "B": "界面看着有点奇怪，我用你手机号查一下官方记录，这样最准。",
            "C": "看着问题不大，我先给你通过，你赶紧进去找朋友吧。",
        },
        "results": {
            "A": ("男子一直无法刷新，神色慌乱，最终被安保上前核查。", -1),
            "B": ("查出无预约，男子自知败露，默默离开，避免违规入校。", 9),
            "C": ("男子入校后很快被保安拦下，你因核验不严被提醒。", -5),
        },
    },
    "CG4": {
        "title": "万林二次核验",
        "subtitle": "未完成核验",
        "npc_name": "抱怨的游客",
        "npc_type": "impatient",
        "npc_say": "同学，我已经在门口核验过了，怎么还要再核验一次啊？太麻烦了，我直接进去不行吗？",
        "options": {
            "A": "行，那你直接进去吧，后面有人问就说已经核验过了。",
            "B": "流程就是两次核验，没弄完确实进不去核心区。",
            "C": "核心区管控严，再扫一次很快，也是为了里面安全。",
        },
        "results": {
            "A": ("游客入校被保安拦下复核，你因简化流程被提醒。", -5),
            "B": ("游客虽配合，但全程不满，边走边向同伴抱怨。", -1),
            "C": ("游客理解配合，顺利完成核验进入核心区。", 9),
        },
    },
    "CG5": {
        "title": "文体路口核验点",
        "subtitle": "校友未登记入校",
        "npc_name": "武大校友",
        "npc_type": "alumni",
        "npc_say": "同学，我是武大毕业的校友，回自己的母校看看樱花，还需要预约登记吗？我以前回来都不用的。",
        "options": {
            "A": "原来你是校友啊，直接进去吧～",
            "B": "特别理解回母校的心情～ 校友也需要通过官方预约系统哦。",
            "C": "不管是不是校友，都要登记核验，没有凭证就不能进。",
        },
        "results": {
            "A": ("校友道谢后进入，巡逻保安发现后告知你校友也需登记，因违规放行被提醒。", -5),
            "B": ("校友笑着点头，顺利出示登记凭证，还和你聊了几句当年在武大的时光。", 9),
            "C": ("校友脸色有些难看，叹了口气，转身去登记，语气中带着不满。", -1),
        },
    },
    "CG6": {
        "title": "珞南门（附中门）",
        "subtitle": "超额预约求助",
        "npc_name": "带父母的女孩",
        "npc_type": "young_girl",
        "npc_say": "同学，求求你了！我预约的是明天，但爸妈今天临时有空，特意从外地过来，你看能不能通融一下？",
        "options": {
            "A": "不然你们先在门口等一会儿，说不定后面会有人空出今天的名额。",
            "B": "我特别理解，只是入校名额按天核定，系统没法提前放行。",
            "C": "难得过来一趟，那你们从旁边低调进去吧，别被工作人员看到。",
        },
        "results": {
            "A": ("一家人在门口等候许久，始终没有空余名额，最终失望离去，还引来其他游客效仿围堵。", -1),
            "B": ("女孩虽有些失落，但礼貌点头，带着父母明天再来了。", 9),
            "C": ("女孩入校没多久就被巡逻保安发现并劝返，你也因违规放行被现场提醒。", -5),
        },
    },
    "CG7": {
        "title": "茶港门预约核验处",
        "subtitle": "证件与预约信息不符",
        "npc_name": "拿着家人证件的游客",
        "npc_type": "tourist_middle",
        "npc_say": "同学，不好意思，我自己没预约上，就用家人的信息预约了，证件是我的，预约信息是家人的，能不能通融？",
        "options": {
            "A": "既然是一家人，那你先进去吧。",
            "B": "系统是按身份核验的，我这边确实没法帮你操作。",
            "C": "被查到会麻烦，要不你在门口等一下，我问问值守同事。",
        },
        "results": {
            "A": ("游客入校后被安保查出人证不符，你因违规放行被提醒。", -5),
            "B": ("游客虽有点失落，但礼貌点头，准备重新预约。", 9),
            "C": ("游客在门口等候引发小范围围观，后面队伍出现拥堵。", -1),
        },
    },
    "CG8": {
        "title": "扬波门（东门）",
        "subtitle": "错过入校时间",
        "npc_name": "满头大汗的游客",
        "npc_type": "rushing",
        "npc_say": "同学，求求你了！我特意请假过来，预约了今天的名额，结果路上堵车，来晚了，能不能通融一下？",
        "options": {
            "A": "看你赶得这么辛苦，我悄悄放你进去。",
            "B": "我这边真的开不了权限，你明天再来会更顺利。",
            "C": "现在进去也快天黑了，其实门口拍拍照也挺有氛围的。",
        },
        "results": {
            "A": ("游客入校被保安劝返，你因违规被批评。", -5),
            "B": ("游客理解点头，礼貌道谢后离开。", 9),
            "C": ("游客觉得被敷衍，情绪低落，在门口徘徊抱怨。", -1),
        },
    },
    "CG9": {
        "title": "樱花大道",
        "subtitle": "摇晃樱花树",
        "npc_name": "拍照的年轻游客",
        "npc_type": "tourist_young",
        "npc_say": "你看，这样摇下来的樱花雨多好看，拍出来的照片肯定很出片，没事的，摇几下不会把树摇坏。",
        "options": {
            "A": "那你轻一点，别把树枝扯断，拍两张就好。",
            "B": "自然落下来的樱花更有氛围感，摇树反而容易伤到花枝。",
            "C": "旁边好多人在看，这样不太好看，还是停下吧。",
        },
        "results": {
            "A": ("游客继续轻摇，花枝受损，周围人纷纷效仿。", -5),
            "B": ("游客不好意思地收手，还劝阻了身边模仿的人。", 9),
            "C": ("游客觉得你多管闲事，反而故意多摇了几下。", -1),
        },
    },
    "CG10": {
        "title": "樱花大道",
        "subtitle": "折取樱花枝",
        "npc_name": "带孩子的女士",
        "npc_type": "mother",
        "npc_say": "孩子喜欢樱花，折一枝带回家当纪念，又不多折，没关系的，这么多樱花，少一枝也看不出来。",
        "options": {
            "A": "就一枝影响不大，下次别再折就好。",
            "B": "大家都折的话，树很快就秃了，还是别这样啦。",
            "C": "拍照留念会更长久，折下来很快就蔫了，也伤树。",
        },
        "results": {
            "A": ("女士不以为意离开，其他游客见状也开始折枝。", -5),
            "B": ("女士觉得你小题大做，淡淡瞥一眼便转身离开。", -1),
            "C": ("女士面露歉意，收起花枝，教孩子文明赏花。", 9),
        },
    },
    "CG11": {
        "title": "樱花大道",
        "subtitle": "踩踏草坪",
        "npc_name": "踩进草坪的游客",
        "npc_type": "tourist_middle",
        "npc_say": "我就进去拍几张照片，很快就出来，草坪这么大，踩几下没关系的，拍出来的照片会更好看。",
        "options": {
            "A": "那你快拍快出来，别在里面待太久。",
            "B": "路边有几个角度不用进草坪，拍出来也一样好看。",
            "C": "草坪踩多了会发黄，还是在路边拍更合适。",
        },
        "results": {
            "A": ("游客在草坪逗留很久，留下明显踩踏痕迹。", -5),
            "B": ("游客主动走出草坪，按你指的位置开心拍照。", 9),
            "C": ("游客不情不愿走出来，小声嘟囔但未激化矛盾。", -1),
        },
    },
    "CG12": {
        "title": "老斋舍旁",
        "subtitle": "乱扔垃圾",
        "npc_name": "乱扔垃圾的游客",
        "npc_type": "impatient",
        "npc_say": "扔个垃圾而已，反正会有保洁人员打扫，没必要这么麻烦，我还要去拍照呢。",
        "options": {
            "A": "麻烦不要乱扔垃圾哦，樱花树下的美景需要我们共同守护。",
            "B": "我帮你捡起来吧，下次可不要乱扔了，要爱护校园环境。",
            "C": "你怎么能乱扔垃圾？太没素质了！",
        },
        "results": {
            "A": ("游客连忙捡起垃圾，不好意思地道谢，跟着你到垃圾桶旁分类丢弃。", 9),
            "B": ("游客笑着说下次注意，但还是没改掉乱扔的习惯，转身又扔了一张纸巾。", -1),
            "C": ("游客脸色不悦，不仅不捡垃圾，还转身离开，影响周边游客观感。", -5),
        },
    },
    "CG13": {
        "title": "鲲鹏广场",
        "subtitle": "攀爬樱花树",
        "npc_name": "爬树的年轻男生",
        "npc_type": "tourist_young",
        "npc_say": "没事没事，我轻轻的，不会把树枝踩断的，就拍几张照片，很快就下来，你别小题大做。",
        "options": {
            "A": "等会儿保安过来，你想好好拍都拍不成了。",
            "B": "其实蹲在落花堆里拍，氛围感比爬树强十倍还安全。",
            "C": "那你拍归拍，别把花瓣摇得到处都是就行。",
        },
        "results": {
            "A": ("男生立刻不爽，故意在树上晃得更欢，还掏出手机对着你拍，引来路人看热闹。", -5),
            "B": ("男生眼睛一亮，麻溜爬下来：\"卧槽这思路可以！\" 蹲在落花里拍得不亦乐乎，还跟周围游客道了歉。", 9),
            "C": ("男生随便拍两张就下来，还是顺手抖落一地花瓣，一脸无所谓。", -1),
        },
    },
    "CG14": {
        "title": "万林艺术博物馆旁",
        "subtitle": "商业拍摄占道",
        "npc_name": "婚纱摄影师",
        "npc_type": "photographer",
        "npc_say": "我们就拍半个小时，很快就好，占用一点通道没关系，拍完我们就走，不会耽误太久。",
        "options": {
            "A": "再占着路，等下游客挤过来你们也拍不安稳。",
            "B": "你们拍你们的，给路人留条能侧身过的缝就行。",
            "C": "往坡上那棵孤樱走，没人挡，拍出来像电影截图。",
        },
        "results": {
            "A": ("摄影师翻了个白眼，故意放慢速度，摆明了跟你对着来。", -5),
            "B": ("摄影师随便应了声，依旧占着大半路，后面游客越积越多开始抱怨。", -1),
            "C": ("摄影师当场眼睛放光，立刻收道具转场，效率极高还特别客气。", 9),
        },
    },
    "CG15": {
        "title": "樱花大道",
        "subtitle": "网络直播扰序",
        "npc_name": "带手机的主播",
        "npc_type": "streamer",
        "npc_say": "我就是开个直播，带大家看看武大的樱花，又没做什么坏事，声音大一点怎么了？拉游客入镜也是为了效果。",
        "options": {
            "A": "轻声慢语讲樱花故事，观众反而更愿意留下来听。",
            "B": "别突然拽路人就行，人家大多不想出镜。",
            "C": "你再这么喊，等下被投诉的可是你自己。",
        },
        "results": {
            "A": ("主播愣了下，笑着调低音量，顺便在直播间纠正了预约信息，氛围舒服很多。", 9),
            "B": ("主播随口答应，还是忍不住凑近路人拍，好几个游客被吓得赶紧躲开。", -1),
            "C": ("主播当场不爽，对着镜头阴阳怪气吐槽你，现场瞬间围了一圈人。", -5),
        },
    },
    "CG16": {
        "title": "珞珈山庄旁",
        "subtitle": "露营搭帐篷",
        "npc_name": "露营的游客",
        "npc_type": "camper",
        "npc_say": "我们就是在草坪上露营一晚，明天一早就走，不会损坏草坪，也不会影响其他人，没关系的。",
        "options": {
            "A": "校园不让露营，被查到你们今晚都歇不好。",
            "B": "旁边休息区有长椅，铺个垫子坐一夜比草坪舒服还不违规。",
            "C": "那你们吃完记得把垃圾全装袋，别留在这儿。",
        },
        "results": {
            "A": ("游客满脸不爽，一边收拾一边大声抱怨，还带动旁边人一起起哄，场面尴尬。", -5),
            "B": ("游客一拍脑袋，麻利收拾干净，开开心心换地方休息。", 9),
            "C": ("游客满口答应，结果夜里垃圾扔得到处都是，草坪被压出印子，第二天被保洁投诉。", -1),
        },
    },
    "CG17": {
        "title": "樱花大道",
        "subtitle": "情侣求帮忙拍照",
        "npc_name": "幸福情侣",
        "npc_type": "couple",
        "npc_say": "同学，麻烦你啦！我们来武大赏樱，想拍张合影留作纪念，你能帮我们拍一张吗？尽量把樱花和我们都拍进去～",
        "options": {
            "A": "前面有不少游客，你可以问问他们方不方便帮忙。",
            "B": "我这边还要看着人流，你们用自拍杆可能会更方便些。",
            "C": "好呀，我帮你们找个好看的角度，多拍几张也没关系！",
        },
        "results": {
            "A": ("情侣在人群里犹豫很久，最终只匆匆拍了几张单人照便离开了。", -1),
            "B": ("情侣默默拿出手机自拍，姿势有些局促，带着小遗憾离开。", -5),
            "C": ("你耐心帮他们定格好几个瞬间，两人看着照片连连道谢，氛围温柔又明亮。\n🌸【解锁特殊成就：樱花见证者】", 9),
        },
        "special": {"C": "樱花见证者"},
    },
    "CG19": {
        "title": "樱花大道旁",
        "subtitle": "摆摊售卖",
        "npc_name": "商贩",
        "npc_type": "vendor",
        "npc_say": "我就摆一会儿摊，卖一点小东西，赚点零花钱，不会占用太久通道，也不会乱扔垃圾，你就让我摆一会儿吧。",
        "options": {
            "A": "那你尽量快一点，别让巡逻的工作人员看到。",
            "B": "这边人多容易堵，我帮你找个不挡路的位置吧。",
            "C": "这里不能摆摊，再继续我只能请你离开了。",
        },
        "results": {
            "A": ("商贩连忙答应，却还是逗留许久，垃圾越丢越多，最终引来游客投诉。", -1),
            "B": ("商贩松了口气，挪到开阔处，收拾干净地面，安静做完几笔生意便自觉离开。", 9),
            "C": ("商贩立刻皱起眉，觉得你态度生硬，故意慢吞吞收拾东西，引发路人侧目。", -5),
        },
    },
    "CG20": {
        "title": "鲲鹏广场",
        "subtitle": "放飞无人机",
        "npc_name": "持无人机的男子",
        "npc_type": "tourist_young",
        "npc_say": "我就是放飞无人机拍几张樱花全景照片，又不会伤到别人，学校没必要管这么严吧！",
        "options": {
            "A": "人流密集无人机失控后果严重，我帮您推荐几个绝佳地面全景机位。",
            "B": "航拍效果确实震撼，只要避开人群和建筑，简单飞一会儿应该没问题。",
            "C": "规定就是规定，校园里禁止飞行器升空，再坚持只能上报处理。",
        },
        "results": {
            "A": ("男子点头致歉，收好无人机，主动离开，未引发任何混乱。", 9),
            "B": ("无人机升空后信号不稳，险些砸中游客，被巡逻保安当场控制。", -1),
            "C": ("男子瞬间不满，故意开机示威，引来大量游客围观，严重扰乱秩序。", -5),
        },
    },
    "CG21": {
        "title": "樱花大道",
        "subtitle": "散发商业传单",
        "npc_name": "发传单的男子",
        "npc_type": "vendor",
        "npc_say": "我就发点宣传页，又不挡路，捡起来不就行了？",
        "options": {
            "A": "商业传单未经许可，我们一起把散落的纸张收好，我帮您指引到允许宣传的区域。",
            "B": "发传单没关系，但别随意乱扔影响环境，也别堵在路口就好。",
            "C": "这里禁止任何商业宣传行为，继续发放我只能联系安保人员。",
        },
        "results": {
            "A": ("男子立刻停止发放，弯腰捡起传单，连声道歉后快速离开。", 9),
            "B": ("男子更加随意，传单扔得到处都是，加重保洁负担，引来游客效仿。", -1),
            "C": ("男子当场顶撞争吵，引发路人围观，现场秩序混乱。", -5),
        },
    },
    "CG22": {
        "title": "核心区禁行路段",
        "subtitle": "游客强行闯入",
        "npc_name": "想闯入的游客",
        "npc_type": "impatient",
        "npc_say": "我就进去看一眼，拍张照就走，又不捣乱，通融一下！",
        "options": {
            "A": "武大最美的樱花都在开放步道里，我带您去几处人少又绝美的机位，比校内更出片哦。",
            "B": "这里是同学们日常作息的地方，多一份安静，也是给樱花多一份温柔呀。",
            "C": "再往前就属于非游览区域了，为了您的安全，请遵守园区参观路线。",
        },
        "results": {
            "A": ("游客眼前一亮，欣然跟着前往新点位，拍到更惊艳的景致，连连道谢。", 9),
            "B": ("游客有些不好意思，虽略有遗憾，但还是主动退了回去。", -1),
            "C": ("游客脸色一沉，不满地嘀咕，转身时还向旁人抱怨，影响周围游客观感。", -5),
        },
    },
    "CG23": {
        "title": "樱花大道",
        "subtitle": "扎堆占道拍照",
        "npc_name": "拍大合照的游客群",
        "npc_type": "group",
        "npc_say": "我们拍个大合照，等几分钟怎么了？出来玩还不能拍照了？",
        "options": {
            "A": "人挤在路中间反而放不开，旁边那片樱花林空阔又好看，拍团体照氛围感直接拉满。",
            "B": "大家难得合影，只是这条路来往人多，稍微快一点，后面的游客也能少等一会儿。",
            "C": "道路中间人流密集，既不安全也影响通行，还请大家移步到安全区域拍摄。",
        },
        "results": {
            "A": ("游客一听立刻心动，主动让出通道，开心前往更佳位置拍摄。", 9),
            "B": ("游客敷衍点头，却依旧不紧不慢摆姿势，道路持续拥堵，后方游客怨声渐起。", -1),
            "C": ("游客立刻面露不悦，当场反驳争执，引来大量围观，场面变得尴尬紧张。", -5),
        },
    },
    "CG25": {
        "title": "樱花大道",
        "subtitle": "孩童与家长走失",
        "npc_name": "迷路的小朋友",
        "npc_type": "child",
        "npc_say": "呜呜...... 我找不到爸爸妈妈了......（攥着樱花玩偶，泪眼汪汪）",
        "options": {
            "A": "不哭不哭，这里人多容易走散，我牵着你去安保室，用广播帮你找到家人。",
            "B": "我需要值守岗位不能离开，前面不远处有服务点，你可以去那里寻求帮助。",
            "C": "你先在原地安心等候，我会留意周边情况，也会请巡逻人员多关注这边。",
        },
        "results": {
            "A": ("小朋友情绪稳定下来，很快与父母重逢，一家人连连向你道谢。", 9),
            "B": ("小朋友独自走向陌生人群，内心更加恐惧，在路边慌乱徘徊。", -1),
            "C": ("小朋友长时间无人陪伴，越哭越凶，最终由安保人员介入处理。", -5),
        },
    },
    "CG27": {
        "title": "老斋舍",
        "subtitle": "考研学子贴祈福便签",
        "npc_name": "备考的学生",
        "npc_type": "student",
        "npc_say": "我就贴一张求好运，不会弄坏树皮的......（手里攥着便签）",
        "options": {
            "A": "不必依附树木，你的努力本身，就是最好的祈福。",
            "B": "记得贴稳一些，别轻易被风吹掉了。",
            "C": "请不要在树木上随意张贴，这是对校园环境的保护。",
        },
        "results": {
            "A": ("学生感动道谢，主动收起便签，满怀信心离开，专心备考。", 9),
            "B": ("便签被风吹落，树皮残留胶痕，破坏校园环境。", -1),
            "C": ("学生沮丧撕掉便签，情绪低落，影响备考状态。", -5),
        },
    },
    "CG28": {
        "title": "核验口",
        "subtitle": "老人不会使用智能手机预约",
        "npc_name": "白发老人",
        "npc_type": "elderly",
        "npc_say": "孩子，我年纪大了不会弄手机，就想看看樱花，你帮帮我吧......（拄着拐杖）",
        "options": {
            "A": "爷爷您别着急，我慢慢帮您登记预约，咱们走绿色通道，我送您进去赏樱。",
            "B": "进园需要线上预约，我帮您点开页面，您按照提示填写信息就可以了。",
            "C": "我帮您用手机预约一下，您确认后就可以直接进园了。",
        },
        "results": {
            "A": ("老人激动道谢，全程安心入园赏樱，贴心规范的服务受到认可（敬老服务考核合格）。", 9),
            "B": ("老人面对复杂操作仍难以独立完成，在核验口旁不知所措。", -1),
            "C": ("被现场工作人员提醒，代预约存在信息安全隐患，需按正规流程服务。", -5),
        },
    },
    "CG29": {
        "title": "值守点",
        "subtitle": "志愿者同伴中暑",
        "npc_name": "中暑的同伴",
        "npc_type": "volunteer",
        "npc_say": "我头好晕...... 有点撑不住了......（站立不稳，脸色苍白）",
        "options": {
            "A": "快到阴凉处坐下，松松衣服透透气，喝点淡盐水，我马上叫负责人过来。",
            "B": "到这边凉快一下，我用湿毛巾给你擦擦，先不要乱吃药。",
            "C": "吃点解暑药会好得快，你侧躺着休息一下。",
        },
        "results": {
            "A": ("同伴很快舒缓过来，负责人对你规范的急救处理表示肯定（应急急救知识考核合格）。", 9),
            "B": ("同伴体感有所好转，但因未补充电解质，恢复不够彻底。（处置基本正确）", -1),
            "C": ("同伴出现轻微肠胃不适，被医护人员提醒不可随意用药。", -5),
        },
    },
    "CG30": {
        "title": "樱花大道",
        "subtitle": "游客遗失贵重物品",
        "npc_name": "焦急的中年游客",
        "npc_type": "rushing",
        "npc_say": "同学，我相机掉在这附近了，银黑色的，里面全是我和家人的樱花合影，对我特别重要！你有没有看到啊？",
        "options": {
            "A": "我暂时没注意到，您先别着急，我陪您沿刚才走过的路线往回仔细找一遍。",
            "B": "我好像看到有人捡到东西，您在这儿等一会儿，我去问问附近的值守同学。",
            "C": "这边人这么多，估计很难找到了，要不您直接去安保点登记挂失吧。",
        },
        "results": {
            "A": ("你陪着游客细心沿路寻找，很快在樱树底下找到了相机，游客激动不已，送上樱花文创表示感谢。\n🎁【获得樱花文创纪念品】", 9),
            "B": ("你离开后并没有问到有效信息，游客独自等待许久越发焦虑，最后自己找回相机，但对你略有不满。", -1),
            "C": ("游客觉得你敷衍了事，十分失望地前往安保处，途中不断向其他游客抱怨。", -5),
        },
    },
    # 以下三个场景全0分，选项分数均为0
    "CG18": {
        "title": "樱花大道",
        "subtitle": "毕业生回校怀旧",
        "npc_name": "怀旧的毕业生",
        "npc_type": "alumni",
        "npc_say": "好久没回来了...... 就想安安静静站一会儿，找找当年的感觉，不会破坏花草的......",
        "options": {
            "A": "这里人来人往，站在路边会有点挤哦。",
            "B": "风大花枝晃，靠近一点反而容易被碰到。",
            "C": "慢慢看吧，难得回来一次，不用着急。",
        },
        "results": {
            "A": ("男生默默往边上挪了挪，没再久留，简单拍了两张照片便匆匆离去。", 0),
            "B": ("男生收回伸出的手，有些失落地点点头，转身离开时频频回头。", 0),
            "C": ("男生轻轻点头，眼底泛起暖意，安静站了许久才轻声离开，背影里满是温柔的怀念。", 0),
        },
    },
    "CG24": {
        "title": "樱花大道",
        "subtitle": "汉服女生花粉过敏",
        "npc_name": "穿汉服的女生",
        "npc_type": "hanfu_girl",
        "npc_say": "好不容易穿汉服来一次，我真的不想就这么走掉...... （频频打喷嚏，眼睛泛红）",
        "options": {
            "A": "樱花花粉浓度较高，稍微退远一些，或许能在不影响拍照的前提下舒服一点。",
            "B": "过敏反应不会自己消退，不如先到开阔处缓解，等状态好些再感受樱花也不迟。",
            "C": "美景值得记录，但身体更值得温柔对待，我陪你找一处安静又好看的地方慢慢取景。",
        },
        "results": {
            "A": ("女生坚持留在近处，过敏愈发明显，全程带着不适勉强拍照。", 0),
            "B": ("女生虽及时离开缓解了症状，却因没能尽兴赏花而心存遗憾。", 0),
            "C": ("女生安心舒缓，在更合适的位置完成拍摄，对你的细心十分感激。", 0),
        },
    },
    "CG26": {
        "title": "万林旁",
        "subtitle": "外国游客不懂预约规则",
        "npc_name": "外国游客",
        "npc_type": "foreigner",
        "npc_say": "（英语）I want to see cherry blossoms, but I don't know how to enter...",
        "options": {
            "A": "礼貌示意预约流程，鼓励对方尝试自行对照操作。",
            "B": "体谅对方沟通不易，耐心引导至专人服务点妥善安置。",
            "C": "主动上前温和安抚，用简单英文与手势全程协助完成预约。",
        },
        "results": {
            "A": ("游客因语言隔阂仍感困惑，独自在入口处反复尝试，焦急无措。", 0),
            "B": ("游客虽被妥善安排，但因全程沟通有限，依旧带着些许不安离开。", 0),
            "C": ("外国游客放下焦虑顺利入校，频频挥手称赞志愿者温暖专业。", 0),
        },
    },
}

SPECIAL_POOL = ["CG17", "CG25", "CG28", "CG29", "CG30"]
NEUTRAL_POOL = ["CG18", "CG24", "CG26"]
COMMON_POOL = [
    "CG1","CG2","CG3","CG4","CG5","CG6","CG7","CG8",
    "CG9","CG10","CG11","CG12","CG13","CG14","CG15","CG16",
    "CG19","CG20","CG21","CG22","CG23","CG27",
]

RANKS = [
    (95, "樱守至尊", "樱雪满城心不负，丹心守得珞珈春", "🏆"),
    (85, "珞珈忠卫", "温情引路明规礼，志愿春风暖客心", "🌸"),
    (75, "芳华锐士", "挺身护景承风骨，敢为先锋守芳华", "⚔️"),
    (65, "文明礼士", "一言一行遵公约，文明相伴赏樱来", "📜"),
    (60, "守樱新辈", "初心已具犹须进，勤习规章再启程", "🌱"),
    (0,  "砺心者",   "守樱之志尚需勉，重整行装再向前",  "💪"),
]

# NPC 外观配置
NPC_STYLES = {
    "tourist_middle": {"head": "#f0c8a0", "body": "#3a6ab4", "legs": "#2a4a90", "icon": "🧳"},
    "tourist_young":  {"head": "#f5b87a", "body": "#c85020", "legs": "#882000", "icon": "📸"},
    "suspicious_man": {"head": "#d8c890", "body": "#556655", "legs": "#334433", "icon": "❓"},
    "impatient":      {"head": "#e8c090", "body": "#885522", "legs": "#663311", "icon": "😤"},
    "alumni":         {"head": "#d4b880", "body": "#8b2252", "legs": "#5a1535", "icon": "🎓"},
    "young_girl":     {"head": "#f8d0b0", "body": "#d060a0", "legs": "#a04080", "icon": "💕"},
    "mother":         {"head": "#f0c8a0", "body": "#d08040", "legs": "#a05020", "icon": "👶"},
    "rushing":        {"head": "#e8c090", "body": "#505090", "legs": "#303070", "icon": "💦"},
    "photographer":   {"head": "#d8c8b0", "body": "#303030", "legs": "#202020", "icon": "📷"},
    "streamer":       {"head": "#f0b8a0", "body": "#cc4488", "legs": "#992266", "icon": "📱"},
    "camper":         {"head": "#d8d0a0", "body": "#4a8a4a", "legs": "#2a6a2a", "icon": "⛺"},
    "couple":         {"head": "#f0c8c8", "body": "#a040a0", "legs": "#702070", "icon": "💐"},
    "vendor":         {"head": "#d8b880", "body": "#8b6030", "legs": "#5a3015", "icon": "🛍️"},
    "group":          {"head": "#e8c8a0", "body": "#507090", "legs": "#304060", "icon": "👥"},
    "hanfu_girl":     {"head": "#f8d0c0", "body": "#c03060", "legs": "#802040", "icon": "🌸"},
    "child":          {"head": "#f8d8a0", "body": "#e08020", "legs": "#b06010", "icon": "🧸"},
    "foreigner":      {"head": "#f0c080", "body": "#2060a0", "legs": "#104070", "icon": "🌍"},
    "student":        {"head": "#d8c890", "body": "#404080", "legs": "#202060", "icon": "📚"},
    "elderly":        {"head": "#d0b890", "body": "#808080", "legs": "#505050", "icon": "🦯"},
    "volunteer":      {"head": "#f0c8a0", "body": "#cc2222", "legs": "#881111", "icon": "🤝"},
}


def draw_levels():
    keep_special = min(4, len(SPECIAL_POOL))
    keep_neutral = min(1, len(NEUTRAL_POOL))
    keep_common = min(10, len(COMMON_POOL))

    special = random.sample(SPECIAL_POOL, keep_special)
    neutral = random.sample(NEUTRAL_POOL, keep_neutral)
    common  = random.sample(COMMON_POOL, keep_common)
    pool = special + neutral + common

    if len(pool) < 15:
        remaining = list(set(SCENES.keys()) - set(pool))
        random.shuffle(remaining)
        pool += remaining[:15 - len(pool)]

    random.shuffle(pool)
    return pool


def validate_scene_pools():
    all_scene_ids = set(SCENES.keys())
    pool_ids = set(SPECIAL_POOL) | set(NEUTRAL_POOL) | set(COMMON_POOL)
    if all_scene_ids != pool_ids:
        missing = sorted(list(all_scene_ids - pool_ids))
        extra = sorted(list(pool_ids - all_scene_ids))
        msg = []
        if missing:
            msg.append(f"SCENES 中存在但未纳入池的场景：{', '.join(missing)}")
        if extra:
            msg.append(f"池中存在但 SCENES 未定义的场景：{', '.join(extra)}")
        st.warning('；'.join(msg))

    duplicates = [item for item in SPECIAL_POOL + NEUTRAL_POOL + COMMON_POOL
                  if (SPECIAL_POOL + NEUTRAL_POOL + COMMON_POOL).count(item) > 1]
    if duplicates:
        dup_list = sorted(set(duplicates))
        st.warning(f"场景池中存在重复项：{', '.join(dup_list)}")


def get_rank(score, stats=None):
    # 如果有统计数据，根据正确率和平均分微调等级
    if stats:
        accuracy = stats['accuracy']
        avg_score = stats['avg_score']
        
        # 基于正确率和平均分的综合评分
        performance_score = score + (accuracy - 50) * 0.5 + (avg_score - 2) * 2
        
        # 查找最合适的等级
        for threshold, title, poem, emoji in RANKS:
            if performance_score >= threshold:
                return title, poem, emoji
        return RANKS[-1][1], RANKS[-1][2], RANKS[-1][3]
    else:
        # 原始逻辑
        for threshold, title, poem, emoji in RANKS:
            if score >= threshold:
                return title, poem, emoji
        return RANKS[-1][1], RANKS[-1][2], RANKS[-1][3]


def calculate_stats(history):
    """计算游戏统计数据"""
    total_scenes = len(history)
    total_score = sum(delta for _, _, delta, _ in history)
    positive_choices = sum(1 for _, _, delta, _ in history if delta > 0)
    negative_choices = sum(1 for _, _, delta, _ in history if delta < 0)
    neutral_choices = sum(1 for _, _, delta, _ in history if delta == 0)
    
    accuracy = (positive_choices / total_scenes * 100) if total_scenes > 0 else 0
    avg_score = total_score / total_scenes if total_scenes > 0 else 0
    
    return {
        "total_scenes": total_scenes,
        "total_score": total_score,
        "positive_choices": positive_choices,
        "negative_choices": negative_choices,
        "neutral_choices": neutral_choices,
        "accuracy": accuracy,
        "avg_score": avg_score
    }


def init_state():
    defaults = {
        "started": False,
        "levels": [],
        "current": 0,
        "score": 0,
        "history": [],
        "achievements": [],
        "phase": "question",
        "last_choice": None,
        "npc_anim": "enter",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def start_game():
    st.session_state.levels = draw_levels()
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.achievements = []
    st.session_state.phase = "question"
    st.session_state.last_choice = None
    st.session_state.npc_anim = "enter"
    st.session_state.started = True


def choose(option):
    idx = st.session_state.current
    cg_id = st.session_state.levels[idx]
    scene = SCENES[cg_id]
    result_text, delta = scene["results"][option]
    st.session_state.score += delta
    st.session_state.history.append((cg_id, option, delta, result_text))
    if "special" in scene and option in scene["special"]:
        ach = scene["special"][option]
        if ach not in st.session_state.achievements:
            st.session_state.achievements.append(ach)
    
    # 添加后续逻辑：根据选择和结果提供额外反馈
    feedback = generate_feedback(option, delta, scene)
    st.session_state.last_choice = (option, result_text + feedback, delta)
    st.session_state.phase = "result"
    st.session_state.npc_anim = "idle"


def generate_feedback(option, delta, scene):
    """根据选择和结果生成额外反馈"""
    feedback = ""
    
    if delta > 0:
        if option == "A":
            feedback = "\n\n💡 **志愿小贴士**：你的选择体现了专业素养，继续保持！"
        else:
            feedback = "\n\n💡 **志愿小贴士**：虽然得分，但还有更优的选择，下次注意细节。"
    elif delta < 0:
        if option == "A":
            feedback = "\n\n💡 **志愿小贴士**：看似正确，但实际操作中需更谨慎。"
        else:
            feedback = "\n\n💡 **志愿小贴士**：这个选择可能带来不良影响，建议学习相关规定。"
    else:
        feedback = "\n\n💡 **志愿小贴士**：中性选择，有时也需要灵活处理。"
    
    # 根据场景类型添加特定反馈
    scene_type = scene.get("npc_type", "")
    if "child" in scene_type:
        feedback += "\n\n👶 **儿童安全提醒**：涉及儿童时，安全第一，及时求助专业人员。"
    elif "elderly" in scene_type:
        feedback += "\n\n🦯 **敬老服务提醒**：老人服务需耐心细致，考虑他们的实际困难。"
    elif "tourist" in scene_type:
        feedback += "\n\n🧳 **游客服务提醒**：文明引导，维护校园形象。"
    
    return feedback


def next_scene():
    st.session_state.current += 1
    st.session_state.phase = "question"
    st.session_state.last_choice = None
    st.session_state.npc_anim = "enter"


def build_npc_svg(npc_type, size=120):
    """生成 NPC 的 SVG 内联图形 - 增强版本"""
    style = NPC_STYLES.get(npc_type, NPC_STYLES.get("tourist_middle", {
        "head": "#f0c8a0",
        "body": "#3a6ab4",
        "legs": "#2a4a90",
        "icon": "🧳",
    }))
    hc = style["head"]
    bc = style["body"]
    lc = style["legs"]
    icon = style["icon"]
    cx = size // 2

    # 根据类型微调比例
    is_child = npc_type == "child"
    is_elderly = npc_type == "elderly"
    head_r = 16 if is_child else 18
    body_h = 36 if is_child else (40 if is_elderly else 44)
    leg_h  = 22 if is_child else (26 if is_elderly else 30)
    body_w = 28 if is_child else 34
    body_y = 22 + head_r * 2
    leg_y  = body_y + body_h
    
    # 计算光线高亮和阴影
    highlight_r = head_r - 6

    # 配件
    accessory = ""
    hair_style = ""
    
    if npc_type == "elderly":
        # 拐杖
        accessory = f'<line x1="{cx+20}" y1="{body_y+10}" x2="{cx+22}" y2="{leg_y+leg_h}" stroke="#888" stroke-width="3" stroke-linecap="round"/>'
        # 白发
        hair_style = f'<ellipse cx="{cx}" cy="{18+head_r}" rx="{head_r+1}" ry="10" fill="#e0e0e0" opacity="0.6"/>'
    elif npc_type == "photographer":
        # 相机
        accessory = f'<rect x="{cx+16}" y="{body_y+5}" width="18" height="13" rx="3" fill="#222" filter="drop-shadow(0 2px 2px rgba(0,0,0,0.2))"/><rect x="{cx+19}" y="{body_y+8}" width="7" height="7" rx="3.5" fill="#555"/>'
        # 头发
        hair_style = f'<path d="M{cx-head_r} {20+head_r} A{head_r} {head_r} 0 0 1 {cx+head_r} {20+head_r}" fill="#333" opacity="0.3"/>'
    elif npc_type == "child":
        # 玩偶
        accessory = f'<circle cx="{cx-20}" cy="{body_y+8}" r="10" fill="#ffb3cc" opacity="0.9" filter="drop-shadow(0 2px 3px rgba(0,0,0,0.15))"/><circle cx="{cx-20}" cy="{body_y+4}" r="6" fill="#ffd0e0"/>'

    # 计算头部高光颜色（基于肤色）
    if hc in ["#ffc0a0", "#ffb080", "#f0c8a0", "#f5b87a"]:  # 皮肤色
        highlight_color = "#ffe8d0"
    else:
        highlight_color = "#ffffff"
    
    # NPC特殊头部设计
    head_decoration = ""
    if npc_type == "student":
        # 学生的眼镜
        head_decoration = f'<circle cx="{cx-6}" cy="{19+head_r}" r="4" fill="none" stroke="#666" stroke-width="1"/><circle cx="{cx+6}" cy="{19+head_r}" r="4" fill="none" stroke="#666" stroke-width="1"/><line x1="{cx-2}" y1="{19+head_r}" x2="{cx+2}" y2="{19+head_r}" stroke="#666" stroke-width="1"/>'
    elif npc_type == "young_girl":
        # 少女发夹
        girl_hair_x1 = cx - head_r + 2
        girl_hair_x2 = cx + head_r - 2
        head_decoration = f'<circle cx="{girl_hair_x1}" cy="{12}" r="3" fill="#ff99cc"/><circle cx="{girl_hair_x2}" cy="{12}" r="3" fill="#ff99cc"/>'

    svg = f"""<svg width="{size}" height="{size+20}" viewBox="0 0 {size} {size+20}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="shadow_g" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#000" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="head_light" cx="35%" cy="35%" r="60%">
      <stop offset="0%" stop-color="{highlight_color}" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="{highlight_color}" stop-opacity="0"/>
    </radialGradient>
    <filter id="soft-shadow">
      <feGaussianBlur in="SourceGraphic" stdDeviation="1.5"/>
    </filter>
  </defs>
  
  <!-- 阴影 -->
  <ellipse cx="{cx}" cy="{leg_y+leg_h+6}" rx="24" ry="8" fill="url(#shadow_g)"/>
  
  <!-- 腿部 -->
  <rect x="{cx-16}" y="{leg_y}" width="13" height="{leg_h}" rx="5" fill="{lc}" filter="url(#soft-shadow)"/>
  <rect x="{cx+3}"  y="{leg_y}" width="13" height="{leg_h}" rx="5" fill="{lc}" filter="url(#soft-shadow)"/>
  <!-- 脚部 -->
  <ellipse cx="{cx-9.5}" cy="{leg_y+leg_h+2}" rx="7" ry="4" fill="#333" opacity="0.3"/>
  <ellipse cx="{cx+9.5}" cy="{leg_y+leg_h+2}" rx="7" ry="4" fill="#333" opacity="0.3"/>
  
  <!-- 身体 -->
  <rect x="{cx-body_w//2}" y="{body_y}" width="{body_w}" height="{body_h}" rx="6" fill="{bc}" filter="url(#soft-shadow)"/>
  <!-- 身体渐变 - 增加立体感 -->
  <rect x="{cx-body_w//2}" y="{body_y}" width="{body_w//4}" height="{body_h}" rx="6" fill="white" opacity="0.1"/>
  
  <!-- 手臂 -->
  <rect x="{cx-body_w//2-10}" y="{body_y+5}" width="10" height="{body_h-15}" rx="5" fill="{bc}" filter="url(#soft-shadow)"/>
  <rect x="{cx+body_w//2}"    y="{body_y+5}" width="10" height="{body_h-15}" rx="5" fill="{bc}" filter="url(#soft-shadow)"/>
  <!-- 手部 -->
  <circle cx="{cx-body_w//2-10}" cy="{body_y+body_h-15}" r="4" fill="{hc}" opacity="0.8"/>
  <circle cx="{cx+body_w//2+10}" cy="{body_y+body_h-15}" r="4" fill="{hc}" opacity="0.8"/>
  
  <!-- 配件 -->
  {accessory}
  
  <!-- 头部 -->
  <circle cx="{cx}" cy="{20+head_r}" r="{head_r}" fill="{hc}" filter="url(#soft-shadow)"/>
  
  <!-- 头发 -->
  {hair_style}
  
  <!-- 头部特殊装饰 -->
  {head_decoration}
  
  <!-- 头部高光 -->
  <circle cx="{cx}" cy="{20+head_r}" r="{head_r}" fill="url(#head_light)"/>
  
  <!-- 眼睛 -->
  <circle cx="{cx-5}" cy="{19+head_r}" r="2.5" fill="#333"/>
  <circle cx="{cx+5}" cy="{19+head_r}" r="2.5" fill="#333"/>
  <circle cx="{cx-4}" cy="{18+head_r}" r="1.2" fill="white"/>
  <circle cx="{cx+6}" cy="{18+head_r}" r="1.2" fill="white"/>
  
  <!-- 微笑（改进） -->
  <path d="M{cx-5},{24+head_r} Q{cx},{27+head_r} {cx+5},{24+head_r}" stroke="#555" stroke-width="1.5" fill="none" stroke-linecap="round"/>
  
  <!-- 图标徽章 -->
  <circle cx="{cx+head_r-2}" cy="{16}" r="10" fill="white" opacity="0.95" filter="drop-shadow(0 2px 3px rgba(0,0,0,0.2))"/>
  <text x="{cx+head_r-2}" y="20" font-size="11" font-weight="bold" text-anchor="middle" dominant-baseline="middle" fill="#333">{icon}</text>
</svg>"""
    return svg


def build_game_html(scene_data, score, current, total, phase, last_choice, achievements):
    """构建完整的游戏画面 HTML"""

    npc_svg = build_npc_svg(scene_data["npc_type"])
    npc_svg_b64 = npc_svg  # 直接内联

    # 根据阶段构建底部内容
    if phase == "question":
        # 只显示对话框，选项按钮移到画面下方的 Streamlit 按钮
        bottom_content = f"""
        <div class="dialog-box">
          <div class="npc-name">{scene_data['npc_name']}</div>
          <div class="dialog-text">"{scene_data['npc_say']}"</div>
        </div>
        """
    else:
        option, result_text, delta = last_choice
        sign = "+" if delta > 0 else ""
        if delta > 0:
            score_cls = "score-pos"
            if delta >= 8:
                label = f"🌟 优秀表现！  {sign}{delta} 分"
            elif delta >= 5:
                label = f"✅ 做得很好！  {sign}{delta} 分"
            else:
                label = f"👍 基本正确  {sign}{delta} 分"
        elif delta < 0:
            score_cls = "score-neg"
            if delta <= -5:
                label = f"❌ 严重失误  {sign}{delta} 分"
            else:
                label = f"⚠️ 有待改进  {sign}{delta} 分"
        else:
            score_cls = "score-neu"
            label = f"📌 特殊记录  ±0 分"

        ach_html = ""
        if achievements:
            last_ach = achievements[-1]
            ach_html = f'<div class="ach-badge">🏅 解锁成就：{last_ach}</div>'

        is_last = current >= total - 1
        next_label = "📊 查看最终报告" if is_last else "下一位游客 →"

        bottom_content = f"""
        <div class="result-box">
          <div class="result-text">{result_text.replace(chr(10), '<br>')}</div>
          <div class="result-score {score_cls}">{label}</div>
          {ach_html}
        </div>
        """

    anim_class = "npc-enter" if phase == "question" else "npc-idle"

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600&family=Noto+Sans+SC:wght@400;500&display=swap');

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: transparent; font-family: 'Noto Sans SC', sans-serif; }}

  .game-frame {{
    position: relative;
    width: 100%;
    height: 560px;
    overflow: hidden;
    border-radius: 16px;
    background: #fde9f3;
    box-shadow: 0 8px 32px rgba(220, 100, 180, 0.25), inset 0 1px 2px rgba(255, 255, 255, 0.5);
  }}

  /* ── 背景层 ── */
  .bg-sky {{
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 100% 80% at 50% -5%, #ffb3d9cc 0%, #ffc4df 20%, transparent 65%),
                linear-gradient(180deg, #ffd6ee 0%, #ffcee7 20%, #ffc4df 35%, #ffb5d5 55%, #ffa8ce 72%, #ff99c4 88%, #ff88b8 100%);
  }}
  
  /* 光晕效果 */
  .bg-sky::before {{
    content: '';
    position: absolute;
    top: -20%;
    left: 50%;
    transform: translateX(-50%);
    width: 150%;
    height: 150%;
    background: radial-gradient(circle, rgba(255, 200, 220, 0.15) 0%, transparent 60%);
    pointer-events: none;
  }}

  /* ── SVG 樱花树 ── */
  .bg-trees {{
    position: absolute; inset: 0;
    pointer-events: none;
    opacity: 0.85;
  }}

  /* ── 地面 ── */
  .ground {{
    position: absolute; bottom: 0; left: 0; right: 0; height: 135px;
    background: linear-gradient(180deg, #ffb3d5 0%, #ffa3ca 45%, #ff99c3 70%, #ff89b8 100%);
    box-shadow: inset 0 4px 12px rgba(200, 80, 140, 0.2), 0 -4px 8px rgba(200, 100, 150, 0.15);
  }}
  .ground::after {{
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, transparent 0%, #ffb5cc99 20%, #ffccdd 50%, #ffb5cc99 80%, transparent 100%);
    box-shadow: 0 2px 4px rgba(255, 150, 200, 0.3);
  }}
  
  .ground::before {{
    content: '';
    position: absolute; bottom: 5%; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent 0%, #ff88b088 35%, #ff99bb99 50%, #ff88b088 65%, transparent 100%);
    opacity: 0.6;
  }}

  /* ── 石板路透视 ── */
  .path {{
    position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
    width: 0; height: 0;
    border-left: 130px solid transparent;
    border-right: 130px solid transparent;
    border-bottom: 130px solid rgba(180, 140, 120, 0.28);
    filter: drop-shadow(0 4px 8px rgba(150, 80, 120, 0.15));
  }}

  /* ── 飘落花瓣 ── */
  .petal {{
    position: absolute;
    border-radius: 50%;
    pointer-events: none;
    animation: petalFall linear infinite;
    opacity: 0;
    will-change: transform, opacity;
    filter: drop-shadow(0 2px 3px rgba(200, 100, 150, 0.2));
  }}
  
  @keyframes petalFall {{
    0%   {{ opacity: 0;   transform: translateY(0) translateX(0) rotate(0deg) scale(0.8); }}
    5%   {{ opacity: 0.8; }}
    10%  {{ transform: translateY(60px) translateX(-15px) rotate(15deg) scale(1); }}
    25%  {{ transform: translateY(140px) translateX(20px) rotate(90deg) scale(1.05); }}
    40%  {{ transform: translateY(240px) translateX(-25px) rotate(180deg) scale(1); }}
    55%  {{ transform: translateY(350px) translateX(30px) rotate(270deg) scale(1.05); }}
    70%  {{ transform: translateY(460px) translateX(-20px) rotate(360deg) scale(1); opacity: 0.7; }}
    85%  {{ transform: translateY(550px) translateX(15px) rotate(450deg) scale(0.9); opacity: 0.3; }}
    100% {{ opacity: 0;   transform: translateY(600px) translateX(25px) rotate(540deg) scale(0.7); }}
  }}

  /* ── NPC 舞台 ── */
  .npc-stage {{
    position: absolute;
    bottom: 118px; left: 0; right: 0;
    display: flex; justify-content: center; align-items: flex-end;
    pointer-events: none;
  }}
  .npc-wrap {{
    position: relative;
    display: flex; flex-direction: column; align-items: center;
    transition: transform 0.55s cubic-bezier(.22,1,.36,1), opacity 0.4s;
  }}
  .npc-enter  {{ animation: npcEnter 0.6s cubic-bezier(.22,1,.36,1) forwards; }}
  .npc-idle   {{ transform: translateX(0) scale(1); opacity: 1; }}
  .npc-leave  {{ animation: npcLeave 0.45s ease-in forwards; }}
  @keyframes npcEnter {{
    from {{ transform: translateX(240px) scale(0.85); opacity: 0; }}
    to   {{ transform: translateX(0)    scale(1);    opacity: 1; }}
  }}
  @keyframes npcLeave {{
    from {{ transform: translateX(0)     scale(1);    opacity: 1; }}
    to   {{ transform: translateX(-260px) scale(0.85); opacity: 0; }}
  }}
  .npc-float {{ animation: npcFloat 3s ease-in-out infinite; }}
  @keyframes npcFloat {{
    0%, 100% {{ transform: translateY(0); }}
    50%       {{ transform: translateY(-6px); }}
  }}

  /* ── HUD ── */
  .hud {{
    position: absolute; top: 14px; left: 14px; right: 14px;
    display: flex; justify-content: space-between; align-items: center;
  }}
  .hud-pill {{
    background: rgba(255,200,220,0.40);
    border: 1px solid rgba(255,100,150,0.35);
    border-radius: 20px; padding: 5px 14px;
    font-size: 12px; color: #d8609a;
    backdrop-filter: blur(6px);
    letter-spacing: 0.3px;
  }}
  .hud-score {{ font-size: 15px; font-weight: 500; color: #d8609a; }}

  /* ── 进度条 ── */
  .progress-bar {{
    position: absolute; top: 48px; left: 14px; right: 14px; height: 3px;
    background: rgba(200,80,154,0.2); border-radius: 2px;
  }}
  .progress-fill {{
    height: 100%; border-radius: 2px;
    background: linear-gradient(90deg, #c060a0, #ff80b0);
    transition: width 0.5s ease;
  }}

  /* ── 对话框 ── */
  .dialog-box {{
    background: rgba(255,200,220,0.58);
    border: 1px solid rgba(255,150,200,0.5);
    border-radius: 12px; padding: 13px 20px;
    backdrop-filter: blur(12px);
    margin-bottom: 10px;
    box-shadow: 0 4px 12px rgba(200, 100, 150, 0.15), 
                inset 0 1px 2px rgba(255, 255, 255, 0.4),
                0 1px 3px rgba(100, 30, 80, 0.1);
  }}
  .npc-name {{
    font-size: 11px; font-weight: 600;
    color: #d8609a; letter-spacing: 1.2px;
    text-transform: uppercase; margin-bottom: 6px;
    text-shadow: 0 1px 2px rgba(255, 255, 255, 0.3);
  }}
  .dialog-text {{
    font-size: 13.5px; color: #c8509a; line-height: 1.68;
    font-family: 'Noto Serif SC', serif;
    text-shadow: 0 1px 1px rgba(255, 255, 255, 0.2);
  }}

  /* ── 选项区 ── */
  .options-wrap {{ display: flex; flex-direction: column; gap: 7px; }}
  .opt-btn {{
    display: flex; align-items: flex-start; gap: 11px;
    width: 100%; text-align: left; cursor: pointer;
    background: rgba(255,200,220,0.52);
    border: 1px solid rgba(255,120,170,0.35);
    border-radius: 10px; padding: 11px 16px;
    color: #c8509a; font-size: 13px; line-height: 1.5;
    font-family: 'Noto Sans SC', sans-serif;
    transition: background 0.18s cubic-bezier(.22,1,.36,1), 
                border-color 0.18s, 
                transform 0.14s,
                box-shadow 0.18s;
    backdrop-filter: blur(6px);
    box-shadow: 0 2px 6px rgba(200, 100, 150, 0.12),
                inset 0 1px 2px rgba(255, 255, 255, 0.3);
  }}
  .opt-btn:hover {{
    background: rgba(180,60,120,0.4);
    border-color: rgba(255,120,180,0.55);
    transform: translateX(5px);
    box-shadow: 0 4px 12px rgba(200, 100, 150, 0.2),
                inset 0 1px 2px rgba(255, 255, 255, 0.3);
  }}
  .opt-btn:active {{ transform: translateX(3px) scale(0.98); }}
  .opt-tag {{
    flex-shrink: 0;
    display: inline-flex; align-items: center; justify-content: center;
    width: 24px; height: 24px; border-radius: 6px;
    background: linear-gradient(135deg, rgba(255,120,160,0.35), rgba(255,150,180,0.25));
    color: #d8609a; font-size: 11px; font-weight: 600;
    margin-top: 1px;
    box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.4);
  }}

  /* ── 结果框 ── */
  .result-box {{
    background: rgba(255,200,220,0.62);
    border: 1px solid rgba(255,150,200,0.5);
    border-radius: 12px; padding: 16px 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 12px rgba(200, 100, 150, 0.15), 
                inset 0 1px 2px rgba(255, 255, 255, 0.4);
  }}
  .result-text {{
    font-size: 13px; color: #c8509a; line-height: 1.7;
    font-family: 'Noto Serif SC', serif;
    margin-bottom: 12px;
    text-shadow: 0 1px 1px rgba(255, 255, 255, 0.2);
  }}
  .result-score {{
    display: inline-block;
    font-size: 13px; font-weight: 600;
    padding: 6px 16px; border-radius: 22px;
    margin-bottom: 12px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }}
  .score-pos {{ background: rgba(40,170,80,0.25);  color: #2faa50; border: 1px solid rgba(40,170,80,0.35); }}
  .score-neg {{ background: rgba(200,80,80,0.23);  color: #d84a4a; border: 1px solid rgba(200,80,80,0.3); }}
  .score-neu {{ background: rgba(150,120,60,0.22); color: #b88a3a; border: 1px solid rgba(150,120,60,0.3); }}
  .ach-badge {{
    display: inline-block;
    background: rgba(220,160,30,0.2); color: #ffd060;
    border: 1px solid rgba(220,160,30,0.35);
    border-radius: 20px; padding: 4px 14px;
    font-size: 12px; margin-bottom: 10px;
  }}
  .next-btn {{
    display: block; width: 100%;
    background: rgba(180,50,100,0.32);
    border: 1px solid rgba(255,120,160,0.45);
    border-radius: 9px; color: #d8609a;
    font-size: 13px; font-weight: 500;
    padding: 10px; cursor: pointer;
    font-family: 'Noto Sans SC', sans-serif;
    transition: background 0.16s;
  }}
  .next-btn:hover {{ background: rgba(180,50,100,0.52); }}

  /* ── UI 下半部分容器 ── */
  .ui-layer {{
    position: absolute;
    bottom: 14px; left: 14px; right: 14px;
  }}

  /* ── 场景标题 ── */
  .scene-tag {{
    position: absolute; bottom: 144px; left: 14px;
    background: rgba(255,200,220,0.40);
    border: 1px solid rgba(255,100,150,0.3);
    border-radius: 8px; padding: 4px 12px;
    font-size: 10px; color: #ff90c0;
    letter-spacing: 0.8px;
    backdrop-filter: blur(6px);
  }}
</style>
</head>
<body>
<div class="game-frame" id="gf">

  <div class="bg-sky"></div>

  <!-- 樱花树 SVG 背景 -->
  <svg class="bg-trees" viewBox="0 0 700 560" preserveAspectRatio="xMidYMax meet">
    <defs>
      <filter id="tree-shadow">
        <feGaussianBlur in="SourceGraphic" stdDeviation="3"/>
      </filter>
      <radialGradient id="tree-light" cx="30%" cy="30%">
        <stop offset="0%" stop-color="#ff99cc" stop-opacity="0.2"/>
        <stop offset="100%" stop-color="#dd4488" stop-opacity="0"/>
      </radialGradient>
    </defs>
    <!-- 背景远树 -->
    <g opacity="0.25">
      <ellipse cx="150" cy="280" rx="120" ry="80" fill="#9a2a58"/>
      <ellipse cx="550" cy="290" rx="110" ry="75" fill="#9a2a58"/>
    </g>
    <!-- 左侧大树 -->
    <g opacity="0.85" filter="url(#tree-shadow)">
      <ellipse cx="75"  cy="165" rx="95" ry="72" fill="#7a1a48"/>
      <ellipse cx="55"  cy="190" rx="72" ry="56" fill="#a83070"/>
      <ellipse cx="95"  cy="148" rx="78" ry="62" fill="#c84090"/>
      <ellipse cx="115" cy="175" rx="58" ry="45" fill="#e860b0"/>
      <ellipse cx="75"  cy="150" rx="45" ry="35" fill="url(#tree-light)"/>
      <rect x="108" y="265" width="18" height="130" rx="6" fill="#4a2010"/>
    </g>
    <!-- 右侧大树 -->
    <g opacity="0.85" filter="url(#tree-shadow)">
      <ellipse cx="625" cy="165" rx="95" ry="72" fill="#7a1a48"/>
      <ellipse cx="645" cy="190" rx="72" ry="56" fill="#a83070"/>
      <ellipse cx="605" cy="148" rx="78" ry="62" fill="#c84090"/>
      <ellipse cx="585" cy="175" rx="58" ry="45" fill="#e860b0"/>
      <ellipse cx="625" cy="150" rx="45" ry="35" fill="url(#tree-light)"/>
      <rect x="574" y="265" width="18" height="130" rx="6" fill="#4a2010"/>
    </g>
    <!-- 中景左树 -->
    <g opacity="0.65">
      <ellipse cx="195" cy="235" rx="58" ry="45" fill="#952860"/>
      <ellipse cx="210" cy="220" rx="42" ry="34" fill="#bb4080"/>
      <ellipse cx="190" cy="215" rx="28" ry="22" fill="#dd6aa0" opacity="0.5"/>
      <rect x="188" y="275" width="14" height="90" rx="4" fill="#5a2820"/>
    </g>
    <!-- 中景右树 -->
    <g opacity="0.65">
      <ellipse cx="505" cy="235" rx="58" ry="45" fill="#952860"/>
      <ellipse cx="490" cy="220" rx="42" ry="34" fill="#bb4080"/>
      <ellipse cx="510" cy="215" rx="28" ry="22" fill="#dd6aa0" opacity="0.5"/>
      <rect x="498" y="275" width="14" height="90" rx="4" fill="#5a2820"/>
    </g>
    <!-- 近景小树群 -->
    <g opacity="0.45">
      <ellipse cx="120" cy="300" rx="35" ry="28" fill="#b84080"/>
      <ellipse cx="580" cy="305" rx="38" ry="30" fill="#b84080"/>
    </g>
    <!-- 枝条细节 -->
    <path d="M108,265 Q80,220 40,200" stroke="#5a2010" stroke-width="3" fill="none" opacity="0.7" stroke-linecap="round"/>
    <path d="M126,265 Q140,230 175,210" stroke="#5a2010" stroke-width="2.5" fill="none" opacity="0.6" stroke-linecap="round"/>
    <path d="M574,265 Q560,225 525,208" stroke="#5a2010" stroke-width="3" fill="none" opacity="0.7" stroke-linecap="round"/>
    <path d="M592,265 Q610,230 645,215" stroke="#5a2010" stroke-width="2.5" fill="none" opacity="0.6" stroke-linecap="round"/>
    <!-- 细枝 -->
    <path d="M50,220 L35,200" stroke="#7a3820" stroke-width="1.5" opacity="0.4" stroke-linecap="round"/>
    <path d="M60,210 L45,190" stroke="#7a3820" stroke-width="1.5" opacity="0.4" stroke-linecap="round"/>
    <path d="M650,220 L665,200" stroke="#7a3820" stroke-width="1.5" opacity="0.4" stroke-linecap="round"/>
    <path d="M640,210 L655,190" stroke="#7a3820" stroke-width="1.5" opacity="0.4" stroke-linecap="round"/>
    <!-- 花瓣散落点 -->
    <circle cx="140" cy="320" r="2.5" fill="#ffb3cc" opacity="0.6"/>
    <circle cx="180" cy="350" r="2" fill="#ffb3cc" opacity="0.5"/>
    <circle cx="250" cy="330" r="2.5" fill="#ffb3cc" opacity="0.55"/>
    <circle cx="320" cy="380" r="2" fill="#ffb3cc" opacity="0.5"/>
    <circle cx="380" cy="360" r="2.5" fill="#ffb3cc" opacity="0.5"/>
    <circle cx="450" cy="390" r="2" fill="#ffb3cc" opacity="0.45"/>
    <circle cx="520" cy="350" r="2.5" fill="#ffb3cc" opacity="0.55"/>
    <circle cx="570" cy="370" r="2" fill="#ffb3cc" opacity="0.5"/>
  </svg>

  <div class="ground"></div>
  <div class="path"></div>

  <!-- NPC 舞台 -->
  <div class="npc-stage">
    <div class="npc-wrap {anim_class}" id="npcWrap">
      <div class="npc-float">
        {npc_svg_b64}
      </div>
    </div>
  </div>

  <!-- HUD -->
  <div class="hud">
    <div class="hud-pill">第 {current+1} / {total} 关</div>
    <div class="hud-pill">守护值 <span class="hud-score">{score}</span></div>
  </div>

  <!-- 进度条 -->
  <div class="progress-bar">
    <div class="progress-fill" style="width:{int((current/total)*100)}%"></div>
  </div>

  <!-- 场景标签 -->
  <div class="scene-tag">📍 {scene_data['title']} · {scene_data['subtitle']}</div>

  <!-- UI 层 -->
  <div class="ui-layer">
    {bottom_content}
  </div>

</div>

<script>
// 花瓣生成 - 大幅增加花瓣数量和美化效果
(function() {{
  const frame = document.getElementById('gf');
  const petalCount = 50;  // 增加到50片花瓣
  
  for (let i = 0; i < petalCount; i++) {{
    const p = document.createElement('div');
    p.className = 'petal';
    
    // 更丰富的尺寸变化
    const baseSize = 3 + Math.random() * 8;
    const width = baseSize + Math.random() * 3;
    const height = baseSize * 0.6 + Math.random() * 2;
    
    // 使用更真实的花瓣颜色范围
    const hue = 335 + Math.random() * 30;
    const sat = 70 + Math.random() * 25;
    const light = 72 + Math.random() * 18;
    
    // 随机横向位置，放宽范围增加覆盖面
    const leftPercent = -5 + Math.random() * 110;
    
    // 增加动画时长变化
    const duration = 6 + Math.random() * 10;
    const delay = Math.random() * 12;
    
    p.style.cssText = `
      width: ${{width}}px;
      height: ${{height}}px;
      left: ${{leftPercent}}%;
      top: -10px;
      background: hsl(${{hue}}, ${{sat}}%, ${{light}}%);
      animation-duration: ${{duration}}s;
      animation-delay: ${{delay}}s;
      transform: rotate(${{Math.random() * 360}}deg);
      box-shadow: inset -1px -1px 2px rgba(255,255,255,0.3);
    `;
    frame.appendChild(p);
  }}
}})();

// 选项点击 -> 发送到 Streamlit
document.querySelectorAll('.opt-btn').forEach(btn => {{
  btn.addEventListener('click', function() {{
    const opt = this.getAttribute('data-opt');
    // 通过 URL hash 传递选择，触发 Streamlit 重跑
    window.parent.postMessage({{type:'streamlit:setComponentValue', value: opt}}, '*');
  }});
}});

// 下一关按钮
const nextBtn = document.getElementById('nextBtn');
if (nextBtn) {{
  nextBtn.addEventListener('click', function() {{
    window.parent.postMessage({{type:'streamlit:setComponentValue', value:'__next__'}}, '*');
  }});
}}
</script>
</body>
</html>"""
    return html


def build_final_html(score, history, achievements):
    stats = calculate_stats(history)
    title, poem, emoji = get_rank(score, stats)
    stats = calculate_stats(history)

    rows = ""
    for i, (cg_id, choice, delta, result_text) in enumerate(history, 1):
        sign = "+" if delta > 0 else ""
        color = "#70ff90" if delta > 0 else ("#ff8888" if delta < 0 else "#cc99ff")
        rows += f"""
        <div class="hist-row">
          <span class="hist-num">{i}</span>
          <span class="hist-title">{SCENES[cg_id]['subtitle']}</span>
          <span class="hist-choice">选{choice}</span>
          <span class="hist-score" style="color:{color}">{sign}{delta}</span>
        </div>"""

    ach_html = ""
    for ach in achievements:
        ach_html += f'<div class="ach-item">🏅 {ach}</div>'

    # 添加统计信息HTML
    stats_html = f"""
    <div class="section-title">📊 本局统计</div>
    <div class="stats-grid">
      <div class="stat-item">
        <div class="stat-value">{stats['total_scenes']}</div>
        <div class="stat-label">总场景</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{stats['positive_choices']}</div>
        <div class="stat-label">正确选择</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{stats['negative_choices']}</div>
        <div class="stat-label">需改进</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{stats['accuracy']:.1f}%</div>
        <div class="stat-label">正确率</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{stats['avg_score']:+.1f}</div>
        <div class="stat-label">平均得分</div>
      </div>
    </div>
    """

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600&family=Noto+Sans+SC:wght@400;500&display=swap');
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background: transparent; font-family:'Noto Sans SC',sans-serif; }}
  .final-wrap {{
    background: linear-gradient(160deg,#ffe6f3 0%,#ffd9ed 50%,#ffe6f3 100%);
    border-radius:16px; padding:28px 24px; color:#a84a80;
    border: 1px solid rgba(255,100,150,0.3);
  }}
  .rank-box {{
    text-align:center; padding:20px 0 24px;
    border-bottom: 1px solid rgba(200,80,154,0.25);
    margin-bottom:20px;
  }}
  .rank-emoji {{ font-size:44px; margin-bottom:10px; display:block; }}
  .rank-title {{ font-size:26px; font-weight:600; color:#d8609a; font-family:'Noto Serif SC',serif; margin-bottom:6px; }}
  .rank-poem  {{ font-size:13px; color:#9a4080; font-style:italic; margin-bottom:14px; }}
  .rank-score {{ font-size:32px; font-weight:500; color:#d8609a; }}
  .rank-score span {{ font-size:14px; color:#9a4080; margin-left:4px; }}
  .section-title {{ font-size:12px; color:#d8609a; letter-spacing:1px; margin-bottom:10px; font-weight:500; }}
  .ach-list {{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px; }}
  .ach-item {{ background:rgba(220,160,30,.18); color:#ffd060; border:1px solid rgba(220,160,30,.3); border-radius:20px; padding:4px 14px; font-size:12px; }}
  .stats-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(80px,1fr)); gap:12px; margin-bottom:20px; }}
  .stat-item {{ background:rgba(255,160,200,.08); border:1px solid rgba(255,160,200,.15); border-radius:10px; padding:12px 8px; text-align:center; }}
  .stat-value {{ font-size:18px; font-weight:600; color:#d8609a; margin-bottom:4px; }}
  .stat-label {{ font-size:11px; color:#9a4080; }}
  .hist-list {{ display:flex; flex-direction:column; gap:5px; margin-bottom:24px; }}
  .hist-row {{ display:flex; align-items:center; gap:8px; background:rgba(255,160,200,.05); border-radius:8px; padding:7px 12px; font-size:12px; }}
  .hist-num {{ width:20px; height:20px; border-radius:50%; background:rgba(255,100,160,.2); color:#d8609a; display:flex; align-items:center; justify-content:center; font-size:10px; flex-shrink:0; }}
  .hist-title {{ flex:1; color:#d8609a; }}
  .hist-choice {{ color:#9a4080; flex-shrink:0; }}
  .hist-score {{ width:38px; text-align:right; font-weight:500; flex-shrink:0; }}
  .restart-btn {{ display:block; width:100%; background:rgba(180,50,100,.35); border:1px solid rgba(255,120,160,.45); border-radius:10px; color:#d8609a; font-size:14px; font-weight:500; padding:12px; cursor:pointer; font-family:'Noto Sans SC',sans-serif; transition:background .16s; }}
  .restart-btn:hover {{ background:rgba(180,50,100,.55); }}
</style>
</head><body>
<div class="final-wrap">
  <div class="rank-box">
    <span class="rank-emoji">{emoji}</span>
    <div class="rank-title">{title}</div>
    <div class="rank-poem">{poem}</div>
    <div class="rank-score">{score}<span>守护值</span></div>
  </div>
  {"<div class='section-title'>🏅 特殊成就</div><div class='ach-list'>" + ach_html + "</div>" if achievements else ""}
  {stats_html}
  <div class="section-title">📋 本局回顾</div>
  <div class="hist-list">{rows}</div>
  <button class="restart-btn" onclick="window.parent.postMessage({{type:'streamlit:setComponentValue',value:'__restart__'}},'*')">🔄 再来一局</button>
</div>

</body></html>"""


# ─────────────────────────────────────────────────────────────
# 主程序
# ─────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="珞珈樱花守护者",
        page_icon="🌸",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # 全局样式覆盖
    st.markdown("""
    <style>
    .stApp { background: #fff5f9; }
    .block-container { max-width: 680px; padding: 1rem 1rem 2rem; }
    header[data-testid="stHeader"] { background: transparent; }
    </style>
    """, unsafe_allow_html=True)

    validate_scene_pools()
    init_state()

    # 接收组件消息（通过 query params 模拟）
    # Streamlit 用 st.components 的 bidirectional 需要自定义组件
    # 这里改用纯 Streamlit 按钮驱动，HTML 只做视觉渲染

    if not st.session_state.started:
        _render_welcome()
        return

    idx = st.session_state.current
    total = len(st.session_state.levels)

    # 游戏结束
    if idx >= total:
        _render_final()
        return

    _render_game()


def _render_welcome():
    st.markdown("""
    <div style="text-align:center;padding:40px 20px 20px;">
      <div style="font-size:52px;margin-bottom:12px;">🌸</div>
      <h1 style="color:#ffd0e8;font-size:28px;font-weight:600;font-family:serif;margin-bottom:8px;">
        珞珈樱花守护者
      </h1>
      <p style="color:#c090b0;font-size:14px;margin-bottom:4px;">武汉大学志愿服务模拟系统</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div style="background:rgba(255,160,200,.06);border:1px solid rgba(255,160,200,.12);
             border-radius:12px;padding:18px 20px;color:#e0c0d0;font-size:13.5px;line-height:1.8;margin-bottom:16px;">
        化身<strong style="color:#ff90c0">红马甲志愿者</strong>，在武大樱花季高峰时段守护珞珈山。<br>
        面对随机抽取的 <strong style="color:#ff90c0">15 个场景</strong>，做出最佳抉择，积累守护值，解锁专属成就。<br><br>
        🎯 &nbsp;每局从 30 个场景中随机抽取 · 特殊 4 关 · 中性 1 关 · 普通 10 关<br>
        📊 &nbsp;满分约 100 分 · 共 6 个等级称号
        </div>
        """, unsafe_allow_html=True)

    if st.button("🌸 &nbsp; 开始守护任务", use_container_width=True, type="primary"):
        start_game()
        st.rerun()


def _render_game():
    idx = st.session_state.current
    total = len(st.session_state.levels)
    cg_id = st.session_state.levels[idx]
    scene = SCENES[cg_id]
    score = st.session_state.score
    phase = st.session_state.phase
    
    # 顶部：背景音乐播放器
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown("🎵")
    with col2:
        try:
            import os
            import base64
            audio_path = os.path.join(os.path.dirname(__file__), '樱花音乐.mp3')
            if os.path.exists(audio_path):
                with open(audio_path, 'rb') as f:
                    audio_data = f.read()
                audio_b64 = base64.b64encode(audio_data).decode()
                audio_html = f'''
                <audio controls autoplay loop style="width: 100%;">
                    <source src="data:audio/mpeg;base64,{audio_b64}" type="audio/mpeg">
                    您的浏览器不支持音频播放。
                </audio>
                '''
                st.markdown(audio_html, unsafe_allow_html=True)
                st.caption("🎵 樱花音乐播放中...")
            else:
                st.warning("🎵 音乐文件不存在，请确保 '樱花音乐.mp3' 在项目目录中")
        except Exception as e:
            st.error(f"🎵 音乐加载失败: {str(e)}")
    with col3:
        pass

    # 渲染视觉游戏画面
    import streamlit.components.v1 as components
    game_html = build_game_html(
        scene_data=scene,
        score=score,
        current=idx,
        total=total,
        phase=phase,
        last_choice=st.session_state.last_choice,
        achievements=st.session_state.achievements,
    )
    components.html(game_html, height=570, scrolling=False)
    
    # 画面下方控制按钮（透明背景，与上方游戏画面视觉融合）
    st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
    
    if phase == "question":
        scene = SCENES[cg_id]
        opts = scene["options"]
        option_keys = list(opts.keys())
        cols = st.columns([1] * len(option_keys))

        for col, opt_key in zip(cols, option_keys):
            with col:
                if st.button(f"{opt_key}\n{opts[opt_key]}", key=f"opt_{opt_key}", use_container_width=True):
                    choose(opt_key)
                    st.rerun()
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            pass
        with col2:
            is_last = idx >= total - 1
            btn_label = "📊 最终报告" if is_last else "下一关 →"
            if st.button(btn_label, use_container_width=True, type="primary"):
                next_scene(); st.rerun()


def _render_final():
    import streamlit.components.v1 as components

    score = st.session_state.score
    history = st.session_state.history
    achievements = st.session_state.achievements

    final_html = build_final_html(score, history, achievements)
    components.html(final_html, height=max(600, 200 + len(history) * 42), scrolling=False)
    
    # 最后的控制按钮
    st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 再来一局", use_container_width=True, type="primary"):
            start_game()
            st.rerun()


if __name__ == "__main__":
    main()