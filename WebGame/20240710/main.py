import time
from calculate import adjust_nums ,find_valid_combinations,adjust_cards
from AutoGameFore20240710 import Game

class Auto(Game):
    def __init__(self) -> None:
        super().__init__()

    def auto_gacha(self):
        """
        自动抽卡
        """
        while self.current_coin > 0:
            self.draw_cards()
    
    
    def auto_merge_luxePerfume(self):
        """
        合成高级香水
        """
        #先判断合成高级香水任务是否完成
        for info in self.reward_infos:
            if info['reward_id']==40034 and ( not info['status']=="RS_DOING" ):
                return
        
        #如果万能卡有3个，直接使用万能卡合成高级香水
        for card in self.cards:
            if card['id']==10023 and card['num']>=3:
                self.merge_perfume(10023)
                return
            
        #将互斥卡片的数量合并到其中一个卡片中
        for t in adjust_cards(self.cards):
            self.exchange_card(t["from_id"],t['to_id'],t['num'])
        #刷新self.cards
        self.index()

        #判断数量是否够合成高级香水
        flag=0
        for card in self.cards:
            if card['id']<10017 and card['num']>=3:
                flag+=1
            if flag >=3:
                #互斥的卡片都合并到这三个id上了
                self.merge_card(10013)
                self.merge_card(10015)
                self.merge_card(10016)
                self.merge_perfume([10019,10021,10022])
                return
        print('高级卡or万能卡数量不够，如果时间急可自行尝试高级卡跟万能卡的组合')
    def auto_merge_perfume(self):
        #如果已经合成12瓶以上的香水
        if self.perfume_num >= 12:
            return
        #配平卡片数量接近平均值
        results=adjust_nums(self.cards)
        print("配平结果",results)
        for t in adjust_nums(self.cards):
            self.exchange_card(*t)
            time.sleep(5)
        #刷新self.cards
        self.index()
        results=find_valid_combinations(self.cards)
        print(results)
        for formula in results:
            self.merge_perfume(formula)
            time.sleep(1)
            self.perfume_num+=1
            if self.perfume_num >= 12:
                return
    
    def auto_give_perfume(self):
        #如果没有赠送过香水，那就送给芙芙id=3
        if self.has_given:
            return
        
        self.book_list()
        for perfume in self.perfumes:
            if perfume['perfume_num'] > 0:
                perfume_id=perfume['perfume_id']
                self.give_perfume(perfume_id,3) 
                return

    def auto_share(self):
        if not self.is_share_report:
            self.share_report()
    
    def auto_finish_task(self):
        for task in self.tasks:
            if not (task['status']=='TS_DOING'):
                continue
            if task['task_id'] == 5021: #地图工具：5021
                self.finish_task(5021)
            elif task['task_id'] == 5022: #冒险互助：5022
                self.finish_task(5022)

    def auto_award_task(self):
        for task in self.tasks:
            if not (task['status']=='TS_DONE'):
                continue
            self.award_task(task['task_id'])
    
    def auto_claim_reward(self):
        """
        reward_id
        40030:3瓶香水
        40031:6瓶香水
        40032:9瓶香水
        40033:12瓶香水
        40034:1瓶高级香水
        40035:送一瓶香水
        40036:分享报告
        """
        for reward in self.reward_infos:
            if reward['status']=='RS_DONE':
                self.claim_reward(reward['reward_id'])

    def main(self):
        print("完成特殊每日任务,获得抽卡机会")
        self.auto_finish_task()
        time.sleep(1)
        self.auto_award_task()
        time.sleep(1)
        
        print("自动抽卡")
        self.auto_gacha()
        time.sleep(1)

        print("自动合成高级香水")
        self.auto_merge_luxePerfume()
        time.sleep(1)
        
        print("自动合成香水")
        self.auto_merge_perfume()
        time.sleep(1)
        
        print("自动分享调香报告")
        self.auto_share()
        time.sleep(1)
        
        print("自动赠礼")
        self.auto_give_perfume()
        time.sleep(1)
        
        print("自动领取游戏道具")
        self.auto_claim_reward()
        time.sleep(1)


if __name__ == "__main__":
    auto=Auto()
    auto.main()
    print("OVER")
    time.sleep(9999)


