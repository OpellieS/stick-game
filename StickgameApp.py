# app.py
import random as rd
import streamlit as st

st.set_page_config(page_title="เกมหยิบไม้ (Misère 1-heap)", page_icon="🪵", layout="centered")

# =========================
# ฟังก์ชันช่วย
# =========================
def init_state():
    st.session_state.name_ = ""
    st.session_state.numstick_init = 21
    st.session_state.max_pick = 3
    st.session_state.numstick = None
    st.session_state.user_turn = True
    st.session_state.turn_count = 0
    st.session_state.game_over = False
    st.session_state.log = []
    st.session_state.started = False

def start_game():
    st.session_state.numstick = st.session_state.numstick_init
    st.session_state.user_turn = True
    st.session_state.turn_count = 0
    st.session_state.game_over = False
    st.session_state.log = [f"เริ่มเกมด้วยไม้ {st.session_state.numstick} แท่ง | หยิบได้สูงสุดครั้งละ {st.session_state.max_pick} แท่ง"]
    st.session_state.started = True

def reset_game():
    init_state()

def ai_pick(numstick, max_pick):
    """
    กลยุทธ์เดียวกับโค้ดต้นฉบับ:
    - นิยาม 'ตำแหน่งแพ้' = 1, (k+2), (2k+3), ... หรือเลขที่เหลือเศษ 1 เมื่อหารด้วย (k+1)
    - AI จะเลือก i ทำให้ (numstick - i) เป็นตำแหน่งแพ้
    - ถ้าหาไม่ได้ ให้สุ่มเลือกแบบปลอดภัยในช่วง [1, min(max_pick, numstick)] (ถ้าเหลือ 1 ให้หยิบ 1)
    """
    losing_positions = list(range(1, numstick + 1, max_pick + 1))
    for i in range(max_pick, 0, -1):
        if numstick >= i and (numstick - i) in losing_positions:
            return i
    # ทางเลือก fallback
    return 1 if numstick == 1 else rd.randint(1, min(max_pick, numstick))

def user_move(take_n):
    if st.session_state.game_over or not st.session_state.started:
        return

    n = take_n
    if n < 1 or n > st.session_state.max_pick:
        st.warning(f"คุณหยิบได้แค่ 1 ถึง {st.session_state.max_pick} แท่งเท่านั้น")
        return
    if n > st.session_state.numstick:
        st.warning(f"จำนวนไม้ไม่พอสำหรับหยิบ {n} แท่ง")
        return

    st.session_state.numstick -= n
    st.session_state.turn_count += 1
    st.session_state.log.append(f"👤 {st.session_state.name_} หยิบ {n} แท่ง → เหลือ {st.session_state.numstick}")

    # กติกา: ใครหยิบ 'แท่งสุดท้าย' แพ้
    if st.session_state.numstick == 0:
        st.session_state.game_over = True
        st.session_state.log.append("❌ คุณหยิบแท่งสุดท้าย คุณแพ้!")
        return
    else:
        st.session_state.user_turn = False
        ai_move()  # ให้ AI เดินทันทีในเทิร์นเดียวกัน

def ai_move():
    if st.session_state.game_over or not st.session_state.started:
        return

    st.session_state.log.append("🤖 ตา AI คิดอยู่...")
    pick = ai_pick(st.session_state.numstick, st.session_state.max_pick)

    st.session_state.numstick -= pick
    st.session_state.turn_count += 1
    st.session_state.log.append(f"🤖 AI หยิบ {pick} แท่ง → เหลือ {st.session_state.numstick}")

    if st.session_state.numstick == 0:
        # ถ้า AI หยิบแท่งสุดท้าย = AI แพ้ → ผู้เล่นชนะ
        st.session_state.game_over = True
        st.session_state.log.append("🎉 AI หยิบแท่งสุดท้าย คุณชนะ!")
    else:
        st.session_state.user_turn = True

# =========================
# เริ่มต้น state
# =========================
if "started" not in st.session_state:
    init_state()

# =========================
# ส่วนหัว + คำอธิบาย
# =========================
st.title("🪵 เกมหยิบไม้ (ใครหยิบไม้แท่งสุดท้ายแพ้)")
st.caption("กติกา: มีไม้จำนวนหนึ่ง กำหนดจำนวนสูงสุดที่หยิบได้ต่อเทิร์น ผลัดกันหยิบ 1..K แท่ง ใครหยิบ ‘แท่งสุดท้าย’ แพ้")

