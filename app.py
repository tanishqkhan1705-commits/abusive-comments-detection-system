# app.py
# Run with: streamlit run app.py

import streamlit as st
import pandas as pd
from datetime import datetime
from model import classify
from ocr import analyze_image_abuse
from api import get_youtube_comments

st.set_page_config(
    page_title="Abusive Content Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp { background-color: #0d1117; font-family: 'Inter', sans-serif; color: #e6edf3; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1.5rem 2rem 2rem 2rem; max-width: 1400px; }
    .stTextInput > div > div > input { background: #0d1117 !important; border: 1px solid #30363d !important; border-radius: 6px !important; color: #e6edf3 !important; font-size: 0.85rem !important; }
    .stButton > button { background: linear-gradient(135deg, #7c3aed, #5b21b6) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; font-size: 0.9rem !important; width: 100% !important; }
    .stButton > button:hover { background: linear-gradient(135deg, #8b5cf6, #6d28d9) !important; }
    .metric-card { background: #161b22; border: 1px solid #21262d; border-radius: 10px; padding: 1rem 1.2rem; display: flex; align-items: center; gap: 0.9rem; margin-bottom: 0.5rem; }
    .metric-label { font-size: 0.72rem; color: #8b949e; font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.15rem; }
    .metric-value { font-size: 1.6rem; font-weight: 700; color: #e6edf3; line-height: 1; }
    .metric-sub { font-size: 0.72rem; color: #8b949e; margin-top: 0.1rem; }
    .metric-red { font-size: 1.6rem; font-weight: 700; color: #f85149; line-height: 1; }
    .metric-green { font-size: 1.6rem; font-weight: 700; color: #3fb950; line-height: 1; }
    .section-title { font-size: 0.95rem; font-weight: 600; color: #e6edf3; margin: 1.5rem 0 0.8rem 0; padding-bottom: 0.4rem; border-bottom: 1px solid #21262d; }
    .badge-safe { display: inline-block; padding: 0.18rem 0.55rem; border-radius: 20px; font-size: 0.72rem; font-weight: 600; background: rgba(63,185,80,0.15); color: #3fb950; border: 1px solid rgba(63,185,80,0.3); }
    .badge-abusive { display: inline-block; padding: 0.18rem 0.55rem; border-radius: 20px; font-size: 0.72rem; font-weight: 600; background: rgba(248,81,73,0.15); color: #f85149; border: 1px solid rgba(248,81,73,0.3); }
    .badge-category { display: inline-block; padding: 0.18rem 0.55rem; border-radius: 20px; font-size: 0.68rem; font-weight: 500; background: rgba(210,153,34,0.15); color: #e3b341; border: 1px solid rgba(210,153,34,0.3); margin-left: 0.3rem; }
    .comment-row { background: #161b22; border: 1px solid #21262d; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; }
    .comment-author { font-size: 0.78rem; font-weight: 600; color: #58a6ff; margin-bottom: 0.2rem; }
    .comment-text { font-size: 0.85rem; color: #c9d1d9; }
    .comment-score { font-size: 0.73rem; color: #8b949e; margin-top: 0.3rem; }
    .img-card { background: #161b22; border: 1px solid #21262d; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; }
    .img-filename { font-size: 0.82rem; font-weight: 600; color: #e6edf3; margin-bottom: 0.25rem; }
    .img-extracted { font-size: 0.78rem; color: #8b949e; font-style: italic; margin-top: 0.25rem; }
    .banner-green { background: rgba(63,185,80,0.1); border: 1px solid rgba(63,185,80,0.3); border-radius: 8px; padding: 0.8rem 1.2rem; color: #3fb950; font-weight: 500; text-align: center; margin-top: 1rem; }
    .banner-red { background: rgba(248,81,73,0.1); border: 1px solid rgba(248,81,73,0.3); border-radius: 8px; padding: 0.8rem 1.2rem; color: #f85149; font-weight: 500; text-align: center; margin-top: 1rem; }
    .stTabs [data-baseweb="tab-list"] { background: #161b22; border-radius: 8px; padding: 0.2rem; border: 1px solid #21262d; gap: 0.1rem; }
    .stTabs [data-baseweb="tab"] { background: transparent; color: #8b949e; border-radius: 6px; font-size: 0.82rem; }
    .stTabs [aria-selected="true"] { background: #21262d !important; color: #e6edf3 !important; }
    .stSelectbox > div > div { background: #161b22 !important; border: 1px solid #30363d !important; color: #e6edf3 !important; border-radius: 6px !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:1.2rem 0 0.5rem 0; border-bottom:1px solid #21262d; margin-bottom:1.5rem;">
    <h1 style="font-size:1.6rem; font-weight:700; color:#e6edf3; margin:0;">&#128737; Multi-Source Abusive Content Detector</h1>
    <p style="font-size:0.85rem; color:#8b949e; margin:0.2rem 0 0 0;">Analyze comments and images from YouTube using AI</p>
</div>
""", unsafe_allow_html=True)

# ── Input Row ─────────────────────────────────────────────────────────────────
col_yt, col_img, col_btn = st.columns([3, 3, 1.5], gap="medium")

with col_yt:
    st.markdown("**&#9654; YouTube Link**")
    yt_url = st.text_input("yt", placeholder="https://www.youtube.com/watch?v=...", key="yt_input", label_visibility="collapsed")

with col_img:
    st.markdown("**&#128444; Upload Images (OCR)**")
    uploaded_files = st.file_uploader("imgs", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True, key="img_upload", label_visibility="collapsed")
    if uploaded_files:
        st.caption(str(len(uploaded_files)) + " image(s) uploaded")

with col_btn:
    st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)
    fetch_clicked = st.button("⚡ Fetch & Analyze", key="fetch_btn", use_container_width=True)
    st.markdown('<div style="text-align:center;font-size:0.7rem;color:#8b949e;margin-top:0.3rem">Analyzes all comments and images</div>', unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
for key in ["results", "img_results", "analyzed_at"]:
    if key not in st.session_state:
        st.session_state[key] = None
if "page" not in st.session_state:
    st.session_state.page = 1

# ── Fetch & Analyze ───────────────────────────────────────────────────────────
if fetch_clicked:
    if not yt_url.strip() and not uploaded_files:
        st.warning("Please provide a YouTube URL or upload images.")
    else:
        comment_results = []
        img_results = []

        if yt_url.strip():
            with st.spinner("Fetching YouTube comments..."):
                try:
                    raw_comments = get_youtube_comments(yt_url.strip())
                except Exception as e:
                    st.error("YouTube API error: " + str(e))
                    raw_comments = []

            if raw_comments:
                bar = st.progress(0, text="Classifying comments...")
                total = len(raw_comments)
                for i, c in enumerate(raw_comments):
                    res = classify(c["text"])
                    comment_results.append({
                        "author":   c["author"],
                        "text":     c["text"],
                        "label":    res["label"],
                        "score":    res["score"],
                        "category": res["category"]
                    })
                    bar.progress((i + 1) / total, text="Classifying " + str(i+1) + " of " + str(total) + "...")
                bar.empty()

        if uploaded_files:
            with st.spinner("Running OCR on images..."):
                for f in uploaded_files:
                    res = analyze_image_abuse(f)
                    img_results.append({
                       "filename":   f.name,
                       "text":       res.get("text", ""),
                       "label":      res.get("label", "Non-Abusive"),
                       "score":      res.get("score", 0.0),
                       "category":   res.get("category", "safe"),
                       "all_scores": res.get("all_scores", {})
                     })

        st.session_state.results     = comment_results
        st.session_state.img_results = img_results
        st.session_state.analyzed_at = datetime.now().strftime("%I:%M %p  %d %b %Y")
        st.session_state.page = 1
        st.rerun()

# ── Display Results ───────────────────────────────────────────────────────────
if st.session_state.results is not None or st.session_state.img_results is not None:

    comments = st.session_state.results or []
    imgs     = st.session_state.img_results or []

    total_c   = len(comments)
    abusive_c = sum(1 for c in comments if c["label"] == "Abusive")
    safe_c    = total_c - abusive_c
    total_i   = len(imgs)
    abusive_i = sum(1 for i in imgs if i["label"] == "Abusive")
    at        = st.session_state.analyzed_at or ""

    safe_pct    = str(round(safe_c / total_c * 100, 1)) + "%" if total_c else "0%"
    abusive_pct = str(round(abusive_c / total_c * 100, 1)) + "%" if total_c else "0%"

    # ── Metrics ──
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    mc1, mc2, mc3, mc4, mc5 = st.columns(5, gap="small")

    with mc1:
        st.markdown('<div class="metric-card"><div style="font-size:1.4rem">&#128172;</div><div><div class="metric-label">Total Comments</div><div class="metric-value">' + str(total_c) + '</div><div class="metric-sub">Fetched</div></div></div>', unsafe_allow_html=True)

    with mc2:
        cls = "metric-red" if abusive_c > 0 else "metric-green"
        st.markdown('<div class="metric-card"><div style="font-size:1.4rem">&#128737;</div><div><div class="metric-label">Abusive Comments</div><div class="' + cls + '">' + str(abusive_c) + '</div><div class="metric-sub">' + abusive_pct + '</div></div></div>', unsafe_allow_html=True)

    with mc3:
        st.markdown('<div class="metric-card"><div style="font-size:1.4rem">&#9989;</div><div><div class="metric-label">Non-Abusive</div><div class="metric-green">' + str(safe_c) + '</div><div class="metric-sub">' + safe_pct + '</div></div></div>', unsafe_allow_html=True)

    with mc4:
        st.markdown('<div class="metric-card"><div style="font-size:1.4rem">&#128444;</div><div><div class="metric-label">Images Analyzed</div><div class="metric-value">' + str(total_i) + '</div><div class="metric-sub">OCR Extracted</div></div></div>', unsafe_allow_html=True)

    with mc5:
        st.markdown('<div class="metric-card"><div style="font-size:1.4rem">&#128336;</div><div><div class="metric-label">Analyzed At</div><div style="font-size:0.88rem;font-weight:600;color:#e6edf3;line-height:1.4">' + at + '</div></div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    # ── Comments Section ──
    if comments:
        st.markdown('<div class="section-title">&#128172; Comments Analysis</div>', unsafe_allow_html=True)

        fc1, fc2, fc3 = st.columns([2, 3, 1])
        with fc1:
            filter_opt = st.selectbox("Filter", ["All Comments", "Non-Abusive", "Abusive"], key="filter_sel", label_visibility="collapsed")
        with fc2:
            search_q = st.text_input("Search", placeholder="Search comments...", key="search_inp", label_visibility="collapsed")
        with fc3:
            csv = pd.DataFrame(comments).to_csv(index=False).encode("utf-8")
            st.download_button("⬇ Export", data=csv, file_name="results.csv", mime="text/csv", use_container_width=True)

        filtered = comments
        if filter_opt == "Non-Abusive":
            filtered = [c for c in comments if c["label"] == "Non-Abusive"]
        elif filter_opt == "Abusive":
            filtered = [c for c in comments if c["label"] == "Abusive"]
        if search_q.strip():
            q = search_q.lower()
            filtered = [c for c in filtered if q in c["text"].lower() or q in c["author"].lower()]

        PAGE_SIZE   = 10
        total_pages = max(1, (len(filtered) + PAGE_SIZE - 1) // PAGE_SIZE)
        st.session_state.page = min(st.session_state.page, total_pages)
        page_items = filtered[(st.session_state.page - 1) * PAGE_SIZE : st.session_state.page * PAGE_SIZE]

        for c in page_items:
            badge     = '<span class="badge-safe">Non-Abusive</span>' if c["label"] == "Non-Abusive" else '<span class="badge-abusive">Abusive</span>'
            cat_badge = '' if c["category"] == "safe" else '<span class="badge-category">' + c["category"] + '</span>'
            icon      = "✅" if c["label"] == "Non-Abusive" else "⚠️"
            st.markdown(
                '<div class="comment-row">'
                '<div style="flex:1">'
                '<div class="comment-author">' + c["author"] + '</div>'
                '<div class="comment-text">' + c["text"] + '</div>'
                '</div>'
                '<div style="text-align:right;min-width:150px">'
                + badge + cat_badge +
                '<div class="comment-score">Score: ' + str(round(c["score"], 2)) + ' ' + icon + '</div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )

        if total_pages > 1:
            p1, p2, p3 = st.columns([1, 4, 1])
            with p1:
                if st.button("← Prev") and st.session_state.page > 1:
                    st.session_state.page -= 1
                    st.rerun()
            with p2:
                st.markdown('<div style="text-align:center;color:#8b949e;font-size:0.82rem;padding-top:0.5rem">Page ' + str(st.session_state.page) + ' of ' + str(total_pages) + '</div>', unsafe_allow_html=True)
            with p3:
                if st.button("Next →") and st.session_state.page < total_pages:
                    st.session_state.page += 1
                    st.rerun()

    # ── Images Section ──
    if imgs:
        st.markdown('<div class="section-title">&#128444; Image Text Analysis (OCR Results)</div>', unsafe_allow_html=True)

        n_safe  = sum(1 for i in imgs if i["label"] == "Non-Abusive")
        n_abuse = sum(1 for i in imgs if i["label"] == "Abusive")

        tab_all, tab_safe, tab_abuse = st.tabs([
            "All (" + str(len(imgs)) + ")",
            "Non-Abusive (" + str(n_safe) + ")",
            "Abusive (" + str(n_abuse) + ")"
        ])

        def show_img_cards(items):
            for item in items:
                badge    = '<span class="badge-safe">Non-Abusive</span>' if item["label"] == "Non-Abusive" else '<span class="badge-abusive">Abusive</span>'
                cat_b    = '' if item["category"] == "safe" else '<span class="badge-category">' + item["category"] + '</span>'
                raw      = item["text"]
                preview  = (raw[:80] + "...") if len(raw) > 80 else (raw if raw else "No text detected")
                st.markdown(
                    '<div class="img-card">'
                    '<div style="display:flex;justify-content:space-between;align-items:center">'
                    '<div class="img-filename">&#128444; ' + item["filename"] + '</div>'
                    '<div>' + badge + cat_b + ' <span style="color:#8b949e;font-size:0.72rem">Score: ' + str(round(item["score"], 2)) + '</span></div>'
                    '</div>'
                    '<div class="img-extracted">Extracted: "' + preview + '"</div>'
                    '<div class="img-extracted">Scores: ' + str(item.get("all_scores", {})) + '</div>'
                    ,
                    unsafe_allow_html=True
                )

        with tab_all:
            show_img_cards(imgs)
        with tab_safe:
            show_img_cards([i for i in imgs if i["label"] == "Non-Abusive"])
        with tab_abuse:
            show_img_cards([i for i in imgs if i["label"] == "Abusive"])

    # ── Bottom Banner ──
    total_abusive_all = abusive_c + abusive_i
    if total_abusive_all == 0:
        st.markdown('<div class="banner-green">✅ Great news! No abusive content detected in comments or images. This entire dataset is 100% positive!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="banner-red">⚠️ Warning: ' + str(total_abusive_all) + ' abusive item(s) detected. Please review the flagged content above.</div>', unsafe_allow_html=True)
