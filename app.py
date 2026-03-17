import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# --- SAYFA AYARI ---
st.set_page_config(page_title="Velochori Süper Lig", page_icon="⚽", layout="wide")

# --- CSS TASARIM (Tasarım ve Başlık Korundu, Fikstür Geliştirildi) ---
st.markdown("""
<style>
.stApp { background: #ffffff; }

/* O GÖSTERİŞLİ BAŞLIK - DOKUNULMADI */
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

/* TAKIM KARTLARI - SIRALAMA TARAFI KORUNDU */
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
}

.leader { border: 2px solid #fbbf24; background: linear-gradient(135deg, #fffdf2 0%, #ffffff 100%); }

.points-val { font-size: 42px; font-weight: 900; color: #16a34a; line-height: 1; }
.av-val { font-size: 14px; font-weight: 800; color: #64748b; background: #f1f5f9; padding: 6px 14px; border-radius: 12px; }

/* FORM İKONLARI */
.form-container { display: flex; gap: 4px; margin-top: 10px; }
.form-dot {
    width: 26px; height: 26px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 900; color: white;
}
.win { background: #22c55e; }
.loss { background: #ef4444; }
.draw { background: #94a3b8; }

/* ULTRA MODERN FİKSTÜR TASARIMI */
.fixture-container {
    background: #f8fafc;
    border-radius: 25px;
    padding: 10px;
    margin-bottom: 20px;
}

.modern-fixture {
    background: #ffffff;
    border-radius: 20px;
    padding: 20px 35px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid #edf2f7;
    transition: all 0.3s ease;
}

.modern-fixture:hover {
    border-color: #22c55e;
    transform: scale(1.005);
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
}

.fixture-info { border-right: 2px solid #f1f5f9; padding-right: 25px; min-width: 140px; }
.fixture-teams { display: flex; align-items: center; justify-content: center; gap: 40px; flex-grow: 1; font-weight: 800; }
.team-name { font-size: 1.2rem; color: #1e293b; width: 150px; }
.score-badge {
    background: #16a34a; color: white; padding: 8px 20px;
    border-radius: 12px; font-size: 1.8rem; font-weight: 900;
    box-shadow: 0 4px 10px rgba(22, 163, 74, 0.2);
}
.vs-circle-modern {
    width: 50px; height: 50px; border: 2px dashed #cbd5e1;
    border-radius: 50%; display: flex; align-items: center;
    justify-content: center; color: #94a3b8; font-size: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="league-title">🏆 VELOCHORI SUPER LEAGUE 🏆</div>', unsafe_allow_html=True)

# --- VERİ YÖNETİMİ ---
if 'matches' not in st.session_state: st.session_state.matches = {}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ SKOR GİRİŞİ")
    with st.form("match_entry"):
        w_in = st.number_input("Hafta Seç", 11, 20, 11)
        h, a = ("Prospor", "Billispor") if w_in % 2 == 0 else ("Billispor", "Prospor")
        st.caption(f"{h} (Ev) vs {a} (Dep)")
        c1, c2 = st.columns(2)
        hs = c1.number_input(f"{h}", 0, 100, 0)
        as_ = c2.number_input(f"{a}", 0, 100, 0)
        if st.form_submit_button("⚽ SONUCU ONAYLA"):
            st.session_state.matches[w_in] = {"Ev": h, "EvSkor": hs, "Dep": a, "DepSkor": as_}
            st.rerun()
    
    if st.button("🗑️ Lig Verilerini Sıfırla"):
        st.session_state.matches = {}
        st.rerun()

# --- HESAPLAMA SİSTEMİ ---
def get_stats():
    # Billispor: Son maç G, ondan önceki M (form verisi)
    data = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 150, "YG": 154, "P": 18, "form": ["G","G","G","M","G"], "p_history": [9,12,15,15,18]},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 154, "YG": 150, "P": 12, "form": ["M","M","M","G","M"], "p_history": [9,9,9,12,12]}
    }
    
    for w in sorted(st.session_state.matches.keys()):
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
        
        data["Billispor"]["p_history"].append(data["Billispor"]["P"])
        data["Prospor"]["p_history"].append(data["Prospor"]["P"])
            
    df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Takım'})
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(["P", "Av"], ascending=False), data

# --- ARAYÜZ ---
t1, t2, t3 = st.tabs(["📊 SIRALAMA", "🗓️ FİKSTÜR MERKEZİ", "📉 PERFORMANS GRAFİĞİ"])

with t1:
    df, raw_data = get_stats()
    for i, r in df.iterrows():
        l_css = "leader" if i == 0 else ""
        form_html = "".join([f'<div class="form-dot {"win" if x=="G" else "loss" if x=="M" else "draw"}">{x}</div>' for x in r["form"][-5:]])
        st.markdown(f"""
        <div class="team-card {l_css}">
            <div>
                <span style="color:#94a3b8; font-weight:800; font-size:12px;">RANK {i+1}</span>
                <h2 style="margin:0; color:#1e293b; font-size:30px;">{r['Takım'].upper()}</h2>
                <div class="form-container">{form_html}</div>
            </div>
            <div class="stats-right">
                <div style="text-align:right">
                    <div class="av-val">AVERAGE: {r['Av']}</div>
                    <div style="color:#94a3b8; font-size:12px; margin-top:4px;">{r['AG']} ATILAN / {r['YG']} YENİLEN</div>
                </div>
                <div class="points-val">{r['P']}<small style="font-size:14px; color:#94a3b8; margin-left:5px;">PTS</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with t2:
    start = datetime.date(2026, 3, 22)
    st.markdown('<div class="fixture-container">', unsafe_allow_html=True)
    for i in range(10):
        w = 11 + i
        dt = start + datetime.timedelta(days=7*i)
        h_t, a_t = ("Prospor", "Billispor") if w % 2 == 0 else ("Billispor", "Prospor")
        m_data = st.session_state.matches.get(w)
        
        score_html = f"<div class='score-badge'>{m_data['EvSkor']} - {m_data['DepSkor']}</div>" if m_data else '<div class="vs-circle-modern">VS</div>'
        status_text = f"<span style='color:#16a34a; font-weight:900;'>OYNANDI</span>" if m_data else "<span style='color:#cbd5e1;'>BEKLİYOR</span>"
        
        st.markdown(f"""
        <div class="modern-fixture">
            <div class="fixture-info">
                <b style="color:#16a34a; font-size:1.1rem;">{w}. HAFTA</b><br>
                <small style="color:#94a3b8;">{dt.strftime('%d.%m.%Y')}</small>
            </div>
            <div class="fixture-teams">
                <span class="team-name" style="text-align:right;">{h_t.upper()} <small style='color:#94a3b8; font-size:10px;'>EV</small></span>
                {score_html}
                <span class="team-name" style="text-align:left;"><small style='color:#94a3b8; font-size:10px;'>DEP</small> {a_t.upper()}</span>
            </div>
            <div style="width:100px; text-align:right;">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with t3:
    df, raw_data = get_stats()
    st.subheader("📈 Puan Gidişatı (Son Maçlar)")
    
    # Grafik Verisi Hazırlama
    chart_data = []
    for team in ["Billispor", "Prospor"]:
        for i, p in enumerate(raw_data[team]["p_history"]):
            chart_data.append({"Hafta": i + 1, "Puan": p, "Takım": team})
    
    plot_df = pd.DataFrame(chart_data)
    fig = px.line(plot_df, x="Hafta", y="Puan", color="Takım", markers=True, 
                  color_discrete_map={"Billispor": "#16a34a", "Prospor": "#ef4444"},
                  template="plotly_white")
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
