from pathlib import Path

def language_construct(grade,subject,writing_norm,essay_content)->str:
    question = ("假如你是一个中小学英语老师，请你批改一位" + grade + "年级的同学的作文，作文题目为"+subject+"其中，打分细则如下："
                + writing_norm+"作文内容如下："+essay_content+"请给出批改建议和范文")
    return question


if __name__ == '__main__':
    grade = "3"  # input("grade")""
    subject = '''假定你是李华，当前你在英语学习方面遇到了一些问题。于是你向你校的外籍老师Tom写一封求助信寻求帮助。要点如下：1.本人简介。2.求助内容。3.希望得到Tom的帮助。'''  # input("subject")
    writing_norm = '''1.内容要点 (content points)。
    2.运用词汇和语法结构的数量。
    3.词汇的准确运用与句子的结构把握 (accuracy of vocabulary and structures) 。
    4.上下文的连贯性(coherence)。"#input("writing norm")。'''
    essay_path = Path('essay_test.txt')
    essay_content = essay_path.read_text(encoding='utf-8')
    print(language_construct(grade, subject, writing_norm))