import streamlit as st

# -------------------------------
# ฟังก์ชันสำหรับ bot ที่เล่นแบบฉลาด
# -------------------------------
def smart_bot_move(stick_all, max_pick):
    """
    คำนวณการหยิบของ bot แบบฉลาด
    พยายามทิ้งไม้ให้ผู้เล่นอยู่ในตำแหน่งที่แพ้เสมอ (loseNumber)
    เช่น ถ้า max_pick = 2 => loseNumber = [1,4,7,10,...]
    """
    lose_nums = [(i * (max_pick + 1) + 1) for i in range(stick_all // (max_pick + 1) + 2)]
    for i in range(1, max_pick + 1):
        if (stick_all - i) in lose_nums:
            return i
    return min(max_pick, stick_all)

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Stick Game", layout="centered")
st.title("🪵 Stick Game (Version 3)")
st.write("Bot จะเล่นแบบฉลาดเพื่อพยายามชนะเสมอ คุณสามารถลองท้าดูได้!")

# Sidebar: setup game
st.sidebar.header("Game Settings")
stick_all = st.sidebar.number_input("จำนวนไม้เริ่มต้น (N):", min_value=5, max_value=100, value=15, step=1)
max_pick = st.sidebar.number_input("จำนวนไม้สูงสุดที่หยิบได้ต่อรอบ:", min_value=2, max_value=5, value=3, step=1)
name = st.sidebar.text_input("กรอกชื่อผู้เล่น:", value="Player")

# Session state
if "stick_all" not in st.session_state:
    st.session_state.stick_all = stick_all
    st.session_state.count = 0
    st.session_state.log = []

# Reset button
if st.sidebar.button("เริ่มเกมใหม่"):
    st.session_state.stick_all = stick_all
    st.session_state.count = 0
    st.session_state.log = []

# Show current state
st.write(f"**ไม้ที่เหลือในกอง: {st.session_state.stick_all}**")

# Display game log
for line in st.session_state.log:
    st.write(line)

# -------------------------------
# Gameplay
# -------------------------------
if st.session_state.stick_all > 0:
    # Bot's turn
    if st.session_state.stick_all == 1:
        bot = 1
    else:
        bot = smart_bot_move(st.session_state.stick_all, max_pick)
    st.session_state.stick_all -= bot
    st.session_state.count += 1
    st.session_state.log.append(f"🤖 Bot หยิบ {bot} ไม้ → เหลือ {st.session_state.stick_all}")

    if st.session_state.stick_all == 0:
        st.success("🎉 Bot หยิบไม้แท่งสุดท้าย → Bot แพ้! คุณชนะ!! 🏆")
    else:
        # Player's turn
        st.write("---")
        st.subheader(f"🎮 {name}'s Turn")
        max_can_pick = min(max_pick, st.session_state.stick_all)
        player_pick = st.number_input(
            f"คุณจะหยิบไม้กี่แท่ง? (1 ถึง {max_can_pick})",
            min_value=1,
            max_value=max_can_pick,
            step=1,
            key="player_input"
        )

        if st.button("หยิบไม้!"):
            st.session_state.stick_all -= player_pick
            st.session_state.count += 1
            st.session_state.log.append(f"🙋 {name} หยิบ {player_pick} ไม้ → เหลือ {st.session_state.stick_all}")

            if st.session_state.stick_all == 0:
                st.error(f"😢 {name} หยิบไม้แท่งสุดท้าย → {name} แพ้!")

st.write("---")
st.write(f"**จำนวนรอบทั้งหมดที่เล่น: {st.session_state.count}**")
