import json
import re
import copy  # 引入copy模块用于深拷贝

def extract_phase_speeches(content):
    phases = {'daytime': {}, 'night': {}}  # 分别存储白天和夜晚的内容
    current_phase_type = None  # 当前阶段类型：daytime或night
    current_phase_num = None   # 当前阶段编号
    current_player = None      # 当前玩家
    capturing_final = False    # 是否正在捕获最终发言
    final_speech = []          # 存储最终发言内容

    lines = content.split('\n')
    
    for line in lines:
        # 检测阶段开始 (白天/夜晚)
        if line.startswith('**Moderator (-> all)**: 现在是'):
            if match := re.search(r'(daytime|night)-(\d+)', line):
                phase_type = match.group(1)  # 阶段类型：daytime或night
                phase_num = match.group(2)   # 阶段编号
                current_phase_type = phase_type
                current_phase_num = phase_num
                # 初始化当前阶段的存储
                phases[phase_type][f"{phase_type}-{phase_num}"] = {}
                capturing_final = False
                final_speech = []  # 清空final_speech

        # 检测玩家发言块
        elif line.startswith('**Player ') and current_phase_type:
            if match := re.search(r'Player (\d+)', line):
                current_player = f"Player {match.group(1)}"
                capturing_final = False
                final_speech = []  # 清空final_speech

        # 检测最终发言开始
        elif '**最终发言**:' in line and current_player and current_phase_type:
            capturing_final = True
            final_line = re.split(r':|】：', line, 1)[-1].strip()  # 处理中文冒号
            if final_line:
                final_speech.append(final_line)
            continue

        # 捕获多行最终发言
        if capturing_final:
            # 遇到下一个条目或空行时停止
            if any(line.startswith(s) for s in ['- **反思', '- **经验', '- **思考过程', '**Player', '**Moderator']):
                capturing_final = False
                if final_speech and current_phase_type:
                    key = f"{current_phase_type}-{current_phase_num}"
                    # 使用深拷贝存储final_speech
                    print(f'{current_phase_type},{key},{current_player},{final_speech}')
                    if phases[current_phase_type][key].get(current_player) is None:
                        phases[current_phase_type][key][current_player] = copy.deepcopy(final_speech)
                final_speech = []  # 清空final_speech
            else:
                clean_line = line.strip()
                if clean_line:
                    # 合并括号内容
                    if re.match(r'^（.*[^）]$', clean_line):  # 处理未闭合括号
                        if final_speech:
                            final_speech[-1] += clean_line
                        else:
                            final_speech.append(clean_line)
                    else:
                        final_speech.append(clean_line)

    # 处理最后一个未完成的发言
    if capturing_final and final_speech and current_phase_type:
        key = f"{current_phase_type}-{current_phase_num}"
        # 使用深拷贝存储final_speech
        phases[current_phase_type][key][current_player] = copy.deepcopy(final_speech)

    return phases

# 使用示例
with open('88.md', 'r', encoding='utf-8') as f:
    content = f.read()

result = extract_phase_speeches(content)

# 保存为JSON
with open('phase_speeches.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2, sort_keys=True)

print("提取完成，结果已保存为 phase_speeches.json")