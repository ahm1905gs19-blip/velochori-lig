st.markdown("""
<style>

/* ANA ARKA PLAN */
.main {
background: linear-gradient(135deg,#e2e8f0,#f8fafc);
color:#0f172a;
}

/* BAŞLIK */
h1{
font-size:48px;
font-weight:900;
text-align:center;
background: linear-gradient(90deg,#16a34a,#22c55e,#4ade80);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:30px;
}

/* TAKIM KARTI */
.team-header{
display:flex;
align-items:center;
gap:20px;
background:white;
padding:18px;
border-radius:15px;
margin-bottom:15px;
border:1px solid #e2e8f0;
transition:all 0.35s ease;
box-shadow:0 5px 15px rgba(0,0,0,0.05);
}

/* HOVER ANİMASYON */
.team-header:hover{
transform:translateY(-5px) scale(1.02);
box-shadow:0 10px 25px rgba(0,0,0,0.15);
border-left:6px solid #22c55e;
}

/* PUAN SAYISI */
.points{
font-size:40px;
font-weight:900;
color:#16a34a;
}

/* FİKSTÜR KARTI */
.match-card{
background:white;
padding:18px;
border-radius:14px;
border-left:6px solid #16a34a;
margin-bottom:12px;
transition:all 0.3s ease;
box-shadow:0 3px 10px rgba(0,0,0,0.08);
}

/* FİKSTÜR HOVER */
.match-card:hover{
transform:scale(1.02);
box-shadow:0 10px 25px rgba(0,0,0,0.15);
}

/* SKOR ANİMASYONU */
.score{
font-size:28px;
font-weight:900;
padding:0 20px;
color:#0f172a;
animation:pulse 2s infinite;
}

/* SKOR PULSE */
@keyframes pulse{
0%{transform:scale(1);}
50%{transform:scale(1.08);}
100%{transform:scale(1);}
}

/* TABLO */
.stTable{
background:white;
border-radius:10px;
box-shadow:0 5px 15px rgba(0,0,0,0.08);
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#16a34a,#15803d);
color:white;
}

</style>
""",unsafe_allow_html=True)
