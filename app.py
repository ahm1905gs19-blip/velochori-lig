import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Super League", page_icon="⚽", layout="wide")

# --- CSS: SOFASCORE PREMIUM LOOK ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
.stApp { background: #f0f3f6; font-family: 'Inter', sans-serif; }

/* CANLI YAYIN EFEKTİ */
@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
.live-label { 
    color: #ffffff; background: #e91e63; font-weight: 900; font-size: 11px; 
    padding: 2px 8px; border-radius: 4px; animation: pulse 1s infinite;
    display: inline-block; margin-bottom: 5px;
}

/* LİG BAŞLIĞI */
.league-header {
    background: white; padding: 20px; text-align: center; border-bottom: 2px solid #e2e8f0;
    margin-bottom: 20px; border-radius: 0 0 20px 20px;
}
.league-header h1 { color: #00a83e; margin: 0; font-weight: 900; font-size: 28px; }

/* TAKIM KARTLARI */
.puan-kart { 
    background: white; padding: 15px; border-radius: 12px; margin-bottom: 10px;
    border-left: 5px solid #00a83e; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* SAHA TASARIMI (VİDEODAKİ GİBİ) */
.football-pitch {
    background: #2d5a27; border-radius: 15px; padding: 30px 10px; position: relative;
    background-image: linear-gradient(rgba(255,255,255,0.1) 2px, transparent 2px), 
                      linear-gradient(90deg, rgba(255,255,255,0.1) 2px, transparent 2px);
    background-size: 100% 20%; border: 3px solid #4a7c44;
}
.player-circle {
    width: 35px; height: 35px; background: white; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; color: #1e293b; border: 2px solid #fbbf24; margin: 0 auto;
}
.player-name { font-size: 10px; color: white; font-weight: 700; margin-top: 4px; text-align: center; }

/* SKOR TABELASI */
.score-box {
    background: #1e293b; color: #00ff85; font-size: 24px; font-weight: 900;
    padding: 10px 25px; border-radius: 12px; min-width: 120px; display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK ---
st.markdown('<div class="league-header"><h1>🏆 VELOCHORI SUPER LEAGUE</h1></div>', unsafe_allow_html=True)

# --- VERİ VE HESAPLAMA ---
if 'matches' not in st.session_state: st.session_state.matches = {}

def get_stats():
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    for w, m in st.session_state.matches.items():
        data[m["Ev"]]["O"]+=1; data[m["Dep"]]["O"]+=1
        data[m["Ev"]]["AG"]+=m["EvS"]; data[m["Ev"]]["YG"]+=m["DepS"]
        data[m["Dep"]]["AG"]+=m["DepS"]; data[m["Dep"]]["YG"]+=m["EvS"]
        res = "G" if m["EvS"] > m["DepS"] else "M" if m["EvS"] < m["DepS"] else "B"
        data[m["Ev"]]["form"].append(res)
        data[m["Dep"]]["form"].append("G" if res=="M" else "M" if res=="G" else "B")
        if res=="G": data[m["Ev"]]["P"]+=3; data[m["Ev"]]["G"]+=1; data[m["Dep"]]["M"]+=1
        elif res=="M": data[m["Dep"]]["P"]+=3; data[m["Dep"]]["G"]+=1; data[m["Ev"]]["M"]+=1
        else: data[m["Ev"]]["P"]+=1; data[m["Dep"]]["P"]+=1; data[m["Ev"]]["B"]+=1; data[m["Dep"]]["B"]+=1
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- SEKMELER ---
tab1, tab2 = st.tabs(["📊 LİG TABLOSU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = get_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        st.markdown(f"""
        <div class="puan-kart">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color: #64748b; font-size: 12px; font-weight: 800;">SIRA {idx+1}</span>
                    <div style="font-size: 20px; font-weight: 900; color: #1e293b;">{r['Takım'].upper()}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 32px; font-weight: 900; color: #00a83e;">{r['P']} <span style="font-size: 14px; color: #94a3b8;">P</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📈 Detaylı Analiz")
    st.dataframe(df, use_container_width=True, hide_index=True)

with tab2:
    # Gerçek Zaman Kontrolü
    now = datetime.now()
    match_time = time(18, 30)
    match_end = time(20, 15)
    
    for week in range(11, 21):
        if week == 11:
            m_date = datetime(2026, 3, 28)
            arena = "Filia Arena"
        else:
            m_date = datetime(2026, 3, 29) + timedelta(weeks=(week-12))
            arena = "Velochori Arena"
            
        is_today = (now.date() == m_date.date())
        is_live = is_today and (match_time <= now.time() <= match_end)
        
        ev, dep = ("Billispor", "Prospor") if week % 2 != 0 else ("Prospor", "Billispor")
        res = st.session_state.matches.get(week)
        
        # Durum Belirleme
        if res:
            status_text = f"{res['EvS']} - {res['DepS']}"
            sub_label = "MS"
        elif is_live:
            status_text = "OYNANIYOR"
            sub_label = '<div class="live-label">CANLI</div>'
        else:
            status_text = "18:30"
            sub_label = m_date.strftime("%d.%m.%Y")

        with st.expander(f"📅 {m_date.strftime('%d.%m.%Y')} | {week}. Hafta - {ev} vs {dep}", expanded=is_today):
            st.markdown(f"""
            <div style="background: white; border-radius: 15px; padding: 20px; text-align: center; border: 1px solid #e2e8f0;">
                <div style="margin-bottom: 10px; font-size: 13px; font-weight: 700; color: #64748b;">📍 {arena}</div>
                <div style="margin-bottom: 5px;">{sub_label}</div>
                <div style="display: flex; justify-content: space-around; align-items: center; margin-bottom: 20px;">
                    <div style="flex: 1; font-weight: 900; font-size: 20px;">{ev.upper()}</div>
                    <div class="score-box">{status_text}</div>
                    <div style="flex: 1; font-weight: 900; font-size: 20px;">{dep.upper()}</div>
                </div>
                
                <div class="football-pitch">
                    <div style="text-align: center; color: rgba(255,255,255,0.5); font-size: 11px; font-weight: 800; margin-bottom: 20px;">SAHA DİZİLİŞİ</div>
                    <div style="display: flex; justify-content: space-between;">
                        <div style="width: 45%;">
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                                <div><div class="player-circle">?</div><div class="player-name">OYUNCU</div></div>
                                <div><div class="player-circle">?</div><div class="player-name">OYUNCU</div></div>
                                <div><div class="player-circle">?</div><div class="player-name">OYUNCU</div></div>
                                <div><div class="player-circle">?</div><div class="player-name">OYUNCU</div></div>
                            </div>
                        </div>
                        <div style="width: 2px; background: rgba(255,255,255,0.2);"></div>
                        <div style="width: 45%;">
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                                <div><div class="player-circle">?</div><div class="player-name">OYUNCU</div></div>
                                <div><div class="player-circle">?</div><div class="player-name">OYUNCU</div></div>
                                <div><div class="player-circle">?</div><div class="player-name">OYUNCU</div></div>
                                <div><div class="player-circle">?</div><div class="player-name">OYUNCU</div></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- ADMIN ---
with st.sidebar:
    st.header("⚙️ MAÇ SONUCU GİR")
    with st.form("admin_form"):
        h = st.number_input("Hafta", 11, 20)
        s1 = st.number_input("Ev Sahibi Skor", 0)
        s2 = st.number_input("Deplasman Skor", 0)
        if st.form_submit_button("SONUCU KAYDET"):
            ev_t, dep_t = ("Billispor", "Prospor") if h % 2 != 0 else ("Prospor", "Billispor")
            st.session_state.matches[h] = {"Ev": ev_t, "Dep": dep_t, "EvS": s1, "DepS": s2}
            st.success("Skor kaydedildi!")
            st.rerun()
