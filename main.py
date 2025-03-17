import openai
import json
import re
from tqdm import tqdm
def get_ner(text):
    
    prompt = """
你是一位狼杀人信息提取高手玩家。请根据内容，分析并给出内容呈现的信息：
role只有五种角色或者是好人和坏人:
角色为：[werewolf,seer,guard,villager,witch]
好人为:good 包括 [seer,guard,villager,witch]
坏人为:bad 只有 [werewolf]
行为可以是多个,为自然语言
请使用以下严格的JSON格式返回结果，JSON的key应该是分析的句子内容，不要包含任何额外的解释：
```json
{
  "identity":[{"role1":[id1,id2]},{"role2":[id3]}],
  "action":["action1","action2"] 
}
```
示例:
input:
我觉得1号,2号比较可疑,有可能是狼人,刚刚3号自爆为预言家比较可信,所有我建议今天投2号,晚上女巫毒2号好了。


output:
```json
{
  "identity":[{"werewolf":[1,2]},{"seer",[3]},{"good",[3]},{"bad",[1,2]}],
  "action":["票走2号","女巫毒1号"] 
}
```
 

以下是需要分析的句子：
"""
    
    # Add each sentence to the prompt
    # for i, sentence in enumerate(sentences):
    #     prompt += f"\n{i+1}. {sentence}"
    prompt+=text
    try:
        response = openai.ChatCompletion.create(
            model="ep-20250302223513-s987j",  # Use your model here
            messages=[
                {"role": "system", "content": "你是一位狼人杀游戏高手。你只返回JSON格式的结果，不包含任何额外的解释。"},
                {"role": "user", "content": prompt}
            ],
            api_base="https://ark.cn-beijing.volces.com/api/v3",
            api_key='6cf4e49c-c8d8-46d7-b123-a7dcdf16b33f'  # Use your API key here
        )
        
        # Extract the response content
        content = response["choices"][0]["message"]["content"].strip()
        
        # Find and extract the JSON part
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # If no code block, try to extract anything that looks like JSON
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
            else:
                json_str = content
        
        # Parse the JSON response
        scores_dict = json.loads(json_str)
        return scores_dict
    
    except Exception as e:
        print(f"Error: {e}")
        # Return empty dictionary if there's an error
        return  { 
                 "identity":[],
                    "action":[] 
                            }

def get_big_five_scores(text):
    
    sentences = re.split(r'[。！？!?.]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Create a more specific prompt with clear instructions
    prompt = """
你是一位精通心理学的专家，负责评估文本中的大五人格特质。对于每个句子，请根据其内容，分析并给出以下五个维度的合理评分（范围为0到120）：
- 开放性（Openness）：对新体验、新思想的接受程度
- 尽责性（Conscientiousness）：组织性、可靠性和自律性
- 外向性（Extraversion）：社交性、精力和积极情绪
- 宜人性（Agreeableness）：合作性、同情心和利他主义
- 神经质（Neuroticism）：情绪不稳定性和负面情绪倾向

请分析以下句子，并为每个句子给出这五个维度的评分。请使用以下严格的JSON格式返回结果，JSON的key应该是分析的句子内容，不要包含任何额外的解释：
```json
{
  "句子1": [开放性, 尽责性, 外向性, 宜人性, 神经质],
  "句子2": [开放性, 尽责性, 外向性, 宜人性, 神经质]
}
```

以下是需要分析的句子：
"""
    
    # Add each sentence to the prompt
    for i, sentence in enumerate(sentences):
        prompt += f"\n{i+1}. {sentence}"
    
    try:
        response = openai.ChatCompletion.create(
            model="ep-20250302223513-s987j",  # Use your model here
            messages=[
                {"role": "system", "content": "你是一位精通心理学的专家，擅长评估文本的大五人格特质。你只返回JSON格式的结果，不包含任何额外的解释。"},
                {"role": "user", "content": prompt}
            ],
            api_base="https://ark.cn-beijing.volces.com/api/v3",
            api_key='6cf4e49c-c8d8-46d7-b123-a7dcdf16b33f'  # Use your API key here
        )
        
        # Extract the response content
        content = response["choices"][0]["message"]["content"].strip()
        
        # Find and extract the JSON part
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # If no code block, try to extract anything that looks like JSON
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
            else:
                json_str = content
        
        # Parse the JSON response
        scores_dict = json.loads(json_str)
        return scores_dict
    
    except Exception as e:
        print(f"Error: {e}")
        # Return empty dictionary if there's an error
        return {sentence: [0, 0, 0, 0, 0] for sentence in sentences}

def analyze_game_text(text):
  
   
    scores = get_big_five_scores(text)
    ner = get_ner(text)
    return scores,ner

if __name__ == "__main__":
    # input_text = "Player3的发言暂时可以认好，大家别急着踩他。平安夜信息量少，狼人肯定在搅混水，注意谁急着分票。守卫女巫自己判断要不要藏，预言家该跳的时候自然会跳，咱们稳扎稳打别送轮次"
    # print(get_ner(input_text))
    # import sys 
    # sys.exit(0)
    with open('phase_speeches.json',mode='r',encoding='utf8') as f:
        speech_data = json.load(f)
    # print(speech_data.keys())
    # final_json = {}
    final_daytime_speech_data = {"logs":{},"role_truth":speech_data["role_truth"]}
    for day_time_key in tqdm(speech_data['daytime'].keys()):
        origin_day_time_data = speech_data['daytime'][day_time_key]
        day_time_data = []
        for play_name in origin_day_time_data.keys():
            player_day_data = {
                "name": "",
                "content": "",
                "big_five_scores": {
                    
                }
            }
            Player_content = origin_day_time_data[play_name]["content"]
            player_day_data["name"]=  play_name
            player_day_data["content"]=  Player_content
            score,ner = analyze_game_text(Player_content)
            player_day_data["big_five_scores"]=  score
            player_day_data["identity"] = ner["identity"]
            player_day_data["action"] = ner["action"]
            day_time_data.append(player_day_data)
        final_daytime_speech_data['logs'][day_time_key] = day_time_data
    print(final_daytime_speech_data)
    with open('1.json',mode='w',encoding='utf8') as f:
        json.dump(final_daytime_speech_data,f,ensure_ascii=False)
