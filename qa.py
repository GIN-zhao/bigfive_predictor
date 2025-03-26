import openai
import csv
import os
role_ = 'villager'
# openai.api_key = '6cf4e49c-c8d8-46d7-b123-a7dcdf16b33f'

def create_personality_agent():
    system_prompt = """
狼人杀游戏中，
虽然村民没有技能，但其发言与投票行为在协作中至关重要。P2 强调：“村民要能说清自己为什么信谁、不信谁。”，P4 则指出：“发言少，投票优柔寡断、摇摆的平民，对好人阵营是负担”。玩家普遍希望村民具备表达清晰度与主动性，在发言中清晰展示逻辑，避免成为模糊票源。同时，判断力与一定的说服能力也是赢得信任、影响局势的关键。
村民：
请你作为村民，根据上述的职位描述，诚实地回答接下来的50个性格测试题目。回答时请遵守以下原则：
1. 只回复数字1-5（1表示非常不同意,2表示不同意,3表示中立,4表示同意,5表示非常同意）
2. 完全基于你的性格特点回答
3. 保持一致性和真实性
4. 不需要额外解释
5. 尽量不要选择中立，要突出个性鲜明

准备好接受测试了。"""

    return system_prompt

def complete_personality_test():
    system_prompt = create_personality_agent()
    questions = [
        'I am the life of the party.', 
        "I don't talk a lot.", 
        "I feel comfortable around people.", 
        "I keep in the background.", 
        "I start conversations.", 
        "I have little to say.", 
        "I talk to a lot of different people at parties.", 
        "I don't like to draw attention to myself.", 
        "I don't mind being the center of attention.", 
        "I am quiet around strangers.",
        'I get stressed out easily.', 
        "I am relaxed most of the time.", 
        "I worry about things.", 
        "I seldom feel blue.", 
        "I am easily disturbed.", 
        "I get upset easily.", 
        "I change my mood a lot.", 
        "I have frequent mood swings.", 
        "I get irritated easily.", 
        "I often feel blue.",
        'I feel little concern for others.', 
        "I am interested in people.", 
        "I insult people.", 
        "I sympathize with others' feelings.", 
        "I am not interested in other people's problems.", 
        "I have a soft heart.", 
        "I am not really interested in others.", 
        "I take time out for others.", 
        "I feel others' emotions.", 
        "I make people feel at ease.",
        'I am always prepared.', 
        "I leave my belongings around.", 
        "I pay attention to details.", 
        "I make a mess of things.", 
        "I get chores done right away.", 
        "I often forget to put things back in their proper place.", 
        "I like order.", 
        "I shirk my duties.", 
        "I follow a schedule.", 
        "I am exacting in my work.",
        'I have a rich vocabulary.', 
        "I have difficulty understanding abstract ideas.", 
        "I have a vivid imagination.", 
        "I am not interested in abstract ideas.", 
        "I have excellent ideas.", 
        "I do not have a good imagination.", 
        "I am quick to understand things.", 
        "I use difficult words.", 
        "I spend time reflecting on things.", 
        "I am full of ideas."
    ]

    categories = ['EXT', 'EST', 'AGR', 'CSN', 'OPN']
    results = []
    scores = [0,0,0,0,0]
    for i, question in enumerate(questions, 1):
        
        category = categories[(i-1)//10]
        response = openai.ChatCompletion.create(
            model="ep-20250302223513-s987j",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"题目：{question}"}
            ],
            api_base="https://ark.cn-beijing.volces.com/api/v3",
            api_key='6cf4e49c-c8d8-46d7-b123-a7dcdf16b33f'  # Use
        )
        answer = response.choices[0].message.content.strip()
        results.append([f"{category}{(i-1)%10 + 1}", answer])
        
        tmp = int(str(answer))
        if i %2 ==0:
            # print(tmp)
            scores[(i-1)//10] = scores[(i-1)//10]+ 6 - tmp
        else:
            scores[(i-1)//10] += tmp
            
        print(f'question:{question} \n answer:{answer}')

    with open(f'personality_test_results_{role_}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Question', 'Response'])
        writer.writerows(results)
    print(dict(zip(categories,scores)))
complete_personality_test()