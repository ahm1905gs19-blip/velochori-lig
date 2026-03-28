import streamlit as st
import pandas as pd
import datetime

# --- 1. SAYFA VE GENEL TASARIM ---
st.set_page_config(page_title="Velochori Ultimate Lig", page_icon="⚽", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@800&display=swap');
.stApp { background: #f0f4f8; font-family: 'Inter', sans-serif; }

/* LİDER İÇİN ÖZEL ALTIN PARLAMA */
@keyframes gold-pulse { 0% { box-shadow: 0 0 0 0 rgba(251, 191, 36, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(251, 191, 36, 0); } 100% { box-shadow: 0 0 0 0 rgba(251, 191, 36, 0); } }
.leader-card { border: 2px solid #fbbf24 !important; background: linear-gradient(135deg, #fffcf0 0%, #ffffff 100%) !important; animation: gold-pulse 2s infinite; }

.team-card {
    display: flex; justify-content: space-between; align-items: center;
    background: white; padding: 12px 18px; border-radius: 12px;
    margin-bottom: 10px; border: 1px solid #e2e8f0;
}

.f-dot { width: 20px; height: 20px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 900; color: white; margin-right: 4px; }
.W { background: #10b981; } .L { background: #ef4444; } .D { background: #94a3b8; }

.points-text { font-size: 28px; font-weight: 900; color: #10b981; }
.digital-scoreboard {
    background: #1e293b; color: #00ff85; font-family: 'JetBrains Mono', monospace;
    font-size: 1.3rem; padding: 8px 18px; border-radius: 10px; min-width: 110px;
    text-align: center; border: 2px solid #334155; box-shadow: inset 0 0 10px #000;
}

.league-title {
    font-size: 36px; font-weight: 900; text-align: center; padding: 20px 0;
    background: linear-gradient(90deg, #059669, #10b981, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# --- 2. VERİLER (BİLLİSPOR 16-15 PROSPOR İŞLENDİ) ---
if 'matches' not in st.session_state:
    # 11. Hafta skorunu senin istediğin gibi doğrudan buraya yazdım
    st.session_state.matches = {
        11: {"Ev": "Billispor", "EvSkor": 16, "Dep": "Prospor", "DepSkor": 15}
    }

def get_live_stats():
    # 10. Hafta Sonu Verileri
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"]}
    }
    
    # 11. Hafta ve sonrasını hesapla
    for w in sorted(st.session_state.matches.keys()):
        m = st.session_state.matches[w]
        data[m["Ev"]]["O"] += 1; data[m["Dep"]]["O"] += 1
        data[m["Ev"]]["AG"] += m["EvSkor"]; data[m["Ev"]]["YG"] += m["DepSkor"]
        data[m["Dep"]]["AG"] += m["DepSkor"]; data[m["Dep"]]["YG"] += m["EvSkor"]
        
        if m["EvSkor"] > m["DepSkor"]:
            data[m["Ev"]]["P"] += 3; data[m["Ev"]]["G"] += 1; data[m["Dep"]]["M"] += 1
            data[m["Ev"]]["form"].append("G"); data[m["Dep"]]["form"].append("M")
        elif m["EvSkor"] < m["DepSkor"]:
            data[m["Dep"]]["P"] += 3; data[m["Dep"]]["G"] += 1; data[m["Ev"]]["M"] += 1
            data[m["Ev"]]["form"].append("M"); data[m["Dep"]]["form"].append("G")
    
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False)

# --- 3. ANA PANEL ---
st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "🗓️ MAÇ MERKEZİ"])

with tab1:
    df = get_live_stats()
    for idx, r in df.reset_index(drop=True).iterrows():
        is_lider = idx == 0
        form_html = "".join([f'<div class="f-dot {"W" if x=="G" else "L" if x=="M" else "D"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"""
        <div class="team-card {'leader-card' if is_lider else ''}">
            <div style="flex:1;">
                <span style="font-size:10px; font-weight:900; color:{'#b45309' if is_lider else '#64748b'};">
                    { '👑 ŞAMPİYONLUK YOLUNDA' if is_lider else f'{idx+1}. SIRADA'}
                </span>
                <div style="font-size:1.1rem; font-weight:800; color:#1e293b;">{r['Takım'].upper()}</div>
                <div style="display:flex; margin-top:5px;">{form_html}</div>
            </div>
            <div style="text-align:right; display:flex; align-items:center; gap:20px;">
                <div style="font-weight:700; color:#64748b;">AV: {r['Av']}</div>
                <div class="points-text">{r['P']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    # 11. Hafta Maçı Görünümü
    w = 11
    res = st.session_state.matches[w]
    st.markdown(f"""
    <div class="stadium-card" style="border: 2px solid #10b981;">
        <div style="background:#f8fafc; padding:10px 15px; display:flex; justify-content:space-between; font-weight:800; font-size:12px;">
            <span>{w}. HAFTA (TAMAMLANDI)</span>
            <span style="color:#10b981;">✅ SKOR ONAYLANDI</span>
        </div>
        <div style="padding:20px; display:flex; align-items:center; justify-content:center;">
            <div style="flex:1; text-align:right; font-weight:800; font-size:1.2rem;">{res['Ev']}</div>
            <div class="digital-scoreboard">{res['EvSkor']} - {res['DepSkor']}</div>
            <div style="flex:1; text-align:left; font-weight:800; font-size:1.2rem;">{res['Dep']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.info("Diğer haftaların skorlarını girmek için sol menüyü kullanabilirsin.")

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Veri Girişi")
    if st.button("Ligi Sıfırla"):
        st.session_state.clear()
        st.rerun()
