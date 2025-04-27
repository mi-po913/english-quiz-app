import random
import csv

# ====== ファイルから問題を読み込む ======
questions = []
try:
    with open('questions.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append({"text": row['text'], "answer": row['answer']})
except FileNotFoundError:
    print("エラー: 'questions.csv' が見つかりません。ファイルを確認してください。")
    exit()

# ====== クイズスタート ======
print("=== 英単語穴埋めクイズ ===")
print("10問チャレンジしてみよう！\n")

score = 0
random.shuffle(questions)  # 問題をシャッフル

for i in range(10):
    q = questions[i]
    print(f"Q{i+1}: {q['text']}")
    user_answer = input("単語を入力してください: ").strip()

    if user_answer.lower() == q["answer"].lower():
        print("正解！\n")
        score += 1
    else:
        print(f"不正解！正解は {q['answer']} です。\n")

# ====== 結果発表 ======
print("=== 結果発表 ===")
print(f"あなたの得点は {score}/10 点です！")
if score == 10:
    print("パーフェクト！すごい！！")
elif score >= 7:
    print("いい感じ！この調子！")
else:
    print("もっとがんばろう！")
