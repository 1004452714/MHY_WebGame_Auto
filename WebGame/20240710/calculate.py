#这个文件98%以上的内容由GPT3.5根据文字需求生成

from itertools import permutations
def adjust_cards(cards)->list:
    """
    将互斥的卡片数量合并到其中之一的卡片，返回置换步骤
    Returns:
        返回例子：[{'from_id': 10012, 'to_id': 10015, 'num': 2}, {'from_id': 10014, 'to_id': 10016, 'num': 2}]
    """
    transfer_details = []
    adjustments = {
    10011: [10013],
    10012: [10015],
    10014: [10016]
    }
    for from_id, to_ids in adjustments.items():
        if from_id not in [card['id'] for card in cards]:
            continue
        from_card = next(card for card in cards if card['id'] == from_id)
        from_num = from_card['num']
        for to_id in to_ids:
            to_card = next((card for card in cards if card['id'] == to_id), None)
            if to_card:
                to_card['num'] += from_num
                transfer_details.append({"from_id": from_id, "to_id": to_id, "num": from_num})
        from_card['num'] = 0
    return transfer_details

def find_valid_combinations(cards)->list:
    """
    计算卡片合成的所有组合，返回所有结果
    返回例子: [[10011,10012,10014],[10013,10012,10023]]
    """
    rules = [
        [10011, 10013],
        [10012, 10015],
        [10014, 10016]
    ]

    # 将卡片列表转换成一个字典
    card_dict = {card['id']: card['num'] for card in cards}
    
    # 提取所有规则中的数字
    all_numbers = [number for rule in rules if isinstance(rule, list) for number in rule] + \
                  [rule for rule in rules if isinstance(rule, int)]
    
    valid_combinations = []
    
    while True:
        found = False
        # 生成所有可能的3个数字的组合
        all_combinations = permutations(all_numbers, 3)
        
        for combo in all_combinations:
            temp_dict = card_dict.copy()
            valid = True
            used_rules = [False] * len(rules)
            
            for card_id in combo:
                if temp_dict.get(card_id, 0) > 0:
                    # 检查当前卡片ID是否来自已经使用的规则
                    rule_index = next((i for i, rule in enumerate(rules) if (isinstance(rule, list) and card_id in rule) or rule == card_id), None)
                    if rule_index is not None and used_rules[rule_index]:
                        valid = False
                        break
                    
                    # 减少临时字典中该卡片的数量
                    temp_dict[card_id] -= 1
                    used_rules[rule_index] = True
                else:
                    valid = False
                    break
            
            if valid:
                # 如果找到有效组合，更新原始字典并添加到结果列表
                valid_combinations.append(list(combo))
                for card_id in combo:
                    card_dict[card_id] -= 1
                found = True
                break
        
        if not found:
            # 如果没有找到有效组合，退出循环
            break
    return valid_combinations

def preprocess_data(data):
    # 需要检查和补齐的 id 列表
    required_ids = set(range(10011, 10017))

    # 去掉 id 在10017 至 10023 的字典
    data = [d for d in data if not (10017 <= d['id'] <= 10023)]

    # 提取现有的 id
    existing_ids = set(d['id'] for d in data)

    # 找出缺少的 id 并补齐
    missing_ids = required_ids - existing_ids
    for missing_id in missing_ids:
        data.append({'id': missing_id, 'num': 0})

    # 返回处理完的 data
    return data

def adjust_nums(data)->list:
    """
    为了把卡片数量平均化，计算卡片置换的步骤,提供给卡片置换函数使用
    """
    data=preprocess_data(data)
    # 计算所有 'num' 的平均值
    nums = [d['num'] for d in data]
    avg_num = int(sum(nums) / len(nums))
    
    # 初始化步骤记录列表
    steps = []

    while True:
        # 分别找出大于平均值和小于平均值的 'num' 列表
        greater_than_avg = [d for d in data if d['num'] > avg_num]
        less_than_avg = [d for d in data if d['num'] < avg_num]
        # 如果没有大于平均值或小于平均值的情况，退出循环
        if not greater_than_avg or not less_than_avg:
            break

        # 对大于平均值的 'num' 从大到小排序，对小于平均值的 'num' 从小到大排序
        greater_than_avg_sorted = sorted(greater_than_avg, key=lambda x: -x['num'])
        less_than_avg_sorted = sorted(less_than_avg, key=lambda x: x['num'])
        
        # 取最大的大于平均值的 'num' 和最小的小于平均值的 'num'
        max_greater = greater_than_avg_sorted[0]
        min_less = less_than_avg_sorted[0]

        # 计算当前的误差
        current_error = max(max_greater['num'] - avg_num, avg_num - min_less['num'])

        # 如果误差已经小于平均值的1，退出循环
        if current_error < 1:
            break

        # 调整 'num' 值
        if max_greater['num'] - avg_num > avg_num - min_less['num']:
            # 减少大于平均值的 'num'
            max_greater['num'] -= 1
            # 记录步骤
            steps.append([max_greater['id'], min_less['id']])
        else:
            # 增加小于平均值的 'num'
            min_less['num'] += 1
            # 记录步骤
            steps.append([min_less['id'], max_greater['id']])

        # 重新计算 'num' 的列表
        nums = [d['num'] for d in data]

    # 返回修改步骤
    return steps
if __name__ == "__main__":
    # 测试函数
    data = [
        {'id': 10023, 'num': 1},
        {'id': 10016, 'num': 1},
        {'id': 10015, 'num': 1},
        {'id': 10014, 'num': 9},
        {'id': 10012, 'num': 1},
        {'id': 10011, 'num': 1}
    ]

    # 调用函数并打印步骤
    result = adjust_nums(data)
    print(result)

    # 调用函数并打印调整后的数据
    print(data)
    find_valid_combinations(data)
