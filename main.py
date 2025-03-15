import openai
import json

example = """
input: Player 1倒牌太诡异了！要么女巫撒毒手滑，要么守卫神盾挡刀。守卫首夜盲守概率低，我更倾向女巫毒错人！真预言家别急着跳，留着第二晚验人更稳妥。女巫要是没用解药赶紧出来报银水，好人轮次不能落后！
output: {"Player 1倒牌太诡异了！":  [0.4, 0.2, 0.1, 0, 0.2],"要么女巫撒毒手滑，要么守卫神盾挡刀。":  [0.4, 0.2, 0.1, 0, 0.2],"守卫首夜盲守概率低，我更倾向女巫毒错人！":  [0.4, 0.2, 0.1, 0, 0.2],预言家别急着跳，留着第二晚验人更稳妥。”:  [0.4, 0.2, 0.1, 0, 0.2],"女巫要是没用解药赶紧出来报银水，好人轮次不能落后！":  [0.4, 0.2, 0.1, 0, 0.2]}
             
"""

def get_big_five_scores(text):
    """调用 OpenAI API 让模型自动拆分句子并获取 Big Five 评分。"""
    response = openai.ChatCompletion.create(
        model="ep-20250302223513-s987j",
        messages=[
            {"role": "system", "content": "你是一个心理学专家，负责评估文本的 Big Five 评分，范围是 0 到 1。请你先智能为一些句子给出 Big Five 评分。"},
            {"role": "user", "content": f"""请分析以下文本，并对其中一些句子分别评估 Big Five 评分: {text},例如：{example}          
    """
            }
        ],
        api_base="https://ark.cn-beijing.volces.com/api/v3",
        api_key= '6cf4e49c-c8d8-46d7-b123-a7dcdf16b33f'
    )
    
    scores_json = response["choices"][0]["message"]["content"].strip()
    print(scores_json)
    # try:
    #     scores_dict = json.loads(scores_json)
    # except json.JSONDecodeError:
    #     scores_dict = {text: [0, 0, 0, 0, 0]}  # 解析失败时返回默认值
    
    # return json.dumps(scores_dict, ensure_ascii=False, indent=4)
    return None
if __name__ == "__main__":
    input_text = "Player3的发言暂时可以认好，大家别急着踩他。平安夜信息量少，狼人肯定在搅混水，注意谁急着分票。守卫女巫自己判断要不要藏，预言家该跳的时候自然会跳，咱们稳扎稳打别送轮次"
    output = get_big_five_scores(input_text)
    print(output)
