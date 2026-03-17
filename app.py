import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Süper Lig", page_icon="⚽", layout="wide")

# --- CSS TASARIM (Tasarım ve Başlık Korundu) ---
st.markdown("""
<style>
.stApp { background: #fdfdfd; }

/* O GÖSTERİŞLİ BAŞLIK - KORUNDU */
.league-title {
    font-size: clamp(40px, 8vw, 65px);
    font-weight: 950;
    text-align: center;
    padding: 20px 0;
    font-family: 'Arial Black', sans-serif;
    background: linear-gradient(90deg, #16a34a, #22c55e, #4ade80, #22c55e, #16a34a);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
}

@keyframes shine { to { background-position: 200% center; } }

/* TAKIM KARTI */
.team-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 25px 35px;
    border-radius: 24px;
    margin-bottom: 18px;
    border: 1px solid #f1f5f9;
    box-shadow: 0 10px 25px rgba(0,0,0,0.03);
    transition: all 0.4s ease;
}

.leader { 
    border: 2px solid #fbbf24; 
    background: linear-gradient(135deg, #fffdf2 0%, #ffffff 100%); 
}

.points-val { font-size: 42px; font-weight: 900; color: #16a34a; line-height: 1; }
.av-val {
    font-size: 14px; font-weight: 800; color: #64748b;
    background: #f1f5f9; padding: 6px 14px; border-radius: 12px;
}

/* FORM İKONLARI (G-M-B) */
.form-container { display: flex; gap: 5px; margin-top: 8px; }
.form-dot {
    width: 24px; height: 24px; border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 900; color: white;
}
.win { background: #22c55e; }
.loss { background: #ef4444; }

/* FİKSTÜR */
.modern-fixture {
    background: #ffffff;
    border-radius: 20px;
    padding: 20px 30px;
    margin-bottom: 12px;
    border: 1px solid #f8fafc;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- VERİ YÖNETİMİ ---
if 'matches' not in st.session_state: st.session_state.matches = {}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ SKOR MERKEZİ")
    with st.form("ultra_form"):
        w_in = st.number_input("Hafta", 11, 20, 11)
        is_even = w_in % 2 == 0
        h, a = ("Prospor", "Billispor") if is_even else ("Billispor", "Prospor")
        st.info(f"📍 {h} vs {a}")
        col1, col2 = st.columns(2)
        hs = col1.number_input(f"{h}", 0, 100, 0)
        as_ = col2.number_input(f"{a}", 0, 100, 0)
        if st.form_submit_button("✅ SKORU KAYDET"):
            st.session_state.matches[w_in] = {"Ev": h, "EvSkor": hs, "Dep": a, "DepSkor": as_}
            st.rerun()
    
    if st.button("🚨 Verileri Sıfırla"):
        st.session_state.matches = {}
        st.rerun()

# --- HESAPLAMA SİSTEMİ ---
def get_stats():
    # Billispor: Son maç galibiyet (G), ondan önceki mağlubiyet (M)
    # Prospor: Tam tersi
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["M", "G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["G", "M"]}
    }
    
    sorted_weeks = sorted(st.session_state.matches.keys())
    for w in sorted_weeks:
        m = st.session_state.matches[w]
        data[m["Ev"]]["O"] += 1; data[m["Dep"]]["O"] += 1
        data[m["Ev"]]["AG"] += m["EvSkor"]; data[m["Ev"]]["YG"] += m["DepSkor"]
        data[m["Dep"]]["AG"] += m["DepSkor"]; data[m["Dep"]]["YG"] += m["EvSkor"]
        
        if m["EvSkor"] > m["DepSkor"]:
            data[m["Ev"]]["G"] += 1; data[m["Ev"]]["P"] += 3; data[m["Dep"]]["M"] += 1
            data[m["Ev"]]["form"].append("G"); data[m["Dep"]]["form"].append("M")
        elif m["EvSkor"] < m["DepSkor"]:
            data[m["Dep"]]["G"] += 1; data[m["Dep"]]["P"] += 3; data[m["Ev"]]["M"] += 1
            data[m["Ev"]]["form"].append("M"); data[m["Dep"]]["form"].append("G")
        else:
            data[m["Ev"]]["B"] += 1; data[m["Dep"]]["B"] += 1; data[m["Ev"]]["P"] += 1; data[m["Dep"]]["P"] += 1
            data[m["Ev"]]["form"].append("B"); data[m["Dep"]]["form"].append("B")
            
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- ARAYÜZ ---
t1, t2 = st.tabs(["📊 PUAN DURUMU", "🗓️ FİKSTÜR"])

with t1:
    df = get_stats()
    
    for i, r in df.iterrows():
        l_css = "leader" if i == 0 else ""
        # Form göstergesini görselleştirme
        form_html = "".join([f'<div class="form-dot {"win" if x=="G" else "loss" if x=="M" else "draw"}">{x}</div>' for x in r["form"]])
        
        st.markdown(f"""
        <div class="team-card {l_css}">
            <div>
                <span style="color:#94a3b8; font-weight:800; font-size:14px;">SIRALAMA: {i+1}</span>
                <h2 style="margin:0; color:#1e293b; letter-spacing:-1px;">{r['Takım'].upper()}</h2>
                <div class="form-container">
                    <span style="font-size:12px; color:#94a3b8; margin-right:10px; align-self:center;">FORM:</span>
                    {form_html}
                </div>
            </div>
            <div class="stats-right">
                <div style="text-align:right">
                    <div class="av-val">AVERAGE: {r['Av']}</div>
                    <div style="color:#94a3b8; font-size:12px; margin-top:4px;">{r['AG']} AG / {r['YG']} YG</div>
                </div>
                <div class="points-val">{r['P']}<span style="font-size:14px; color:#94a3b8; margin-left:5px;">PTS</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("### 📝 Detaylı Tablo")
    st.dataframe(df[["Takım", "O", "G", "B", "M", "AG", "YG", "Av", "P"]], use_container_width=True, hide_index=True)

with t2:
    start = datetime.date(2026, 3, 22)
    for i in range(10):
        w = 11 + i
        dt = start + datetime.timedelta(days=7*i)
        h_t = "Prospor" if w % 2 == 0 else "Billispor"
        a_t = "Billispor" if h_t == "Prospor" else "Prospor"
        
        done = w in st.session_state.matches
        m_data = st.session_state.matches.get(w)
        
        score = f"<b style='font-size:24px; color:#16a34a;'>{m_data['EvSkor']} - {m_data['DepSkor']}</b>" if done else "VS"
        
        st.markdown(f"""
        <div class="modern-fixture">
            <div style="width:120px;">
                <b style="color:#16a34a; font-size:18px;">{w}. HAFTA</b><br>
                <small style="color:#94a3b8;">{dt.strftime('%d.%m.%Y')}</small>
            </div>
            <div style="flex-grow:1; display:flex; justify-content:center; align-items:center; gap:40px; font-weight:800;">
                <span style="width:120px; text-align:right;">{h_t.upper()}</span>
                {score}
                <span style="width:120px; text-align:left;">{a_t.upper()}</span>
            </div>
            <div style="width:100px; text-align:right;">
                <span style="color:{'#22c55e' if done else '#cbd5e1'};">{'● BİTTİ' if done else '○ BEKLEMEDE'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
