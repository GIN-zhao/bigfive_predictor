import openai
import json
import re
from tqdm import tqdm

# def get_big_five_scores(text):
#     """
#     分析文本并返回大五人格的5x6数组分数。
#     """
#     sentences = re.split(r'[。！？!?.]', text)
#     sentences = [s.strip() for s in sentences if s.strip()]
    
#     # 定义大五人格的五个维度及其子维度
#     big_five_dimensions = {
#         "开放性 (Openness)": ["想象力 (Imagination)", "艺术兴趣 (Artistic Interests)", "情感丰富 (Emotionality)", 
#                             "冒险性 (Adventurousness)", "智力 (Intellect)", "自由主义 (Liberalism)"],
#         "尽责性 (Conscientiousness)": ["自律 (Self-Discipline)", "秩序 (Orderliness)", "责任感 (Dutifulness)", 
#                                     "成就导向 (Achievement-Striving)", "谨慎 (Cautiousness)", "效率 (Efficiency)"],
#         "外向性 (Extraversion)": ["社交性 (Sociability)", "活力 (Energy)", "自信 (Assertiveness)", 
#                                 "积极情绪 (Positive Emotions)", "寻求刺激 (Excitement-Seeking)", "健谈 (Talkativeness)"],
#         "宜人性 (Agreeableness)": ["信任 (Trust)", "诚实 (Honesty)", "利他主义 (Altruism)", 
#                                 "顺从 (Compliance)", "谦逊 (Modesty)", "同情心 (Tendermindedness)"],
#         "神经质 (Neuroticism)": ["焦虑 (Anxiety)", "愤怒 (Anger)", "抑郁 (Depression)", 
#                               "自我意识 (Self-Consciousness)", "冲动性 (Impulsiveness)", "脆弱性 (Vulnerability)"]
#     }
    
#     prompt = """
#             你是一位精通心理学的专家，负责评估文本中的大五人格特质。对于每个句子，请根据其内容，分析并给出以下五个维度的评分，每个维度包含六个子维度(分数范围为0-20)：
#             - 开放性（Openness）：想象力、艺术兴趣、情感丰富、冒险性、智力、自由主义
#             - 尽责性（Conscientiousness）：自律、秩序、责任感、成就导向、谨慎、效率
#             - 外向性（Extraversion）：社交性、活力、自信、积极情绪、寻求刺激、健谈
#             - 宜人性（Agreeableness）：信任、诚实、利他主义、顺从、谦逊、同情心
#             - 神经质（Neuroticism）：焦虑、愤怒、抑郁、自我意识、冲动性、脆弱性

#             请分析以下句子，并为每个句子给出这五个维度的评分。请使用以下严格的JSON格式返回结果，JSON的key应该是分析的句子内容，不要包含任何额外的解释：
#             ```json
#             {
#             "句子内容1": {
#                 "开放性": [想象力, 艺术兴趣, 情感丰富, 冒险性, 智力, 自由主义],
#                 "尽责性": [自律, 秩序, 责任感, 成就导向, 谨慎, 效率],
#                 "外向性": [社交性, 活力, 自信, 积极情绪, 寻求刺激, 健谈],
#                 "宜人性": [信任, 诚实, 利他主义, 顺从, 谦逊, 同情心],
#                 "神经质": [焦虑, 愤怒, 抑郁, 自我意识, 冲动性, 脆弱性]
#             },
#             "句子内容2": {
#                 "开放性": [想象力, 艺术兴趣, 情感丰富, 冒险性, 智力, 自由主义],
#                 "尽责性": [自律, 秩序, 责任感, 成就导向, 谨慎, 效率],
#                 "外向性": [社交性, 活力, 自信, 积极情绪, 寻求刺激, 健谈],
#                 "宜人性": [信任, 诚实, 利他主义, 顺从, 谦逊, 同情心],
#                 "神经质": [焦虑, 愤怒, 抑郁, 自我意识, 冲动性, 脆弱性]
#             }
#             }
#             以下是需要分析的句子：
            
#             """
   
#     for i, sentence in enumerate(sentences):
#         prompt += f"\n{i+1}. {sentence}"

#     try:
#         response = openai.ChatCompletion.create(
#             model="ep-20250302223513-s987j",  # 使用你的模型
#             messages=[
#                 {"role": "system", "content": "你是一位精通心理学的专家，擅长评估文本的大五人格特质。你只返回JSON格式的结果，不包含任何额外的解释。"},
#                 {"role": "user", "content": prompt}
#             ],
#             api_base="https://ark.cn-beijing.volces.com/api/v3",
#             api_key='6cf4e49c-c8d8-46d7-b123-a7dcdf16b33f'  # 使用你的API密钥
#         )
        
#         # 提取响应内容
#         content = response["choices"][0]["message"]["content"].strip()
        
#         # 提取JSON部分
#         json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
#         if json_match:
#             json_str = json_match.group(1)
#         else:
#             # 如果没有代码块，尝试提取类似JSON的内容
#             json_start = content.find('{')
#             json_end = content.rfind('}') + 1
#             if json_start >= 0 and json_end > json_start:
#                 json_str = content[json_start:json_end]
#             else:
#                 json_str = content
        
#         # 解析JSON响应
#         scores_dict = json.loads(json_str)
#         return scores_dict

#     except Exception as e:
#         print(f"Error: {e}")
#         # 如果出错，返回空字典
#         return {sentence: {dim: [0] * 6 for dim in big_five_dimensions.keys()} for sentence in sentences}

def get_big_five_scores(text):
    
    sentences = re.split(r'[。！？!?.]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Create a more specific prompt with clear instructions
    prompt = """
你是一位精通心理学的专家，负责评估文本中的大五人格特质。对于每个句子，请根据其内容，分析并给出以下五个维度的评分（范围为0到20）：
- 开放性（Openness）：对新体验、新思想的接受程度
- 尽责性（Conscientiousness）：组织性、可靠性和自律性
- 外向性（Extraversion）：社交性、精力和积极情绪
- 宜人性（Agreeableness）：合作性、同情心和利他主义
- 神经质（Neuroticism）：情绪不稳定性和负面情绪倾向

请分析以下句子，并为每个句子给出这五个维度的评分。请使用以下严格的JSON格式返回结果，不要包含任何额外的解释：
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
    
    return scores

if __name__ == "__main__":
    # input_text = "Player3的发言暂时可以认好，大家别急着踩他。平安夜信息量少，狼人肯定在搅混水，注意谁急着分票。守卫女巫自己判断要不要藏，预言家该跳的时候自然会跳，咱们稳扎稳打别送轮次"
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
            score = analyze_game_text(Player_content)
            player_day_data["big_five_scores"]=  score
            day_time_data.append(player_day_data)
        final_daytime_speech_data['logs'][day_time_key] = day_time_data
    print(final_daytime_speech_data)
    with open('1.json',mode='w',encoding='utf8') as f:
        json.dump(final_daytime_speech_data,f,ensure_ascii=False)
