import streamlit as st
import pandas as pd
import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Velochori Süper Lig", page_icon="⚽", layout="wide")

# --- CSS TASARIMI ---
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: white; }
    .stTable { background-color: #1e293b !important; border-radius: 10px; color: white !important; }
    .match-card {
        background: #1e293b; padding: 15px; border-radius: 10px;
        border-left: 5px solid #16a34a; margin-bottom: 10px;
    }
    h1, h2, h3 { color: #16a34a !important; font-family: 'Arial Black', sans-serif; }
    .team-header { display: flex; align-items: center; gap: 20px; background: #1e293b; padding: 15px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #334155; }
    .status-badge { padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 VELOCHORI SÜPER LİG")

# --- VERİ SAKLAMA (Session State) ---
if 'matches' not in st.session_state:
    st.session_state.matches = {} # Hafta numarasını anahtar olarak tutuyoruz

# --- YAN PANEL: SKOR GİRİŞİ ---
st.sidebar.image("prospor.jpg", width=80) 
st.sidebar.image("billispor.jpg", width=80)
st.sidebar.header("🕹️ Yönetici Paneli")

with st.sidebar.form("score_form"):
    week_input = st.number_input("Hafta Seçin", min_value=11, max_value=20, value=11)
    
    # Seçilen haftanın takımlarını otomatik belirle (Ev/Dep rotasyonu)
    is_even = (week_input % 2 == 0)
    h_team = "Prospor" if is_even else "Billispor"
    a_team = "Billispor" if is_even else "Prospor"
    
    st.write(f"**{week_input}. Hafta Maçı:**")
    st.write(f"{h_team} (Ev) vs {a_team} (Dep)")
    
    c1, c2 = st.columns(2)
    h_score = c1.number_input(f"{h_team}", min_value=0, step=1, key="h_sc")
    a_score = c2.number_input(f"{a_team}", min_value=0, step=1, key="a_sc")
    
    if st.form_submit_button("Skoru Kaydet / Güncelle"):
        st.session_state.matches[week_input] = {
            "Ev": h_team, "EvSkor": h_score,
            "Dep": a_team, "DepSkor": a_score
        }
        st.sidebar.success(f"{week_input}. Hafta skoru güncellendi!")

# --- HESAPLAMA MOTORU ---
def get_standings():
    # 10. Hafta Sonu Sabit Veriler
    stats = {
        "Billispor": {"O": 10, "G": 6, "B": 0, "M": 4, "AG": 15, "YG": 19, "P": 18, "Logo": "billispor.jpg"},
        "Prospor": {"O": 10, "G": 4, "B": 0, "M": 6, "AG": 19, "YG": 15, "P": 12, "Logo": "prospor.jpg"}
    }
    
    # Girilen skorları ekle
    for w, m in st.session_state.matches.items():
        stats[m["Ev"]]["O"] += 1
        stats[m["Dep"]]["O"] += 1
        stats[m["Ev"]]["AG"] += m["EvSkor"]
        stats[m["Ev"]]["YG"] += m["DepSkor"]
        stats[m["Dep"]]["AG"] += m["DepSkor"]
        stats[m["Dep"]]["YG"] += m["EvSkor"]
        
        if m["EvSkor"] > m["DepSkor"]:
            stats[m["Ev"]]["G"] += 1; stats[m["Ev"]]["P"] += 3; stats[m["Dep"]]["M"] += 1
        elif m["EvSkor"] < m["DepSkor"]:
            stats[m["Dep"]]["G"] += 1; stats[m["Dep"]]["P"] += 3; stats[m["Ev"]]["M"] += 1
        else:
            stats[m["Ev"]]["B"] += 1; stats[m["Dep"]]["B"] += 1
            stats[m["Ev"]]["P"] += 1; stats[m["Dep"]]["P"] += 1
            
    df = pd.DataFrame.from_dict(stats, orient='index').reset_index()
    df.columns = ["Takım", "O", "G", "B", "M", "AG", "YG", "P", "Logo"]
    df["Av"] = df["AG"] - df["YG"]
    return df.sort_values(by=["P", "Av"], ascending=False)

# --- ANA SAYFA SEKMELERİ ---
tab1, tab2 = st.tabs(["📊 PUAN DURUMU", "📅 20. HAFTAYA KADAR FİKSTÜR"])

with tab1:
    st.header("Lig Sıralaması")
    current_df = get_standings()
    
    for _, row in current_df.iterrows():
        st.markdown(f"""
        <div class="team-header">
            <img src="file/{row['Logo']}" width="70" style="border-radius:10px;">
            <div style="flex-grow:1">
                <h2 style="margin:0; font-size:1.5em;">{row['Takım'].upper()}</h2>
                <span style="color:#94a3b8">{row['O']} Maç | {row['G']}G {row['B']}B {row['M']}M</span>
            </div>
            <div style="text-align:right">
                <div style="font-size: 2.2em; font-weight: 900; color: #16a34a;">{row['P']} <small style="font-size:0.4em">PUAN</small></div>
                <div style="color:#94a3b8">Av: {row['Av']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.table(current_df[["Takım", "O", "G", "B", "M", "AG", "YG", "Av", "P"]])

with tab2:
    st.header("Sezon Finaline Kadar Maçlar")
    start_date = datetime.date(2026, 3, 22)
    
    # 11. Haftadan 20. Haftaya kadar (10 Hafta)
    for i in range(10):
        w_num = 11 + i
        cur_date = start_date + datetime.timedelta(days=7 * i)
        
        # Ev sahibi değişimi
        h_t = "Prospor" if w_num % 2 == 0 else "Billispor"
        a_t = "Billispor" if h_t == "Prospor" else "Prospor"
        
        status_html = '<span style="color:#94a3b8">⌛ Bekleniyor</span>'
        score_html = "vs"
        
        if w_num in st.session_state.matches:
            m = st.session_state.matches[w_num]
            status_html = '<span style="color:#16a34a">✅ Tamamlandı</span>'
            score_html = f'<b style="font-size:1.5em; padding:0 20px;">{m["EvSkor"]} - {m["DepSkor"]}</b>'
        
        st.markdown(f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="width:120px">
                    <strong style="font-size:1.1em">{w_num}. Hafta</strong><br>
                    <small style="color:#94a3b8">{cur_date.strftime('%d.%m.%Y')}</small>
                </div>
                <div style="flex-grow:1; text-align:center;">
                    <span style="font-size:1.2em">{h_t}</span>
                    {score_html}
                    <span style="font-size:1.2em">{a_t}</span>
                </div>
                <div style="width:120px; text-align:right;">
                    {status_html}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

