from DrissionPage import WebPage
class Game():
    def __init__(self) -> None:
        self.page = WebPage()
        self.page.set.window.size(1280,720)
        self.postUrl='https://hk4e-api.mihoyo.com/event/e20240710perfume'
        self.login()
        self.params = {
            "badge_uid": self.uid,
            "badge_region": "cn_gf01",
            "lang": "zh-cn",
            "game_biz": "hk4e_cn"
        }
        self.page.change_mode("s")
        self.cards = {}
        self.current_coin = 0
        self.has_given = None
        self.is_share_report = None
        self.fristShowIndex=True
        self.perfume_num=0
        self.index()
        
        self.reward_infos={}
        self.reward_list()
        
        self.perfumes = {}
        self.book_list()
        
        self.tasks={}
        self.task_list()

    
    def login(self):
        """用户手动登录网页获取UID,Dr模块两种模式共享cookies,省去获取cookies的步骤"""
        url='https://act.mihoyo.com/ys/event/e20240710perfume-f65h6y/index.html'
        self.page.get(url)
        input("请先登录,登录成功后回车继续")
        self.uid=self.page.ele(".mihoyo-account-role__uid").text.split('UID: ')[1]
        self.cookies=self.page.cookies(as_dict=True,all_domains=True)
        print('UID为',self.uid)
        # print(self.cookies)
        
    def index(self):
        """
        获取游戏内数据
        """
        url = self.postUrl+"/index"
        self.page.get(url,params=self.params)
        data=self.page.json

        self.cards = data['data']['cards']
        self.current_coin = data['data']['current_coin']
        self.has_given = data['data']['has_given']
        self.is_share_report = data['data']['is_share_report']
        self.perfume_num=data['data']['perfume_num']
        if self.fristShowIndex:
            print("cards:", self.cards)
            print("剩余抽卡次数:", self.current_coin)
            print("是否已赠送过:", self.has_given)
            print("是否已分享过调香报告:", self.is_share_report)
            print("已合成的香水数量：",self.perfume_num)
            self.fristShowIndex=False
    
    def book_list(self):
        """
        获取香水列表
        """
        url = self.postUrl+'/book_list'
        self.page.get(url=url,params=self.params)
        print("获取香水列表 ",self.page.json['message'])

        data=self.page.json
        self.perfumes = data['data']['perfumes']

    def task_list(self)->list:
        """
        获取任务列表
        """
        url = self.postUrl+"/task_list"
        params = self.params.copy()
        params.update({"channel": "CHL_EXTER"})
        self.page.get(url,params=params)
        self.tasks=self.page.json['data']['tasks']
        print('获取任务列表：',self.page.json['message'])
    
    def finish_task(self,task_id):
        """完成任务"""
        url = self.postUrl+'/finish_task'
        payload={"task_id":task_id,"channel":"CHL_EXTER"}
        self.page.post(url=url,params=self.params,json=payload)
        print("完成任务id:",task_id,",",self.page.json['message'])
    
    def share_report(self):
        """
            完成分享调香报告，调用一次就可以拿奖励了。目测没有赠送过香水也能调用，但没测试
        """
        url = self.postUrl+'/share_report'
        self.page.post(url=url,params=self.params)
        print("分享调香报告: ",self.page.json['message'])

    def give_perfume(self,perfume_id:int,npc_id:int=3):
        """
        赠送香水
        Args:
            npc_id:3是芙宁娜,猜测1是娜维娅,2是希格雯
            perfume_id:香水id
        """
        url = self.postUrl+'/give_perfume'
        payload={"npc_id":npc_id,"perfume_id":perfume_id}
        self.page.post(url=url,params=self.params,json=payload)
        print("赠送香水",self.page.json['message'])

    def award_task(self,task_id):
        """
        提交任务,获得抽卡机会
        """
        url = self.postUrl+'/award_task'
        payload={"task_id":task_id,"channel":"CHL_EXTER"}
        self.page.post(url,params=self.params,json=payload)

    def reward_list(self):
        """
        获取游戏奖励列表
        """
        url = self.postUrl+'/reward_list'
        self.page.get(url,params=self.params)
        self.reward_infos=self.page.json["data"]["reward_infos"]
        self.perfume_num=self.page.json["data"]["perfume_num"]
        print("获取游戏奖励列表",self.page.json['message'])

    def claim_reward(self,reward_id):
        """
        领取游戏道具奖励
        """
        url = self.postUrl+'/claim_reward'
        payload={"reward_id":reward_id}
        self.page.post(url,params=self.params,json=payload)
        print("领取游戏道具奖励",self.page.json['message'])
    
    def draw_cards(self):
        """抽取卡片"""
        url = self.postUrl+'/draw_cards'
        self.page.post(url=url,params=self.params)
        print("抽取卡片：",self.page.json['message'])

    def merge_card(self,card_id:int):
        """合成高级卡片"""
        url = self.postUrl+'/merge_card'
        card_ids=[card_id,card_id]
        payload={"card_ids":card_ids}
        self.page.post(url=url,params=self.params,json=payload)
        print("合成高级卡片",self.page.json['message'])
    
    def merge_perfume(self,cardList:list):
        """
        合成香水
        Args:
            cardList:[ perfume_id , perfume_id , perfume_id ]
        """
        url=self.postUrl+'/merge_perfume'
        payload={'card_ids': cardList}
        self.page.post(url=url,params=self.params,json=payload)
        print("合成香水：",self.page.json['message'])


    def exchange_card(self,origin_id:int,target_id:int,card_cnt:int=1):
        """
        1比1置换卡片 
        Args:
            origin_id(int):源卡片ID,置换后对应ID卡片数量减一
            target_id(int):目标卡片ID,置换后对应ID卡片数量加一
            card_cnt(int):置换数量,默认为1
        """
        url=self.postUrl+'/exchange_card'
        payload={"origin_id":origin_id,"target_id":target_id,"card_cnt":card_cnt}
        self.page.post(url=url,params=self.params,json=payload)
        print("置换卡片：",self.page.json['message'])