# =========================
# แถบด้านข้าง: ตั้งค่าเกม
# =========================
with st.sidebar:
    st.header("ตั้งค่าเกม")
    st.text_input("ชื่อผู้เล่น", key="name_", placeholder="พิมพ์ชื่อของคุณ", disabled=st.session_state.started)
    st.number_input("จำนวนไม้เริ่มต้น", min_value=3, max_value=200, value=st.session_state.numstick_init, step=1, key="numstick_init", disabled=st.session_state.started)
    st.number_input("หยิบได้สูงสุดต่อเทิร์น", min_value=1, max_value=20, value=st.session_state.max_pick, step=1, key="max_pick", disabled=st.session_state.started)

    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        if st.button("▶️ เริ่มเกม", use_container_width=True, disabled=st.session_state.started or st.session_state.name_.strip() == ""):
            # ตรวจความสมเหตุสมผลเบื้องต้น
            if st.session_state.max_pick >= st.session_state.numstick_init:
                st.warning("เพื่อให้เกมมีความหมาย กรุณาตั้งค่า 'หยิบได้สูงสุดต่อเทิร์น' ให้น้อยกว่า 'จำนวนไม้เริ่มต้น'")
            else:
                start_game()
    with col_sb2:
        if st.button("🔄 รีเซ็ต", use_container_width=True):
            reset_game()

# =========================
# กระดานเกม
# =========================
st.subheader("กระดานเกม")

if not st.session_state.started:
    st.info("กรุณาตั้งค่าและกด **เริ่มเกม** จากแถบด้านซ้าย")
else:
    # แสดงสถานะปัจจุบัน
    status_cols = st.columns(3)
    status_cols[0].metric("ไม้คงเหลือ", st.session_state.numstick)
    status_cols[1].metric("หยิบได้สูงสุด/เทิร์น", st.session_state.max_pick)
    status_cols[2].metric("จำนวนเทิร์นทั้งหมด", st.session_state.turn_count)

    st.divider()

    # แถวอินพุตของผู้เล่น
    if not st.session_state.game_over:
        if st.session_state.user_turn:
            st.markdown(f"### ตาของ **{st.session_state.name_}**")
            take_n = st.slider(f"เลือกจำนวนไม้ที่จะหยิบ (1 ถึง {st.session_state.max_pick})",
                               min_value=1, max_value=st.session_state.max_pick, value=1, key="take_n_slider")
            go_col1, go_col2 = st.columns([1,1])
            with go_col1:
                if st.button("หยิบไม้", type="primary", use_container_width=True):
                    user_move(take_n)
            with go_col2:
                st.button("ผ่านเทิร์น (ไม่ทำอะไร)", use_container_width=True, disabled=True, help="เกมนี้ต้องหยิบอย่างน้อย 1 แท่งทุกเทิร์น")
        else:
            st.markdown("### ตาของ 🤖 **AI**")
            # ปุ่มบังคับให้ AI เดิน (สำหรับกรณีอยากแยกจังหวะ)
            if st.button("ให้ AI เล่น", use_container_width=True):
                ai_move()
    else:
        # จบเกม
        st.success("เกมจบแล้ว")
        # สรุปผลท้ายเกม
        if len(st.session_state.log) > 0 and ("คุณชนะ" in st.session_state.log[-1] or "คุณแพ้" in st.session_state.log[-1]):
            st.markdown(f"**ผลลัพธ์:** {st.session_state.log[-1]}")
        st.button("เริ่มใหม่", on_click=reset_game)

    st.divider()

    # ไทม์ไลน์การเล่น
    st.markdown("### บันทึกการเดินเกม")
    for i, line in enumerate(st.session_state.log, start=1):
        st.write(f"{i}. {line}")

# =========================
# ทิปส์เชิงกลยุทธ์
# =========================
with st.expander("ดูทิปส์เชิงกลยุทธ์ (ทำไม AI ถึงเก่ง?)"):
    st.markdown(
        """
- ในกติกาที่ **คนหยิบไม้แท่งสุดท้ายจะแพ้** (misère), ตำแหน่งที่ถือว่า "แพ้โดยธรรมชาติ" คือจำนวนไม้ที่เป็นรูป `m×(K+1) + 1`  
  เช่น ถ้า K=3 ตำแหน่งแพ้คือ 1, 5, 9, 13, ...
- AI พยายามหยิบให้เหลือจำนวนไม้เข้า **ตำแหน่งแพ้** สำหรับคู่แข่งทุกครั้ง  
  ซึ่งคือเหตุผลว่าทำไมมันจะคำนวณ `(numstick - i)` ให้ไปอยู่ในชุดตัวเลขนั้น
        """
    )
