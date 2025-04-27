import streamlit as st
import pandas as pd
import random

# セッションステートの初期化（シャッフルして全問使用）
if "questions" not in st.session_state:
    df = pd.read_csv("questions.csv", encoding="shift_jis") 
    st.session_state.questions = df.sample(frac=1, random_state=random.randint(0, 1000)).reset_index(drop=True)  # ✅ 全問題をシャッフル

if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""

st.title("🌟 英単語 穴埋めクイズ")

# 現在の問題を取得
if st.session_state.current_question < len(st.session_state.questions):
    row = st.session_state.questions.iloc[st.session_state.current_question]
    
    st.subheader(f"Q{st.session_state.current_question + 1}")
    st.write(f"**日本語訳**: {row['japanese']}")
    st.write(f"**英文**: {row['sentence']}")

    # **セッションステートがリセットされるたびに入力欄もリセット**
    user_input = st.text_input("英単語を入力してね:", value="", key=f"input_{st.session_state.current_question}")

    if not st.session_state.answered:
        if st.button("答える"):
            st.session_state.user_answer = user_input
            if user_input.strip().lower() == row['answer'].strip().lower():
                st.success("正解！🎉")
                st.session_state.score += 1
            else:
                st.error(f"不正解😢 正解は「{row['answer']}」だよ。")
            st.session_state.answered = True
    
    # 「次の問題へ」ボタンで完全にリセット
    if st.session_state.answered:
        if st.button("次の問題へ"):
            st.session_state.current_question += 1
            st.session_state.answered = False
            st.session_state.user_answer = ""  # 入力をクリア
            st.rerun()

else:
    st.success(f"クイズ終了！あなたの得点は {st.session_state.score} / {len(st.session_state.questions)} 点です！")

    if st.button("もう一回やる！"):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.user_answer = ""  # 入力をクリア
        del st.session_state.questions  # **ゲーム再スタート時に再シャッフル**
        st.rerun()