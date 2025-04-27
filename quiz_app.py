import streamlit as st
import pandas as pd
import random

# ✅ CSVファイルを読み込む（Shift-JISで固定）
df = pd.read_csv("questions.csv", encoding="shift_jis")

# ✅ アプリタイトル
st.title("🌟 英単語 穴埋めクイズ")

# ✅ IDの範囲を選ぶ
start_id = st.number_input(
    "開始IDを入力:",
    min_value=int(df["id"].min()),
    max_value=int(df["id"].max()),
    value=int(df["id"].min())
)
end_id = st.number_input(
    "終了IDを入力:",
    min_value=int(df["id"].min()),
    max_value=int(df["id"].max()),
    value=int(df["id"].max())
)

# ✅ クイズをスタート
if st.button("クイズを開始！"):
    selected = df[(df["id"] >= start_id) & (df["id"] <= end_id)].sample(frac=1).reset_index(drop=True)

    if selected.empty:
        st.warning("選択した範囲の問題がありません！IDを確認してね。")
    else:
        st.session_state.questions = selected
        st.session_state.current = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.wrong = []
        st.rerun()

# ✅ クイズ画面
if "questions" in st.session_state:
    questions = st.session_state.questions
    idx = st.session_state.current

    if idx < len(questions):
        q = questions.iloc[idx]

        st.subheader(f"Q{idx + 1}（No.{q['id']}）")
        st.write(f"**日本語訳**: {q['japanese']}")
        st.write(f"**英文**: {q['sentence']}")

        user_input = st.text_input("英単語を入力してね:", key=f"input_{idx}")

        if not st.session_state.answered:
            if st.button("答える"):
                if user_input.strip().lower() == q['answer'].strip().lower():
                    st.success("正解！🎉")
                    st.session_state.score += 1
                else:
                    st.error(f"不正解😢 正解は「{q['answer']}」だよ。")
                    st.session_state.wrong.append(q)
                st.session_state.answered = True

        if st.session_state.answered:
            if st.button("次の問題へ"):
                st.session_state.current += 1
                st.session_state.answered = False
                st.rerun()
    else:
        st.success(f"クイズ終了！得点は {st.session_state.score} / {len(questions)} 点！")

        if st.session_state.wrong:
            if st.button("間違えた問題だけもう一度やる！"):
                st.session_state.questions = pd.DataFrame(st.session_state.wrong)
                st.session_state.current = 0
                st.session_state.score = 0
                st.session_state.answered = False
                st.session_state.wrong = []
                st.rerun()
        else:
            st.write("全問正解！すごい！🎉")

        if st.button("最初からやる！"):
            for key in ["questions", "current", "score", "answered", "wrong"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
