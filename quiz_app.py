import streamlit as st
import pandas as pd
import random


# ✅ CSVファイルを読み込む（Shift-JIS用）
df = pd.read_csv("questions.csv", encoding="shift_jis")

# ✅ アプリタイトル
st.title("🌟 英単語 穴埋めクイズ")

# ✅ ID範囲をユーザーに入力させる
start_id = st.number_input("開始IDを入力:", min_value=int(df["id"].min()), max_value=int(df["id"].max()), value=int(df["id"].min()))
end_id = st.number_input("終了IDを入力:", min_value=int(df["id"].min()), max_value=int(df["id"].max()), value=int(df["id"].max()))

if st.button("クイズを開始！"):
    selected_questions = df[(df["id"] >= start_id) & (df["id"] <= end_id)].sample(frac=1, random_state=random.randint(0, 1000)).reset_index(drop=True)

    if selected_questions.empty:
        st.warning("選択した範囲の問題がありません！IDを確認してください。")
    else:
        st.session_state.questions = selected_questions
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.user_answer = ""
        st.session_state.incorrect_questions = []
        st.rerun()

# ✅ クイズ開始後だけ動く
if "questions" in st.session_state and len(st.session_state.questions) > 0:
    if st.session_state.current_question < len(st.session_state.questions):
        row = st.session_state.questions.iloc[st.session_state.current_question]

        st.subheader(f"Q{st.session_state.current_question + 1}（No.{row['id']}）")
        st.write(f"**日本語訳**: {row['japanese']}")
        st.write(f"**英文**: {row['sentence']}")

        user_input = st.text_input("英単語を入力してね:", value="", key=f"input_{st.session_state.current_question}")

        if not st.session_state.answered:
            if st.button("答える"):
                st.session_state.user_answer = user_input
                if user_input.strip().lower() == row['answer'].strip().lower():
                    st.success("正解！🎉")
                    st.session_state.score += 1
                else:
                    st.error(f"不正解😢 正解は「{row['answer']}」だよ。")
                    st.session_state.incorrect_questions.append(row)
                st.session_state.answered = True

        if st.session_state.answered:
            if st.button("次の問題へ"):
                st.session_state.current_question += 1
                st.session_state.answered = False
                st.session_state.user_answer = ""
                st.rerun()
    else:
        # クイズ終了画面
        st.success(f"クイズ終了！あなたの得点は {st.session_state.score} / {len(st.session_state.questions)} 点です！")

        if len(st.session_state.incorrect_questions) > 0:
            if st.button("間違えた問題だけもう一度やる！"):
                st.session_state.questions = pd.DataFrame(st.session_state.incorrect_questions)
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.answered = False
                st.session_state.user_answer = ""
                st.session_state.incorrect_questions = []
                st.rerun()
        else:
            st.write("全問正解！再挑戦する問題はありません。🎉")

        if st.button("最初からやる！"):
            del st.session_state.questions
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.user_answer = ""
            st.session_state.incorrect_questions = []
            st.rerun()
