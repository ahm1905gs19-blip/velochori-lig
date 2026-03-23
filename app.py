import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

# --- CSS: TÜM TASARIM SİSTEMİ ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@800&display=swap');
.stApp { background: #f0f4f8; font-family: 'Inter', sans-serif; }

.league-title {
    font-size: clamp(24px, 5vw, 45px); font-weight: 900; text-align: center;
    padding: 15px 0; background: linear-gradient(90deg, #059669, #10b981, #34d399, #10b981, #059669);
    background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
}
@keyframes shine { to { background-position: 200% center; } }

/* FORUM TASARIMI */
.forum-post {
    background: white; padding: 15px; border-radius: 12px; margin-bottom: 10px;
    border-left: 5px solid #10b981; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.forum-user { font-weight: 900; color: #1e293b; font-size: 14px; }
.forum-time { font-size: 10px; color: #94a3b8; margin-left: 10px; }
.forum-msg { margin-top: 5px; color: #475569; font-size: 15px; }

.team-card {
    display: flex; justify-content: space-between; align-items: center;
    background: white; padding: 12px 20px; border-radius: 15px;
    margin-bottom: 10px; border: 1px solid #e2e8f0;
}
.leader-card { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); }

.f-dot {
    width: 20px; height: 20px; border-radius: 5px; display: flex; align-items: center; 
    justify-content: center; font-size: 10px; font-weight: 900; color: white; margin-right: 3px;
}
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

.stadium-card {
    background: white; border-radius: 25px; padding: 20px; margin-bottom: 15px; border: 1px solid #e2e8f0;
}
.postponed-card { border: 2px dashed #f59e0b !important; background: #fffaf0; }

.digital-scoreboard {
    background: #0f172a; color: #34d399; font-family: 'JetBrains Mono', monospace;
    font-size: 2.2rem; padding: 10px 25px; border-radius: 15px; text-align: center; 
}
.team-name { font-size: 1.1rem; font-weight: 900; color: #1e293b; text-transform: uppercase; }
.status-pill { font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- SESSION STATE ---
if 'matches' not in st.session_state: st.session_state.matches = {}
if 'forum_messages' not in st.session_state: st.session_state.forum_messages = []

def get_live_stats():
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    for w, m in st.session_state.matches.items():
        data[m["Ev"]]["O"] += 1; data[m["Dep"]]["O"] += 1
        data[m["Ev"]]["AG"] += m["EvSkor"]; data[m["Ev"]]["YG"] += m["DepSkor"]
        data[m["Dep"]]["AG"] += m["DepSkor"]; data[m["Dep"]]["YG"] += m["EvSkor"]
        res = "G" if m["EvSkor"] > m["DepSkor"] else "M" if m["EvSkor"] < m["DepSkor"] else "B"
        data[m["Ev"]]["form"].append(res)
        data[m["Dep"]]["form"].append("G" if res=="M" else "M" if res=="G" else "B")
        if res == "G": data[m["Ev"]]["P"]+=3; data[m["Ev"]]["G"]+=1; data[m["Dep"]]["M"]+=1
        elif res == "M": data[m["Dep"]]["P"]+=3; data[m["Dep"]]["G"]+=1; data[m["Ev"]]["M"]+=1
        else: data[m["Ev"]]["P"]+=1; data[m["Dep"]]["P"]+=1; data[m["Ev"]]["B"]+=1; data[m["Dep"]]["B"]+=1
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🏟️ MAÇ YÖNETİMİ")
    with st.form("score_form"):
        h_no = st.number_input("Hafta", 11, 20, 11)
        ev_s, dep_s = ("Prospor", "Billispor") if h_no % 2 == 0 else ("Billispor", "Prospor")
        c1, c2 = st.columns(2)
        s1 = c1.number_input(f"{ev_s}", 0, 100, 0)
        s2 = c2.number_input(f"{dep_s}", 0, 100, 0)
        if st.form_submit_button("⚽ SKORU İŞLE"):
            st.session_state.matches[h_no] = {"Ev": ev_s, "EvSkor": s1, "Dep": dep_s, "DepSkor": s2}
            st.rerun()

# --- TABLAR ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 TABLO", "🗓️ FİKSTÜR", "🏆 ANALİZ", "💬 FORUM"])

with tab1:
    df = get_live_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        is_l = idx == 0
        f_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f'<div class="team-card {"leader-card" if is_l else ""}"><div style="flex:1;"><span style="font-size:10px; font-weight:900;">{ "🏆 LİDER" if is_l else f"RANK {idx+1}"}</span><h3 style="margin:0;">{r["Takım"].upper()}</h3><div style="display:flex; margin-top:5px;">{f_html}</div></div><div style="font-size:28px; font-weight:900; color:#10b981;">{r["P"]} P</div></div>', unsafe_allow_html=True)

with tab2:
    today = datetime.date.today()
    aylar = {"March": "Mart", "April": "Nisan", "May": "Mayıs"}
    for i in range(10):
        w = 11 + i
        m_dt = today + datetime.timedelta(days=7*i)
        is_today = m_dt == today
        res = st.session_state.matches.get(w)
        is_postponed = is_today and not res # Bugün ve skor yoksa ertelendi
        
        status, s_col, s_bg = ('● BİTTİ', '#166534', '#dcfce7') if res else (('⚠️ ERTELENDİ', '#92400e', '#fef3c7') if is_postponed else ('○ BEKLİYOR', '#64748b', '#f1f5f9'))
        score = f'{res["EvSkor"]} - {res["DepSkor"]}' if res else ('TBD' if is_postponed else 'VS')
        ev_t, dep_t = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")

        st.markdown(f"""
        <div class="stadium-card {'postponed-card' if is_postponed else ''}">
            <div style="display:flex; justify-content:space-between; font-size:12px; font-weight:800; color:#94a3b8; margin-bottom:10px;">
                <span>{w}. HAFTA | 🕒 19:30</span>
                <span style="color:#10b981;">{'📅 BUGÜN' if is_today else m_dt.strftime('%d %B')}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="flex:1; text-align:center;" class="team-name">{ev_t}</div>
                <div class="digital-scoreboard">{score}</div>
                <div style="flex:1; text-align:center;" class="team-name">{dep_t}</div>
            </div>
            <center><div class="status-pill" style="background:{s_bg}; color:{s_col};">{status}</div></center>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.info("Şampiyonluk analizleri bu sekmede yer alıyor.")

with tab4:
    st.subheader("💬 Taraftar Forumu")
    with st.form("forum_form", clear_on_submit=True):
        u_name = st.text_input("Adınız", placeholder="Örn: Billisporlu Ahmet")
        u_msg = st.text_area("Yorumunuz", placeholder="Maç hakkında ne düşünüyorsun?")
        if st.form_submit_button("Gönder"):
            if u_name and u_msg:
                new_post = {"user": u_name, "msg": u_msg, "time": datetime.datetime.now().strftime("%H:%M")}
                st.session_state.forum_messages.insert(0, new_post)
                st.rerun()
            else:
                st.warning("Lütfen her iki alanı da doldurun!")
    
    st.markdown("---")
    if not st.session_state.forum_messages:
        st.write("Henüz yorum yapılmamış. İlk yorumu sen yap!")
    else:
        for post in st.session_state.forum_messages:
            st.markdown(f"""
            <div class="forum-post">
                <span class="forum-user">👤 {post['user']}</span>
                <span class="forum-time">🕒 {post['time']}</span>
                <div class="forum-msg">{post['msg']}</div>
            </div>
            """, unsafe_allow_html=True)
