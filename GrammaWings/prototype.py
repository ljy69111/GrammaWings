from api_config import GPT_API, OCR_API, OCR_ID
from openai import OpenAI
from language_cons import language_construct
from pathlib import Path
from ocr import extracted_text

# 初始化 OpenAI 客户端
gpt_api = GPT_API
client = OpenAI(api_key=gpt_api, base_url="https://api.deepseek.com")

def get_answer(question):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are an English teacher. Your tasks are: "
                                              "1. Evaluate and correct students' essays based on grammar, vocabulary, coherence, and content. "
                                              "2. Provide detailed feedback and suggestions for improvement. "
                                              "3. Write a model essay based on the given topic to demonstrate a high-quality response. "
                                              "Your feedback should be clear, constructive, and educational. "
                                              "Your model essays should be well-structured, use appropriate vocabulary, and follow the topic requirements."},
                {"role": "user", "content": question},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"request fail!: {e}"

def main():
    # 用户输入
    grade = input("输入年级\n")
    subject = input("输入题目\n")
    writing_norm = input("输入评分标准（默认为多行评分标准）\n") or '''1.内容要点 (content points)。\n2.运用词汇和语法结构的数量。\n3.词汇的准确运用与句子的结构把握 (accuracy of vocabulary and structures)。\n4.上下文的连贯性(coherence)。'''

    # 读取文件内容
    essay_path = Path('essay_test.txt')
    if not essay_path.exists():
        print("file is not exist！")
        return

    try:
        essay_content = essay_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"读取文件失败: {e}")
        return

    # 生成问题并调用模型
    question = language_construct(grade, subject, writing_norm,essay_content)
    question_with_essay = f"{question}\n\n作文内容如下：\n{essay_content}"
    print("生成的问题:", question_with_essay)

    response = get_answer(question_with_essay)
    print("模型的回答:", response)

if __name__ == "__main__":
    main()
