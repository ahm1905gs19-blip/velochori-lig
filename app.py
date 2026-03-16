import streamlit as st
import pandas as pd
import datetime
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Velochori Süper Lig", page_icon="⚽", layout="wide")

# --- AÇIK RENK TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    h1, h2, h3 { color: #2d3748 !important; font-family: 'Arial', sans-serif; }
    .main-card {
        background: #ffffff; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 15px;
        border: 1px solid #e2e8f0;
    }
    .match-card {
        background: #ffffff; padding: 15px; border-radius: 10px;
        border-left: 5px solid #38a169; margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .team-text { font-size: 1.2em; font-weight: bold; color: #2d3748; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 VELOCHORI SÜPER LİG")

# --- VERİ ---
if 'matches' not in st.session_state:
    st.session_state.matches = {}

# --- YÖNETİCİ PANELİ ---
st.sidebar.header("🕹️ Yönetici Paneli")
if os.path.exists("prospor.jpg"): st.sidebar.image("prospor.jpg", width=80)
if os.path.exists("billispor.jpg"): st.sidebar.image("billispor.jpg", width=80)

with st.sidebar.form("score_form"):
    week_input = st.number_input("Hafta Seçin", min_value=11, max_value=20, value=11)
    is_even = (week_input % 2 == 0)
    h_team, a_team = ("Prospor", "Billispor") if is_even else ("Billispor", "Prospor")
    
    st.write(f"**{week_input}. Hafta:** {h_team} vs {a_team}")
    h_score = st.number_input(f"{h_team} Skoru", min_value=0, step=1)
    a_score = st.number_input(f"{a_team} Skoru", min_value=0, step=1)
    
    if st.form_submit_button("Skoru Kaydet"):
        st.session_state.matches[week_input] = {"Ev": h_team, "EvSkor": h_score, "Dep": a_team, "DepSkor": a_score}

# --- PUAN DURUMU HESAPLAMA ---
def get_standings():
    stats = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 15, "YG": 19, "P": 18},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 19, "YG": 15, "P": 12}
    }
    for w, m in st.session_state.matches.items():
        stats[m["Ev"]]["O"] += 1; stats[m["Dep"]]["O"] += 1
        stats[m["Ev"]]["AG"] += m["EvSkor"]; stats[m["Ev"]]["YG"] += m["DepSkor"]
        stats[m["Dep"]]["AG"] += m["DepSkor"]; stats[m["Dep"]]["YG"] += m["EvSkor"]
        if m["EvSkor"] > m["DepSkor"]: stats[m["Ev"]]["G"] += 1; stats[m["Ev"]]["P"] += 3; stats[m["Dep"]]["M"] += 1
        elif m["EvSkor"] < m["DepSkor"]: stats[m["Dep"]]["G"] += 1; stats[m["Dep"]]["P"] += 3; stats[m["Ev"]]["M"] += 1
        else: stats[m["Ev"]]["B"] += 1; stats[m["Dep"]]["B"] += 1; stats[m["Ev"]]["P"] += 1; stats[m["Dep"]]["P"] += 1
    df = pd.DataFrame.from_dict(stats, orient='index').reset_index()
    df.columns = ["Takım", "O", "G", "B", "M", "AG", "YG", "P"]
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(by=["P", "Av"], ascending=False)

# --- ARAYÜZ ---
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "📅 FİKSTÜR"])

with tab1:
    current_df = get_standings()
    for _, row in current_df.iterrows():
        st.markdown(f"""
        <div class="main-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="team-text">{row['Takım'].upper()}</span>
                <span style="font-size:1.5em; font-weight:bold; color:#38a169;">{row['P']} Puan</span>
            </div>
            <small style="color:#718096">{row['O']} Maç | {row['G']}G-{row['B']}B-{row['M']}M | Av: {row['Av']}</small>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    start_date = datetime.date(2026, 3, 22)
    for i in range(10):
        w_num = 11 + i
        h_t, a_t = ("Prospor", "Billispor") if w_num % 2 == 0 else ("Billispor", "Prospor")
        status = "✅" if w_num in st.session_state.matches else "⌛"
        score = f"{st.session_state.matches[w_num]['EvSkor']} - {st.session_state.matches[w_num]['DepSkor']}" if w_num in st.session_state.matches else "vs"
        
        st.markdown(f"""
        <div class="match-card">
            {w_num}. Hafta | {h_t} {score} {a_t} | {status}
        </div>
        """, unsafe_allow_html=True)
