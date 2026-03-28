import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

# --- KADRO VE SAHA VERİLERİ ---
teams_squads = {
    "Billispor": {"Kadro": ["Ahmet", "Mehmet", "Can", "Hüseyin", "Burak", "Efe"], "Renk": "#ef4444"},
    "Prospor": {"Kadro": ["Murat", "Selim", "Deniz", "Arda", "Volkan", "Gökhan"], "Renk": "#3b82f6"}
}

# --- CSS: MAÇKOLİK / SOFASCORE TARZI TASARIM ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
.stApp { background: #f1f5f9; font-family: 'Inter', sans-serif; }

/* MAÇ KARTI ANA YAPI */
.match-card-premium {
    background: white; border-radius: 16px; padding: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08); border: 1px solid #e2e8f0;
    margin-bottom: 15px;
}

/* SKOR TABELASI */
.scoreboard-flex {
    display: flex; justify-content: space-around; align-items: center; text-align: center;
}
.team-identity { flex: 1; }
.team-logo-circle {
    width: 60px; height: 60px; border-radius: 50%; background: #f8fafc;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 10px; border: 2px solid #e2e8f0; font-size: 24px;
}
.score-box-premium {
    font-size: 32px; font-weight: 900; color: #1e293b;
    background: #f8fafc; padding: 10px 25px; border-radius: 12px; min-width: 100px;
}

/* SAHA DİZİLİŞİ (VİDEODAKİ GİBİ) */
.pitch-container {
    background: #2d5a27; border-radius: 12px; padding: 20px;
    background-image: linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px);
    background-size: 50px 50px; border: 2px solid #fff; position: relative; margin-top: 15px;
}
.formation-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 20px;
}
.player-pill {
    background: white; color: #1e293b; padding: 5px 10px; border-radius: 6px;
    font-size: 11px; font-weight: 700; margin-bottom: 5px; border-left: 4px solid #fbbf24;
}

/* DETAY BİLGİLER */
.info-strip {
    display: flex; justify-content: center; gap: 20px; margin-top: 15px;
    font-size: 12px; color: #64748b; font-weight: 600;
}

/* ŞAMPİYONLUK KARTI DÜZELTME */
.champ-container {
    background: #0f172a; border-radius: 20px; padding: 30px; color: white; text-align: center;
}
.stat-grid {
    display: flex; justify-content: center; gap: 15px; margin-top: 20px;
}
.stat-item {
    background: rgba(255,255,255,0.1); padding: 15px; border-radius: 12px; min-width: 80px;
}
</style>
""", unsafe_allow_html=True)

# --- VERİ HESAPLAMA ---
if 'matches' not in st.session_state: st.session_state.matches = {}
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

# --- ANA EKRAN ---
tab1, tab2, tab3 = st.tabs(["📊 TABLO", "🗓️ MAÇ MERKEZİ", "🏆 ŞAMPİYONLUK"])

with tab2:
    today = datetime.date.today()
    for i in range(10):
        w = 11 + i
        ev_t, dep_t = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        res = st.session_state.matches.get(w)
        
        with st.expander(f"📍 {w}. HAFTA | {ev_t} - {dep_t}", expanded=(i==0)):
            # Üst Skor Paneli
            score_txt = f"{res['EvSkor']} - {res['DepSkor']}" if res else "18:30"
            st.markdown(f"""
            <div class="match-card-premium">
                <div class="scoreboard-flex">
                    <div class="team-identity">
                        <div class="team-logo-circle" style="border-color:{teams_squads[ev_t]['Renk']}">⚽</div>
                        <div style="font-weight:900;">{ev_t}</div>
                    </div>
                    <div class="score-box-premium">{score_txt}</div>
                    <div class="team-identity">
                        <div class="team-logo-circle" style="border-color:{teams_squads[dep_t]['Renk']}">⚽</div>
                        <div style="font-weight:900;">{dep_t}</div>
                    </div>
                </div>
                <div class="info-strip">
                    <span>🏟️ Velochori Arena</span><span>☁️ Bulutlu, 19°C</span><span>⏱️ 2x20 dk</span>
                </div>
                <div class="pitch-container">
                    <div style="color:white; font-size:10px; font-weight:800; text-align:center; margin-bottom:10px;">İLK 6 DİZİLİŞLERİ</div>
                    <div class="formation-grid">
                        <div>
                            {"".join([f'<div class="player-pill">{p}</div>' for p in teams_squads[ev_t]['Kadro']])}
                        </div>
                        <div style="text-align:right;">
                            {"".join([f'<div class="player-pill" style="border-left:0; border-right:4px solid #fbbf24;">{p}</div>' for p in teams_squads[dep_t]['Kadro']])}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab3:
    df = get_live_stats()
    lider = df.iloc[0]
    # Görseldeki gibi temiz HTML yapısı
    st.markdown(f"""
    <div class="champ-container">
        <div style="font-size:40px;">🏆</div>
        <h1 style="color:white; margin:0;">{lider['Takım'].upper()}</h1>
        <p style="color:#fbbf24; font-weight:800;">LİDERLİK KOLTUĞUNDA</p>
        <div class="stat-grid">
            <div class="stat-item"><div style="font-size:20px; font-weight:900;">{lider['P']}</div><div style="font-size:10px; color:#94a3b8;">PUAN</div></div>
            <div class="stat-item"><div style="font-size:20px; font-weight:900;">{lider['Av']}</div><div style="font-size:10px; color:#94a3b8;">AVERAY</div></div>
            <div class="stat-item"><div style="font-size:20px; font-weight:900;">{20-lider['O']}</div><div style="font-size:10px; color:#94a3b8;">KALAN</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar (Admin)
with st.sidebar:
    st.title("⚙️ PANEL")
    with st.form("score"):
        h = st.number_input("Hafta", 11, 20)
        s1 = st.number_input("Ev", 0)
        s2 = st.number_input("Dep", 0)
        if st.form_submit_button("KAYDET"):
            st.session_state.matches[h] = {"Ev": "Prospor" if h%2==0 else "Billispor", "EvSkor": s1, "Dep": "Billispor" if h%2==0 else "Prospor", "DepSkor": s2}
            st.rerun()
