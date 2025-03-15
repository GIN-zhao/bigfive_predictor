import openai
import json

def get_big_five_scores(text):
    """调用 OpenAI API 让模型自动拆分句子并获取 Big Five 评分。"""
    response = openai.ChatCompletion.create(
        model="ep-20250302223513-s987j",
        messages=[
            {"role": "system", "content": "你是一个心理学专家，负责评估文本的 Big Five 评分，范围是 0 到 1。请你先智能拆分输入的文本，并为其中的每个句子给出 Big Five 评分。"},
            {"role": "user", "content": f"请为以下文本拆分并分别评估 Big Five 评分: {text}"}
        ],
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        
    )
    
    scores_json = response["choices"][0]["message"]["content"].strip()
    try:
        scores_dict = json.loads(scores_json)
    except json.JSONDecodeError:
        scores_dict = {text: [0, 0, 0, 0, 0]}  # 解析失败时返回默认值
    
    return json.dumps(scores_dict, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    input_text = "Player 1倒牌太诡异了！要么女巫撒毒手滑，要么守卫神盾挡刀。守卫首夜盲守概率低，我更倾向女巫毒错人！真预言家别急着跳，留着第二晚验人更稳妥。女巫要是没用解药赶紧出来报银水，好人轮次不能落后！"
    output = get_big_five_scores(input_text)
    print(output)
