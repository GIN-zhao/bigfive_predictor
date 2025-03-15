import openai
import json
import re

def get_big_five_scores(text):
    
    sentences = re.split(r'[。！？!?.]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Create a more specific prompt with clear instructions
    prompt = """
你是一位精通心理学的专家，负责评估文本中的大五人格特质。对于每个句子，请根据其内容，分析并给出以下五个维度的评分（范围为0到1）：
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
    input_text = "Player3的发言暂时可以认好，大家别急着踩他。平安夜信息量少，狼人肯定在搅混水，注意谁急着分票。守卫女巫自己判断要不要藏，预言家该跳的时候自然会跳，咱们稳扎稳打别送轮次"
    output = analyze_game_text(input_text)
    print(json.dumps(output, ensure_ascii=False, indent=4))