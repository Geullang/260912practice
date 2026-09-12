import random
import re
from datetime import date
import streamlit as st

st.set_page_config(
    page_title="오늘 체크인",
    page_icon="🌿",
    layout="centered",
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Jua&family=Sunflower:wght@300;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Gowun Dodum', 'Malgun Gothic', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 8%, rgba(255, 250, 206, 0.58) 0, rgba(255, 250, 206, 0) 17%),
        radial-gradient(circle at 86% 12%, rgba(205, 241, 222, 0.72) 0, rgba(205, 241, 222, 0) 22%),
        radial-gradient(circle at 76% 82%, rgba(196, 229, 255, 0.70) 0, rgba(196, 229, 255, 0) 28%),
        linear-gradient(145deg, #eafaf3 0%, #e6f7f5 42%, #e8f4ff 100%);
}

.block-container {
    max-width: 790px;
    padding-top: 2rem;
    padding-bottom: 3.4rem;
}

h1 {
    color: #173f5f !important;
    letter-spacing: -0.025em;
    font-weight: 800 !important;
}

p, label, div {
    color: #24445d;
}

.block-container {
    position: relative;
    z-index: 2;
}
.bg-decor {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.bg-note {
    position: fixed;
    font-family: 'Gowun Dodum', sans-serif;
    font-size: 0.9rem;
    line-height: 1.45;
    color: rgba(83, 119, 122, 0.48);
    letter-spacing: 0.02em;
    white-space: nowrap;
}
.bg-note.n1 { top: 92px; left: 6.5%; transform: rotate(-8deg); }
.bg-note.n2 { top: 160px; right: 8%; transform: rotate(7deg); }
.bg-note.n3 { bottom: 208px; left: 7%; transform: rotate(-6deg); }
.bg-note.n4 { bottom: 130px; right: 9%; transform: rotate(5deg); }
.bg-wave, .bg-leaf {
    position: fixed;
    opacity: 0.42;
}
.bg-wave.w1 { top: 108px; right: 6%; width: 170px; transform: rotate(-6deg); }
.bg-wave.w2 { bottom: 92px; left: 5%; width: 190px; transform: rotate(4deg); opacity: 0.35; }
.bg-leaf.l1 { top: 235px; left: 3%; width: 88px; transform: rotate(-10deg); opacity: 0.36; }
.bg-leaf.l2 { bottom: 220px; right: 3%; width: 94px; transform: rotate(9deg); opacity: 0.30; }
@media (max-width: 760px) {
  .bg-note { font-size: 0.77rem; }
  .bg-wave.w1, .bg-wave.w2 { width: 128px; }
  .bg-leaf.l1, .bg-leaf.l2 { width: 72px; }
}
.st-key-gift_shell {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 0.95rem;
    margin-bottom: 0.1rem;
    text-align: center;
}
.st-key-gift_shell div[data-testid="stButton"] {
    width: 188px;
}
.st-key-gift_shell button {
    width: 188px !important;
    height: 138px !important;
    min-height: 138px !important;
    padding: 0 !important;
    border: none !important;
    border-radius: 28px !important;
    background-image: url("assets/otter_shell_button.png") !important;
    background-size: contain !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-color: transparent !important;
    box-shadow: none !important;
    color: transparent !important;
}
.st-key-gift_shell button p {
    color: transparent !important;
    font-size: 0 !important;
}
.st-key-gift_shell button:hover {
    transform: translateY(-2px) scale(1.015);
    filter: brightness(1.02);
}
.st-key-gift_shell button:focus {
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(68, 148, 130, 0.15) !important;
}

/* Input fields */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    font-family: 'Gowun Dodum', 'Malgun Gothic', sans-serif;
    border-radius: 15px;
    border: 1px solid rgba(83, 136, 151, 0.24);
    background: rgba(255,255,255,0.78);
    box-shadow: 0 3px 12px rgba(58, 102, 116, 0.04);
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(65, 140, 153, 0.55);
    box-shadow: 0 0 0 0.15rem rgba(91, 179, 184, 0.10);
}

/* Main primary form button */
div[data-testid="stForm"] button[kind="primary"],
div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(180deg, #bfe6c7 0%, #a9d8b5 100%) !important;
    color: #b78c2f !important;
    border: 1.4px solid #d8bd72 !important;
    border-radius: 999px !important;
    min-height: 3rem !important;
    font-family: 'Jua', 'Gowun Dodum', sans-serif !important;
    font-size: 1.20rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.02em !important;
    text-shadow: 0 1px 0 rgba(255,255,255,0.45);
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.38),
        0 6px 16px rgba(77, 130, 90, 0.16) !important;
}
div[data-testid="stForm"] button[kind="primary"]:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    background: linear-gradient(180deg, #caecd1 0%, #b4dfbf 100%) !important;
    color: #c09535 !important;
    border-color: #e0c57d !important;
}

/* Letter paper */
.result-box {
    position: relative;
    padding: 2.1rem 1.95rem 1.95rem 3.65rem;
    border-radius: 24px;
    margin-top: 1.1rem;
    background:
        radial-gradient(circle at 18px 24px, rgba(212,205,190,0.92) 0 8px, transparent 8.8px) 0 0 / 100% 48px repeat-y,
        repeating-linear-gradient(
            to bottom,
            rgba(0,0,0,0) 0px,
            rgba(0,0,0,0) 43px,
            rgba(156, 170, 182, 0.21) 43px,
            rgba(156, 170, 182, 0.21) 44px
        ),
        linear-gradient(180deg, rgba(255,252,244,0.98), rgba(253,248,236,0.98));
    border: 1px solid rgba(210, 198, 182, 0.74);
    box-shadow: 0 14px 32px rgba(74, 97, 108, 0.10);
    overflow: hidden;
}

.result-box::after {
    content: "";
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml;utf8,%0A%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20viewBox%3D%270%200%20900%20520%27%3E%0A%20%20%3Cg%20opacity%3D%270.45%27%3E%0A%20%20%20%20%3Cpath%20d%3D%27M790%20320%20C820%20292%2C%20845%20285%2C%20872%20298%27%20fill%3D%27none%27%20stroke%3D%27%238fbe83%27%20stroke-width%3D%276%27%20stroke-linecap%3D%27round%27/%3E%0A%20%20%20%20%3Cpath%20d%3D%27M826%20273%20C816%20242%2C%20819%20216%2C%20837%20196%27%20fill%3D%27none%27%20stroke%3D%27%238fbe83%27%20stroke-width%3D%276%27%20stroke-linecap%3D%27round%27/%3E%0A%20%20%20%20%3Cellipse%20cx%3D%27782%27%20cy%3D%27327%27%20rx%3D%2724%27%20ry%3D%2714%27%20transform%3D%27rotate%28-30%20782%20327%29%27%20fill%3D%27%23b8d89c%27/%3E%0A%20%20%20%20%3Cellipse%20cx%3D%27818%27%20cy%3D%27308%27%20rx%3D%2724%27%20ry%3D%2714%27%20transform%3D%27rotate%2818%20818%20308%29%27%20fill%3D%27%23a8cf90%27/%3E%0A%20%20%20%20%3Cellipse%20cx%3D%27847%27%20cy%3D%27325%27%20rx%3D%2724%27%20ry%3D%2714%27%20transform%3D%27rotate%28-10%20847%20325%29%27%20fill%3D%27%23c0ddaa%27/%3E%0A%20%20%20%20%3Cellipse%20cx%3D%27834%27%20cy%3D%27275%27%20rx%3D%2722%27%20ry%3D%2713%27%20transform%3D%27rotate%2822%20834%20275%29%27%20fill%3D%27%23b2d78f%27/%3E%0A%20%20%3C/g%3E%0A%3C/svg%3E%0A");
    background-repeat: no-repeat;
    background-size: 210px auto;
    background-position: right -4px bottom -6px;
    opacity: 0.72;
    pointer-events: none;
}

.letter-date {
    position: absolute;
    top: 1.25rem;
    right: 1.5rem;
    font-family: 'Gowun Dodum', sans-serif;
    font-size: 0.95rem;
    color: #617379;
    z-index: 2;
}

.letter-body {
    position: relative;
    z-index: 2;
    margin-top: 1.75rem;
    font-family: 'Sunflower', 'Gowun Dodum', sans-serif;
    font-size: 1.22rem;
    line-height: 1.72;
    color: #43494d;
    letter-spacing: -0.01em;
    word-break: keep-all;
}

.letter-greeting {
    display: block;
    margin-bottom: 0.64rem;
    font-weight: 700;
    color: #35484f;
}

.letter-sentence {
    display: block;
    margin-bottom: 0.35rem;
}

.letter-sentence:last-child {
    margin-bottom: 0;
}

.quote-card {
    position: relative;
    padding: 1.75rem 1.95rem 1.65rem 2rem;
    margin-top: 1.15rem;
    border-radius: 26px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.76);
    box-shadow:
        0 12px 28px rgba(74, 112, 132, 0.10),
        inset 0 0 0 1px rgba(255,255,255,0.18);
}

.quote-card::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
}

.quote-card.primary-card {
    background: linear-gradient(135deg, #d7eee2 0%, #d7efe6 46%, #cfe7dd 100%);
}

.quote-card.primary-card::before {
    background-image:
        linear-gradient(90deg, rgba(216,238,226,0.06) 0%, rgba(216,238,226,0.0) 48%, rgba(255,255,255,0.06) 100%),
        url("data:image/svg+xml;utf8,%0A%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20viewBox%3D%270%200%201200%20420%27%3E%0A%20%20%3Cdefs%3E%0A%20%20%20%20%3Cfilter%20id%3D%27b%27%20x%3D%27-20%25%27%20y%3D%27-20%25%27%20width%3D%27140%25%27%20height%3D%27140%25%27%3E%0A%20%20%20%20%20%20%3CfeGaussianBlur%20stdDeviation%3D%2712%27/%3E%0A%20%20%20%20%3C/filter%3E%0A%20%20%3C/defs%3E%0A%20%20%3Ccircle%20cx%3D%27980%27%20cy%3D%27110%27%20r%3D%2758%27%20fill%3D%27rgba%28255%2C255%2C255%2C0.30%29%27%20filter%3D%27url%28%23b%29%27/%3E%0A%20%20%3Ccircle%20cx%3D%271035%27%20cy%3D%27160%27%20r%3D%2728%27%20fill%3D%27rgba%28255%2C255%2C255%2C0.20%29%27%20filter%3D%27url%28%23b%29%27/%3E%0A%20%20%3Ccircle%20cx%3D%27930%27%20cy%3D%27185%27%20r%3D%2722%27%20fill%3D%27rgba%28255%2C255%2C255%2C0.16%29%27%20filter%3D%27url%28%23b%29%27/%3E%0A%20%20%3Cg%20stroke%3D%27%2394c291%27%20stroke-width%3D%277%27%20stroke-linecap%3D%27round%27%20fill%3D%27none%27%20opacity%3D%270.66%27%3E%0A%20%20%20%20%3Cpath%20d%3D%27M930%20390%20C976%20338%2C%201008%20270%2C%201013%20188%27/%3E%0A%20%20%20%20%3Cpath%20d%3D%27M1012%20242%20C1037%20227%2C%201059%20205%2C%201071%20176%27/%3E%0A%20%20%20%20%3Cpath%20d%3D%27M1010%20282%20C1038%20274%2C%201071%20281%2C%201101%20302%27/%3E%0A%20%20%20%20%3Cpath%20d%3D%27M995%20325%20C1020%20336%2C%201042%20354%2C%201061%20382%27/%3E%0A%20%20%3C/g%3E%0A%20%20%3Cg%20fill%3D%27%23b5d9a6%27%20opacity%3D%270.82%27%3E%0A%20%20%20%20%3Cellipse%20cx%3D%271069%27%20cy%3D%27174%27%20rx%3D%2730%27%20ry%3D%2716%27%20transform%3D%27rotate%28-28%201069%20174%29%27/%3E%0A%20%20%20%20%3Cellipse%20cx%3D%271102%27%20cy%3D%27303%27%20rx%3D%2730%27%20ry%3D%2716%27%20transform%3D%27rotate%2818%201102%20303%29%27/%3E%0A%20%20%20%20%3Cellipse%20cx%3D%271054%27%20cy%3D%27226%27%20rx%3D%2732%27%20ry%3D%2717%27%20transform%3D%27rotate%2816%201054%20226%29%27/%3E%0A%20%20%20%20%3Cellipse%20cx%3D%271045%27%20cy%3D%27353%27%20rx%3D%2730%27%20ry%3D%2716%27%20transform%3D%27rotate%2828%201045%20353%29%27/%3E%0A%20%20%3C/g%3E%0A%3C/svg%3E%0A");
    background-repeat: no-repeat, no-repeat;
    background-size: cover, cover;
    background-position: center, center;
}

.quote-card.secondary-card {
    background: linear-gradient(135deg, #d9ecf7 0%, #d6ecf5 50%, #cee3f5 100%);
}

.quote-card.secondary-card::before {
    background-image:
        linear-gradient(90deg, rgba(217,236,247,0.08) 0%, rgba(217,236,247,0.0) 50%, rgba(255,255,255,0.08) 100%),
        url("data:image/svg+xml;utf8,%0A%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20viewBox%3D%270%200%201200%20420%27%3E%0A%20%20%3Cdefs%3E%0A%20%20%20%20%3Cfilter%20id%3D%27b%27%20x%3D%27-20%25%27%20y%3D%27-20%25%27%20width%3D%27140%25%27%20height%3D%27140%25%27%3E%0A%20%20%20%20%20%20%3CfeGaussianBlur%20stdDeviation%3D%2711%27/%3E%0A%20%20%20%20%3C/filter%3E%0A%20%20%3C/defs%3E%0A%20%20%3Ccircle%20cx%3D%27980%27%20cy%3D%27108%27%20r%3D%2754%27%20fill%3D%27rgba%28255%2C255%2C255%2C0.34%29%27%20filter%3D%27url%28%23b%29%27/%3E%0A%20%20%3Ccircle%20cx%3D%271038%27%20cy%3D%27165%27%20r%3D%2728%27%20fill%3D%27rgba%28255%2C255%2C255%2C0.24%29%27%20filter%3D%27url%28%23b%29%27/%3E%0A%20%20%3Ccircle%20cx%3D%27928%27%20cy%3D%27186%27%20r%3D%2720%27%20fill%3D%27rgba%28255%2C255%2C255%2C0.18%29%27%20filter%3D%27url%28%23b%29%27/%3E%0A%20%20%3Cg%20fill%3D%27none%27%20stroke%3D%27rgba%28132%2C185%2C219%2C0.48%29%27%20stroke-width%3D%276%27%20stroke-linecap%3D%27round%27%3E%0A%20%20%20%20%3Cpath%20d%3D%27M850%20284%20C900%20262%2C%20958%20262%2C%201020%20290%27/%3E%0A%20%20%20%20%3Cpath%20d%3D%27M874%20315%20C930%20292%2C%20988%20294%2C%201054%20323%27/%3E%0A%20%20%20%20%3Cpath%20d%3D%27M898%20346%20C954%20327%2C%201016%20330%2C%201082%20360%27/%3E%0A%20%20%3C/g%3E%0A%3C/svg%3E%0A");
    background-repeat: no-repeat, no-repeat;
    background-size: cover, cover;
    background-position: center, center;
}

.quote-inner {
    position: relative;
    z-index: 2;
}

.quote-title {
    font-size: 1.06rem;
    font-family: 'Gowun Dodum', sans-serif;
    font-weight: 700;
    letter-spacing: -0.01em;
    margin-bottom: 0.82rem;
    color: #2a625e;
}

.quote-title::before {
    content: "🍃";
    display: inline-block;
    margin-right: 0.38rem;
    font-size: 1.0rem;
    vertical-align: 0.02rem;
}

.quote-text {
    font-size: 1.44rem;
    line-height: 1.58;
    font-family: 'Sunflower', 'Gowun Dodum', sans-serif;
    font-weight: 500;
    letter-spacing: -0.02em;
    margin-bottom: 0.55rem;
    color: #1e4867;
    word-break: keep-all;
    max-width: 64%;
}

.quote-text br {
    line-height: 1.92;
}

.quote-meta {
    font-size: 0.98rem;
    font-family: 'Gowun Dodum', sans-serif;
    font-weight: 400;
    color: #607a83;
}

.quote-note {
    position: absolute;
    right: 1.5rem;
    bottom: 1.2rem;
    font-family: 'Gowun Dodum', sans-serif;
    font-size: 0.92rem;
    line-height: 1.45;
    text-align: right;
    color: rgba(255, 255, 255, 0.88);
    text-shadow: 0 1px 5px rgba(49, 78, 97, 0.16);
}

.st-key-gift_shell {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 0.2rem;
    margin-bottom: 0.0rem;
    text-align: center;
}

.st-key-gift_shell div[data-testid="stButton"] {
    width: 190px;
}

.st-key-gift_shell button {
    width: 190px !important;
    height: 138px !important;
    min-height: 138px !important;
    padding: 0 !important;
    border: none !important;
    border-radius: 28px !important;
    background-image: url("data:image/png;base64,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...");
    background-size: contain !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-color: transparent !important;
    box-shadow: none !important;
}
.st-key-gift_shell button p {
    visibility: hidden !important;
}
.st-key-gift_shell button:hover {
    transform: translateY(-2px);
    box-shadow: none !important;
}
.st-key-gift_shell button:focus {
    box-shadow: none !important;
}
.gift-hint {
    text-align: center;
    margin-top: -0.12rem;
    margin-bottom: 0.35rem;
    font-family: 'Gowun Dodum', sans-serif;
    font-size: 0.86rem;
    color: rgba(55, 92, 104, 0.72);
}

.otter-static {
    display: flex;
    justify-content: center;
    margin-top: -0.15rem;
    margin-bottom: -0.15rem;
}

.otter-static img {
    width: 170px;
    height: auto;
}

@media (max-width: 760px) {
    .result-box {
        padding: 1.9rem 1.25rem 1.7rem 3.1rem;
    }
    .letter-date {
        font-size: 0.88rem;
        right: 1.1rem;
    }
    .letter-body {
        font-size: 1.1rem;
        line-height: 1.68;
        margin-top: 1.6rem;
    }
    .quote-card {
        padding: 1.5rem 1.25rem 1.4rem 1.3rem;
    }
    .quote-text {
        font-size: 1.33rem;
        max-width: 66%;
        line-height: 1.56;
    }
    .quote-title {
        font-size: 0.98rem;
    }
    .quote-meta {
        font-size: 0.92rem;
    }
    .quote-note {
        right: 1rem;
        bottom: 0.95rem;
        font-size: 0.82rem;
    }
}

/* Secondary/reset button */
div[data-testid="stButton"] button[kind="secondary"] {
    border-radius: 14px;
    border: 1px solid rgba(72, 127, 143, 0.25);
    background: rgba(255,255,255,0.68);
    color: #31546c;
}

.clarify-note {
    margin-top: -0.15rem;
    margin-bottom: 0.35rem;
    color: #c55f68;
    font-size: 0.97rem;
    font-weight: 700;
    line-height: 1.55;
}

.clarify-sub {
    color: #8b7075;
    font-size: 0.86rem;
    margin-bottom: 0.3rem;
}

.small-note {
    font-size: 0.86rem;
    opacity: 0.62;
    margin-top: 1rem;
    color: #557080;
}


div[data-testid="stForm"] button[kind="primary"] p,
div[data-testid="stFormSubmitButton"] button p {
    color: #b78c2f !important;
    font-family: 'Jua', 'Gowun Dodum', sans-serif !important;
    font-size: 1.20rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.02em !important;
}
div[data-testid="stForm"] button[kind="primary"]:hover p,
div[data-testid="stFormSubmitButton"] button:hover p {
    color: #c09535 !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div class="bg-decor" aria-hidden="true">
        <div class="bg-note n1">좋은 하루가 계속되기를</div>
        <div class="bg-note n2">오늘도, 너의 하루를 응원해</div>
        <div class="bg-note n3">지금도 충분히 좋아</div>
        <div class="bg-note n4">오늘의 속도로 가도 괜찮아</div>
        <img class="bg-wave w1" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScyMzAnIGhlaWdodD0nOTAnIHZpZXdCb3g9JzAgMCAyMzAgOTAnPgogIDxnIGZpbGw9J25vbmUnIHN0cm9rZT0nIzhlZDhlNScgc3Ryb2tlLXdpZHRoPSc0JyBzdHJva2UtbGluZWNhcD0ncm91bmQnIG9wYWNpdHk9JzAuNzUnPgogICAgPHBhdGggZD0nTTEwIDM1IEMgMzUgMTgsIDU4IDE4LCA4MiAzNSBTIDEzMCA1MiwgMTU0IDM1IFMgMjAxIDE4LCAyMjAgMzUnLz4KICAgIDxwYXRoIGQ9J00xOCA1MiBDIDQwIDM4LCA2MSAzOCwgODQgNTIgUyAxMjkgNjYsIDE1MyA1MiBTIDE5OCAzOCwgMjE2IDUyJyBvcGFjaXR5PScwLjY1Jy8+CiAgICA8cGF0aCBkPSdNMjUgNjggQyA0NyA1NiwgNjYgNTYsIDg4IDY4IFMgMTI4IDc5LCAxNTAgNjggUyAxOTMgNTYsIDIwOSA2OCcgb3BhY2l0eT0nMC41Jy8+CiAgPC9nPgo8L3N2Zz4=" />
        <img class="bg-wave w2" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScyMzAnIGhlaWdodD0nOTAnIHZpZXdCb3g9JzAgMCAyMzAgOTAnPgogIDxnIGZpbGw9J25vbmUnIHN0cm9rZT0nIzhlZDhlNScgc3Ryb2tlLXdpZHRoPSc0JyBzdHJva2UtbGluZWNhcD0ncm91bmQnIG9wYWNpdHk9JzAuNzUnPgogICAgPHBhdGggZD0nTTEwIDM1IEMgMzUgMTgsIDU4IDE4LCA4MiAzNSBTIDEzMCA1MiwgMTU0IDM1IFMgMjAxIDE4LCAyMjAgMzUnLz4KICAgIDxwYXRoIGQ9J00xOCA1MiBDIDQwIDM4LCA2MSAzOCwgODQgNTIgUyAxMjkgNjYsIDE1MyA1MiBTIDE5OCAzOCwgMjE2IDUyJyBvcGFjaXR5PScwLjY1Jy8+CiAgICA8cGF0aCBkPSdNMjUgNjggQyA0NyA1NiwgNjYgNTYsIDg4IDY4IFMgMTI4IDc5LCAxNTAgNjggUyAxOTMgNTYsIDIwOSA2OCcgb3BhY2l0eT0nMC41Jy8+CiAgPC9nPgo8L3N2Zz4=" />
        <img class="bg-leaf l1" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScxNDAnIGhlaWdodD0nMTgwJyB2aWV3Qm94PScwIDAgMTQwIDE4MCc+CiAgPGcgZmlsbD0nbm9uZScgc3Ryb2tlPScjN2ZjZjlhJyBzdHJva2Utd2lkdGg9JzMnIHN0cm9rZS1saW5lY2FwPSdyb3VuZCcgc3Ryb2tlLWxpbmVqb2luPSdyb3VuZCcgb3BhY2l0eT0nMC44Jz4KICAgIDxwYXRoIGQ9J002NiAxNjUgQzY1IDEzMCwgNjggOTUsIDcyIDE1Jy8+CiAgICA8cGF0aCBkPSdNNzIgMzQgQzU3IDI4LCA0MyAzMSwgMzIgNDUgQzQ2IDQ4LCA2MCA0NCwgNzIgMzQnLz4KICAgIDxwYXRoIGQ9J003MSA1NSBDODYgNDgsIDEwMSA1MCwgMTEzIDY0IEM5OCA2OCwgODQgNjUsIDcxIDU1Jy8+CiAgICA8cGF0aCBkPSdNNzAgNzggQzU1IDcxLCA0MiA3NSwgMzAgODggQzQ0IDkyLCA1OCA4OSwgNzAgNzgnLz4KICAgIDxwYXRoIGQ9J003MyA5OCBDODggOTAsIDEwMyA5NCwgMTE0IDEwOCBDOTggMTExLCA4NSAxMDksIDczIDk4Jy8+CiAgICA8cGF0aCBkPSdNNjkgMTIxIEM1NCAxMTQsIDQyIDExNywgMzEgMTMwIEM0NCAxMzQsIDU3IDEzMSwgNjkgMTIxJy8+CiAgPC9nPgo8L3N2Zz4=" />
        <img class="bg-leaf l2" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPScxNDAnIGhlaWdodD0nMTgwJyB2aWV3Qm94PScwIDAgMTQwIDE4MCc+CiAgPGcgZmlsbD0nbm9uZScgc3Ryb2tlPScjN2ZjZjlhJyBzdHJva2Utd2lkdGg9JzMnIHN0cm9rZS1saW5lY2FwPSdyb3VuZCcgc3Ryb2tlLWxpbmVqb2luPSdyb3VuZCcgb3BhY2l0eT0nMC44Jz4KICAgIDxwYXRoIGQ9J002NiAxNjUgQzY1IDEzMCwgNjggOTUsIDcyIDE1Jy8+CiAgICA8cGF0aCBkPSdNNzIgMzQgQzU3IDI4LCA0MyAzMSwgMzIgNDUgQzQ2IDQ4LCA2MCA0NCwgNzIgMzQnLz4KICAgIDxwYXRoIGQ9J003MSA1NSBDODYgNDgsIDEwMSA1MCwgMTEzIDY0IEM5OCA2OCwgODQgNjUsIDcxIDU1Jy8+CiAgICA8cGF0aCBkPSdNNzAgNzggQzU1IDcxLCA0MiA3NSwgMzAgODggQzQ0IDkyLCA1OCA4OSwgNzAgNzgnLz4KICAgIDxwYXRoIGQ9J003MyA5OCBDODggOTAsIDEwMyA5NCwgMTE0IDEwOCBDOTggMTExLCA4NSAxMDksIDczIDk4Jy8+CiAgICA8cGF0aCBkPSdNNjkgMTIxIEM1NCAxMTQsIDQyIDExNywgMzEgMTMwIEM0NCAxMzQsIDU3IDEzMSwgNjkgMTIxJy8+CiAgPC9nPgo8L3N2Zz4=" />
    </div>
    """,
    unsafe_allow_html=True,
)

QUOTES = [{'text': '오늘 하루의 빛깔을 바꾸는 것, 그것이 가장 높은 예술이다.', 'author': '헨리 데이비드 소로', 'source': '『Walden』, “Where I Lived, and What I Lived For”', 'type': '산문', 'tags': ['오늘', '관점 전환']}, {'text': '우주는 우리가 바라보는 것보다 더 넓다.', 'author': '헨리 데이비드 소로', 'source': '『Walden』, “Conclusion”', 'type': '산문', 'tags': ['관점 전환', '가능성']}, {'text': '자신을 믿어라. 모든 마음은 그 단단한 줄에 울린다.', 'author': '랠프 월도 에머슨', 'source': '「Self-Reliance」', 'type': '산문', 'tags': ['자기신뢰']}, {'text': '하루하루는 알지 못하는 것을 세월은 많이 가르쳐 준다.', 'author': '랠프 월도 에머슨', 'source': '「Experience」', 'type': '산문', 'tags': ['관점 전환', '위로']}, {'text': '지혜의 변함없는 표지는 평범한 것에서 놀라운 것을 보는 데 있다.', 'author': '랠프 월도 에머슨', 'source': '『Nature』', 'type': '산문', 'tags': ['관점 전환', '오늘']}, {'text': '나는 지금의 나로 존재한다. 그것으로 충분하다.', 'author': '월트 휘트먼', 'source': '「Song of Myself」 20', 'type': '시', 'tags': ['자기신뢰', '위로']}, {'text': '나는 크다. 내 안에는 수많은 모습이 함께 있다.', 'author': '월트 휘트먼', 'source': '「Song of Myself」 51', 'type': '시', 'tags': ['자기이해', '자기신뢰']}, {'text': '이제 나는 행운을 구하지 않는다. 내가 곧 나의 행운이다.', 'author': '월트 휘트먼', 'source': '「Song of the Open Road」', 'type': '시', 'tags': ['자기신뢰', '용기']}, {'text': '나는 지금 보이는 것 말고도 아직 보이지 않는 많은 것이 여기 있다고 믿는다.', 'author': '월트 휘트먼', 'source': '「Song of the Open Road」', 'type': '시', 'tags': ['가능성', '희망']}, {'text': '네가 강과 하늘을 보며 느끼는 것처럼, 나도 그렇게 느꼈다.', 'author': '월트 휘트먼', 'source': '「Crossing Brooklyn Ferry」', 'type': '시', 'tags': ['관계', '위로']}, {'text': '네가 여기 있다는 것. 삶이 계속되고, 너도 그 안에 한 구절을 보탤 수 있다는 것.', 'author': '월트 휘트먼', 'source': '「O Me! O Life!」', 'type': '시', 'tags': ['자기존재', '희망', '자기신뢰']}, {'text': '영원은 수많은 ‘지금’으로 이루어진다.', 'author': '에밀리 디킨슨', 'source': '「Forever—is composed of Nows—」', 'type': '시', 'tags': ['오늘', '관점 전환']}, {'text': '나는 가능성 속에 산다.', 'author': '에밀리 디킨슨', 'source': '「I dwell in Possibility—」', 'type': '시', 'tags': ['가능성', '희망']}, {'text': '우리는 일어서야 할 때가 오기 전까지 자신이 얼마나 높이 오를 수 있는지 모른다.', 'author': '에밀리 디킨슨', 'source': '「We never know how high we are」', 'type': '시', 'tags': ['자기신뢰', '용기', '가능성']}, {'text': '희망은 깃털을 가진 것, 영혼에 내려앉아 노래하는 것.', 'author': '에밀리 디킨슨', 'source': '「“Hope” is the thing with feathers—」', 'type': '시', 'tags': ['희망', '위로']}, {'text': '가장 용감한 사람도 잠시 더듬으며 걷는다.', 'author': '에밀리 디킨슨', 'source': '「We grow accustomed to the Dark」', 'type': '시', 'tags': ['위로', '용기']}, {'text': '새벽이 언제 올지 몰라 나는 모든 문을 열어 둔다.', 'author': '에밀리 디킨슨', 'source': '「Not knowing when the Dawn will come」', 'type': '시', 'tags': ['가능성', '희망']}, {'text': '마음은 하늘보다 넓다.', 'author': '에밀리 디킨슨', 'source': '「The Brain—is wider than the Sky—」', 'type': '시', 'tags': ['자기신뢰', '자기이해']}, {'text': '우리는 세월과 함께 낡아지는 것이 아니라, 날마다 새로워진다.', 'author': '에밀리 디킨슨', 'source': '1874년 편지, 『Letters of Emily Dickinson』', 'type': '서간', 'tags': ['다시 시작', '오늘']}, {'text': '지금은 그 질문들을 살아 보라.', 'author': '라이너 마리아 릴케', 'source': '『Letters to a Young Poet』, Letter 4, 1903.7.16', 'type': '서간', 'tags': ['관점 전환', '오늘', '자기이해']}, {'text': '우리의 의심은 때로, 시도했다면 얻었을 것을 놓치게 한다.', 'author': '윌리엄 셰익스피어', 'source': '『Measure for Measure』 1막 4장', 'type': '희곡', 'tags': ['용기', '가능성']}, {'text': '우리가 찾는 해결책은 종종 우리 자신 안에 있다.', 'author': '윌리엄 셰익스피어', 'source': '『All’s Well That Ends Well』 1막 1장', 'type': '희곡', 'tags': ['자기신뢰', '자기이해']}, {'text': '우리 삶의 실은 좋은 것과 좋지 않은 것이 함께 섞여 짜인다.', 'author': '윌리엄 셰익스피어', 'source': '『All’s Well That Ends Well』 4막 3장', 'type': '희곡', 'tags': ['위로', '관점 전환']}, {'text': '운은 키를 잡지 않은 배도 항구로 데려올 때가 있다.', 'author': '윌리엄 셰익스피어', 'source': '『Cymbeline』 4막 3장', 'type': '희곡', 'tags': ['관점 전환', '희망']}, {'text': '세상에는 우리가 생각해 낸 것보다 더 많은 것이 있다.', 'author': '윌리엄 셰익스피어', 'source': '『Hamlet』 1막 5장', 'type': '희곡', 'tags': ['가능성', '관점 전환']}, {'text': '나는 새가 아니다. 어떤 그물도 나를 가둘 수 없다. 나는 독립된 의지를 가진 자유로운 사람이다.', 'author': '샬럿 브론테', 'source': '『Jane Eyre』 Ch.23', 'type': '소설', 'tags': ['자기신뢰', '용기']}, {'text': '나는 폭풍이 두렵지 않다. 내 배를 다루는 법을 배우고 있으니까.', 'author': '루이자 메이 올컷', 'source': '『Little Women』 Part II, Ch.44', 'type': '소설', 'tags': ['용기', '자기신뢰']}, {'text': '어제로 돌아가도 소용없어. 나는 이미 그때와 다른 사람이니까.', 'author': '루이스 캐럴', 'source': '『Alice’s Adventures in Wonderland』 Ch.10', 'type': '소설', 'tags': ['다시 시작', '오늘']}, {'text': '뒤로만 움직이는 기억이라면 그다지 좋은 기억은 아니지.', 'author': '루이스 캐럴', 'source': '『Through the Looking-Glass』 Ch.5', 'type': '소설', 'tags': ['관점 전환', '다시 시작']}, {'text': '진짜 용기는 두렵지 않은 것이 아니라, 두려운 채로 위험에 맞서는 것이다.', 'author': 'L. 프랭크 바움', 'source': '『The Wonderful Wizard of Oz』 Ch.15', 'type': '소설', 'tags': ['용기', '자기신뢰']}, {'text': '이 순간까지 나는 나 자신을 몰랐다.', 'author': '제인 오스틴', 'source': '『Pride and Prejudice』 Ch.36', 'type': '소설', 'tags': ['자기이해', '관점 전환']}, {'text': '사람의 말 속에 완전한 진실이 그대로 담기는 경우는 아주 드물다.', 'author': '제인 오스틴', 'source': '『Emma』 Ch.49', 'type': '소설', 'tags': ['관점 전환', '관계']}, {'text': '한 가지 일을 여러 관점에서 바라보지 못하는 것은 좁은 생각이다.', 'author': '조지 엘리엇', 'source': '『Middlemarch』 Ch.7', 'type': '소설', 'tags': ['관점 전환']}, {'text': '정의하는 순간, 한계를 긋는다.', 'author': '오스카 와일드', 'source': '『The Picture of Dorian Gray』 Ch.17', 'type': '소설', 'tags': ['자기신뢰', '관점 전환']}, {'text': '사람의 진짜 완성은 무엇을 가졌느냐가 아니라 어떤 사람이냐에 있다.', 'author': '오스카 와일드', 'source': '「The Soul of Man under Socialism」', 'type': '산문', 'tags': ['자기신뢰', '자기이해']}, {'text': '우리는 모두 진흙탕에 있지만, 그중 누군가는 별을 바라본다.', 'author': '오스카 와일드', 'source': '『Lady Windermere’s Fan』 3막', 'type': '희곡', 'tags': ['관점 전환', '희망']}, {'text': '남을 흉내 내 성공하는 것보다 자기 방식으로 실패하는 편이 낫다.', 'author': '허먼 멜빌', 'source': '「Hawthorne and His Mosses」', 'type': '평론', 'tags': ['자기신뢰', '다시 시작']}, {'text': '남의 방식으로 옳기보다 자기 방식으로 틀리는 편이 낫다.', 'author': '표도르 도스토옙스키', 'source': '『Crime and Punishment』 Part III, Ch.1', 'type': '소설', 'tags': ['자기신뢰', '다시 시작']}, {'text': '한 문이 닫히면 다른 문이 열린다.', 'author': '미겔 데 세르반테스', 'source': '『Don Quixote』 Part I, Ch.21', 'type': '소설', 'tags': ['다시 시작', '희망']}, {'text': '희망을 품고 가는 것은 도착하는 것보다 더 나은 일일 때가 있다.', 'author': '로버트 루이스 스티븐슨', 'source': '「El Dorado」', 'type': '산문', 'tags': ['관점 전환', '희망']}, {'text': '겉모습으로 판단하지 말고, 근거를 보라.', 'author': '찰스 디킨스', 'source': '『Great Expectations』 Ch.40', 'type': '소설', 'tags': ['관점 전환']}, {'text': '명백해 보이는 사실만큼 우리를 속이기 쉬운 것도 없다.', 'author': '아서 코난 도일', 'source': '「The Boscombe Valley Mystery」', 'type': '소설', 'tags': ['관점 전환']}, {'text': '자료를 갖기 전에 이론을 세우는 것은 큰 실수다.', 'author': '아서 코난 도일', 'source': '「A Scandal in Bohemia」', 'type': '소설', 'tags': ['관점 전환']}, {'text': '크고 갑작스러운 변화만큼 사람의 마음을 아프게 하는 것도 없다.', 'author': '메리 셸리', 'source': '『Frankenstein』 1818년판, Vol. III, Ch.6', 'type': '소설', 'tags': ['위로', '관점 전환']}, {'text': '삶은 사람들 앞에서 바이올린 독주를 하면서, 연주하는 법을 동시에 배우는 것과 같다.', 'author': '새뮤얼 버틀러', 'source': '「How to Make the Best of Life」', 'type': '산문', 'tags': ['위로', '자기이해']}, {'text': '시간의 좋은 점은 미리 낭비해 버릴 수 없다는 것이다.', 'author': '아널드 베넷', 'source': '『How to Live on 24 Hours a Day』', 'type': '산문', 'tags': ['다시 시작', '오늘']}, {'text': '서두를 필요도, 빛나 보일 필요도, 자기 아닌 다른 사람이 될 필요도 없다.', 'author': '버지니아 울프', 'source': '『A Room of One’s Own』 Ch.1', 'type': '산문', 'tags': ['위로', '자기신뢰']}, {'text': '모험이란, 다르게 바라본 불편함일 뿐이다.', 'author': 'G. K. 체스터턴', 'source': '『All Things Considered』, 「On Running After One’s Hat」', 'type': '산문', 'tags': ['관점 전환', '용기']}, {'text': '어떤 사람은 있는 것을 보며 ‘왜?’라고 묻고, 나는 없던 것을 꿈꾸며 ‘왜 안 돼?’라고 묻는다.', 'author': '조지 버나드 쇼', 'source': '『Back to Methuselah』', 'type': '희곡', 'tags': ['가능성', '용기']}, {'text': '코앞에 있는 것을 제대로 보는 데에도 끊임없는 노력이 필요하다.', 'author': '조지 오웰', 'source': '「In Front of Your Nose」, 1946', 'type': '산문', 'tags': ['관점 전환', '오늘']}, {'text': '절뚝이며 가더라도 뒤로 가는 것은 아니다.', 'author': '칼릴 지브란', 'source': '『The Prophet』, “Good and Evil”', 'type': '산문시', 'tags': ['다시 시작', '위로']}, {'text': '‘진리를 찾았다’고 말하지 말고, ‘하나의 진리를 찾았다’고 말하라.', 'author': '칼릴 지브란', 'source': '『The Prophet』, “Self-Knowledge”', 'type': '산문시', 'tags': ['관점 전환', '자기이해']}, {'text': '오래된 길이 사라진 곳에서 새로운 땅이 경이로움과 함께 모습을 드러낸다.', 'author': '라빈드라나트 타고르', 'source': '『Gitanjali』 37', 'type': '시', 'tags': ['가능성', '다시 시작']}, {'text': '우리는 세상을 잘못 읽고는 세상이 우리를 속였다고 말한다.', 'author': '라빈드라나트 타고르', 'source': '『Stray Birds』 75', 'type': '산문시', 'tags': ['관점 전환']}, {'text': '어떤 일에 대해 꼭 지금 의견을 가져야 하는 것은 아니다.', 'author': '마르쿠스 아우렐리우스', 'source': '『Meditations』 VI.52', 'type': '철학', 'tags': ['관점 전환', '위로']}, {'text': '어떤 것은 우리에게 달려 있고, 어떤 것은 그렇지 않다.', 'author': '에픽테토스', 'source': '『Enchiridion』 §1', 'type': '철학', 'tags': ['관점 전환', '위로']}, {'text': '우리는 현실보다 상상 속에서 더 자주 괴로워한다.', 'author': '세네카', 'source': '『Moral Letters to Lucilius』 Letter 13', 'type': '서간·철학', 'tags': ['관점 전환', '위로']}, {'text': '제비 한 마리가 여름을 만들지 않듯, 하루가 한 사람의 삶 전체를 결정하지 않는다.', 'author': '아리스토텔레스', 'source': '『Nicomachean Ethics』 I.7', 'type': '철학', 'tags': ['위로', '관점 전환']}, {'text': '우리는 해보면서 배운다.', 'author': '아리스토텔레스', 'source': '『Nicomachean Ethics』 II.1', 'type': '철학', 'tags': ['다시 시작', '용기']}, {'text': '세상에서 가장 큰 일은 자기 자신에게 속할 줄 아는 것이다.', 'author': '미셸 드 몽테뉴', 'source': '『Essays』 I, 「Of Solitude」', 'type': '철학', 'tags': ['자기신뢰', '자기이해']}, {'text': '나는 고정된 존재를 그리지 않는다. 변화해 가는 모습을 그린다.', 'author': '미셸 드 몽테뉴', 'source': '『Essays』 III.2, 「Of Repentance」', 'type': '철학', 'tags': ['자기이해', '다시 시작']}, {'text': '확신에서 시작하면 의심으로 끝나고, 의심에서 시작하면 확신에 이를 수 있다.', 'author': '프랜시스 베이컨', 'source': '『The Advancement of Learning』', 'type': '철학', 'tags': ['관점 전환']}, {'text': '진실은 혼란보다 오류를 통해 더 빨리 모습을 드러내기도 한다.', 'author': '프랜시스 베이컨', 'source': '『Novum Organum』 관련 구절', 'type': '철학', 'tags': ['관점 전환', '다시 시작']}, {'text': '다른 사람을 아는 것은 지혜이고, 자기 자신을 아는 것은 밝은 앎이다.', 'author': '노자', 'source': '『도덕경』 33장', 'type': '철학', 'tags': ['자기이해', '자기신뢰']}, {'text': '회오리바람도 아침 내내 불지는 않고, 소나기도 하루 종일 내리지는 않는다.', 'author': '노자', 'source': '『도덕경』 23장', 'type': '철학', 'tags': ['위로', '희망']}, {'text': '아는 것을 안다고 하고, 모르는 것을 모른다고 하는 것. 그것이 아는 것이다.', 'author': '공자', 'source': '『논어』 「위정」 2.17', 'type': '철학', 'tags': ['자기신뢰', '자기이해']}, {'text': '나는 모르는 것을 안다고 생각하지 않는다.', 'author': '플라톤', 'source': '『Apology』 21d, 소크라테스의 말', 'type': '철학', 'tags': ['자기이해', '관점 전환']}, {'text': '지혜로운 사람은 근거에 맞추어 믿음의 정도를 정한다.', 'author': '데이비드 흄', 'source': '『An Enquiry Concerning Human Understanding』 §10', 'type': '철학', 'tags': ['관점 전환']}, {'text': '철학자가 되어라. 그러나 철학 속에서도 여전히 한 사람으로 있어라.', 'author': '데이비드 흄', 'source': '『An Enquiry Concerning Human Understanding』 §1', 'type': '철학', 'tags': ['자기신뢰', '자기이해']}, {'text': '자기 쪽 이야기만 아는 사람은 그것조차 충분히 알지 못한다.', 'author': '존 스튜어트 밀', 'source': '『On Liberty』 Ch.2', 'type': '철학', 'tags': ['관점 전환']}, {'text': '모든 것을 의심하는 것과 모든 것을 믿는 것은 똑같이 편한 방법이다. 둘 다 생각할 필요를 없애기 때문이다.', 'author': '앙리 푸앵카레', 'source': '『Science and Hypothesis』, Preface', 'type': '과학·철학', 'tags': ['관점 전환']}, {'text': '지혜의 기술은 무엇을 지나쳐도 되는지 아는 기술이다.', 'author': '윌리엄 제임스', 'source': '『The Principles of Psychology』 Vol. II, Ch.22', 'type': '심리학', 'tags': ['관점 전환', '위로']}, {'text': '마음에는 이성이 알지 못하는 나름의 이유가 있다.', 'author': '블레즈 파스칼', 'source': '『Pensées』', 'type': '철학', 'tags': ['자기이해', '위로']}, {'text': '우리는 남이 준 이유보다 스스로 발견한 이유에 더 잘 설득된다.', 'author': '블레즈 파스칼', 'source': '『Pensées』', 'type': '철학', 'tags': ['자기신뢰', '자기이해']}, {'text': '불확실함과 의문 속에 있으면서도 성급하게 답을 붙잡지 않을 수 있다.', 'author': '존 키츠', 'source': '조지·톰 키츠에게 보낸 편지, 1817.12.21, “Negative Capability”', 'type': '서간', 'tags': ['관점 전환', '위로']}, {'text': '의심은 편안한 상태가 아니지만, 확신만 하는 것은 어리석은 상태다.', 'author': '볼테르', 'source': '프리드리히 빌헬름에게 보낸 편지, 1770.11.28', 'type': '서간', 'tags': ['관점 전환']}, {'text': '가장 좋은 것을 고집하다 보면 좋은 것마저 놓칠 수 있다.', 'author': '볼테르', 'source': '「La Bégueule」, 1772', 'type': '시·경구', 'tags': ['관점 전환', '위로']}, {'text': '태양은 날마다 새롭다.', 'author': '헤라클레이토스', 'source': 'Fragment DK B6', 'type': '철학', 'tags': ['오늘', '다시 시작']}, {'text': '사람의 행동을 비웃거나 미워하기보다 이해하려고 했다.', 'author': '바뤼흐 스피노자', 'source': '『Tractatus Politicus』 I.4', 'type': '철학', 'tags': ['관점 전환', '관계']}, {'text': '마음은 채워야 할 그릇이라기보다 불붙여야 할 불과 같다.', 'author': '플루타르코스', 'source': '『On Listening』 48C', 'type': '철학', 'tags': ['가능성', '자기신뢰']}, {'text': '큰 사람은 어린아이의 마음을 잃지 않은 사람이다.', 'author': '맹자', 'source': '『맹자』 「이루 하」 12', 'type': '철학', 'tags': ['자기이해', '자기신뢰']}, {'text': '지금 증명된 것도 한때는 오직 상상 속에 있었다.', 'author': '윌리엄 블레이크', 'source': '『The Marriage of Heaven and Hell』', 'type': '시·산문', 'tags': ['가능성', '희망']}, {'text': '기쁨과 슬픔은 촘촘히 함께 짜여 있다.', 'author': '윌리엄 블레이크', 'source': '「Auguries of Innocence」', 'type': '시', 'tags': ['위로', '관점 전환']}, {'text': '겨울이 온다면, 봄이 어찌 멀리 있겠는가.', 'author': '퍼시 비시 셸리', 'source': '「Ode to the West Wind」', 'type': '시', 'tags': ['희망', '위로']}, {'text': '많은 것을 잃었어도, 아직 많은 것이 남아 있다.', 'author': '앨프리드 테니슨', 'source': '「Ulysses」', 'type': '시', 'tags': ['위로', '희망']}, {'text': '살아 있는 지금 속에서 행동하라.', 'author': '헨리 워즈워스 롱펠로', 'source': '「A Psalm of Life」', 'type': '시', 'tags': ['오늘', '용기']}, {'text': '용기는 두려움에 저항하고 그것을 다스리는 것이지, 두려움이 없는 것이 아니다.', 'author': '마크 트웨인', 'source': '『Pudd’nhead Wilson』 Ch.12', 'type': '소설', 'tags': ['용기', '자기신뢰']}, {'text': '가능한 모든 반론을 먼저 해결해야 한다면, 아무것도 시작되지 않을 것이다.', 'author': '새뮤얼 존슨', 'source': '『The History of Rasselas』', 'type': '소설·철학', 'tags': ['용기', '가능성']}, {'text': '일상의 작은 것들에 진짜 관심을 갖는 데에도 삶의 기쁨이 있다.', 'author': '윌리엄 모리스', 'source': '「The Aims of Art」 관련 산문', 'type': '산문', 'tags': ['오늘', '관점 전환']}, {'text': '아무것도 놓치지 않는 사람 가운데 한 사람이 되어 보라.', 'author': '헨리 제임스', 'source': '「The Art of Fiction」', 'type': '평론', 'tags': ['관점 전환', '오늘']}, {'text': '사실이 반대한다는 것이 드러나면, 아무리 아끼던 생각이라도 내려놓을 준비를 해 왔다.', 'author': '찰스 다윈', 'source': '『Autobiography』', 'type': '과학자 기록', 'tags': ['관점 전환', '용기']}, {'text': '자신이 모른다는 것을 분명히 아는 것이 모든 진정한 과학적 진보의 출발이다.', 'author': '제임스 클러크 맥스웰', 'source': 'R. B. 리치필드에게 보낸 편지, 1858.2.5', 'type': '과학자 서간', 'tags': ['자기신뢰', '관점 전환']}, {'text': '새로운 생각은 새롭다는 이유만으로 의심받고 반대받곤 한다.', 'author': '존 로크', 'source': '『An Essay Concerning Human Understanding』, “Epistle to the Reader”', 'type': '철학', 'tags': ['자기신뢰', '가능성']}, {'text': '사람은 자기 시야의 한계를 세상의 한계라고 생각하기 쉽다.', 'author': '아르투어 쇼펜하우어', 'source': '『Parerga and Paralipomena』', 'type': '철학', 'tags': ['관점 전환', '가능성']}, {'text': '행복은 찾아 나섰을 때보다 뜻밖에 찾아올 때가 있다.', 'author': '너새니얼 호손', 'source': '『American Note-Books』, 1851.11.3', 'type': '일기', 'tags': ['관점 전환', '희망']}, {'text': '경험의 결과만이 아니라 경험 그 자체에도 의미가 있다.', 'author': '월터 페이터', 'source': '『The Renaissance』, “Conclusion”', 'type': '평론', 'tags': ['관점 전환', '위로']}, {'text': '서로 다른 것들에서 가장 아름다운 조화가 생긴다.', 'author': '헤라클레이토스', 'source': 'Fragment DK B8', 'type': '철학', 'tags': ['위로', '관점 전환']}, {'text': '삶에는 우리에게 내어 줄 아름다움이 있다.', 'author': '세라 티즈데일', 'source': '「Barter」', 'type': '시', 'tags': ['오늘', '희망']}, {'text': '나의 길은 언제나 새로운 길.', 'author': '윤동주', 'source': '「새로운 길」, 1938.5.10', 'type': '시', 'tags': ['오늘', '다시 시작']}, {'text': '삶은 놀라움의 연속이다.', 'author': '랠프 월도 에머슨', 'source': '「Experience」', 'type': '산문', 'tags': ['가능성', '오늘']}]

# ------------------------------------------------------------
# 1. 명시적 감정어
# ------------------------------------------------------------
EMOTION_RULES = {
    "행복·즐거움": [
        "행복", "기쁜", "기뻐", "즐거", "유쾌", "신나", "쾌활", "살맛",
        "환상적", "기분 좋은", "경쾌", "활기찬", "상쾌", "산뜻",
        "좋아", "좋다", "해피", "happy", "joy", "glad", "기분 최고", "최고야"
    ],
    "평온·편안": [
        "편안", "평온", "차분", "안정", "잔잔", "고요", "포근", "홀가분", "괜찮아", "괜찮은 편", "calm", "peaceful", "relaxed"
    ],
    "감사·감동": [
        "감사", "고마", "감동", "감격", "뭉클", "따뜻", "다정", "애틋"
    ],
    "기대·설렘": [
        "기대", "설레", "두근", "간절", "열망", "호기심", "흥분", "짜릿"
    ],
    "만족·자신감": [
        "만족", "뿌듯", "흐뭇", "대견", "기특", "자신 있", "통쾌"
    ],
    "저조·허탈": [
        "별로", "그저 그래", "그냥 그래", "기분이 안 좋", "썩 좋지", "허탈",
        "허무", "헛헛", "찝찝", "마음이 무거", "의욕이 떨어", "맥 빠"
    ],
    "분노·짜증": [
        "분노", "짜증", "화나", "화가", "신경질", "약 오르", "괘씸", "불쾌",
        "얄미", "미운", "원망", "끓어오르", "기분이 상"
    ],
    "서운·배신": [
        "서운", "섭섭", "배신", "실망", "야속", "씁쓸", "언짢", "의리"
    ],
    "슬픔·상실": [
        "슬프", "슬퍼", "슬픔", "서글프", "서러", "가슴 아", "침통", "울적", "우울", "애처",
        "처량", "황량", "허전", "공허"
    ],
    "불안·걱정": [
        "불안", "걱정", "근심", "염려", "미심쩍", "조마조마", "초조", "절박"
    ],
    "두려움": [
        "무서", "두려", "섬뜩", "소름", "끔찍", "몸서리"
    ],
    "피로·버거움": [
        "피곤", "지쳐", "버거", "부담", "골치 아", "괴로", "고통", "숨 막", "갑갑"
    ],
    "무기력·권태": [
        "무기력", "권태", "지루", "귀찮", "싫증", "지겨", "의기소침", "낙담", "낙심"
    ],
    "답답·막막": [
        "답답", "암담", "절망", "좌절", "막막"
    ],
    "당황·혼란": [
        "당황", "착잡", "멍한", "어색", "복잡", "혼란", "민망"
    ],
    "부끄러움·죄책감": [
        "부끄", "창피", "죄스", "죄책감", "미안", "초라", "위축"
    ],
    "외로움·고독": [
        "외롭", "고독", "쓸쓸", "소외", "혼자인 것 같"
    ],
    "억울·모욕": [
        "억울", "모욕", "재수 없", "불공평"
    ],
    "후회·아쉬움": [
        "후회", "아쉬", "괜히", "그때 왜"
    ],
}

# ------------------------------------------------------------
# 2. 구어·비속어·은어 표현층
# 특정 감정으로 바로 단정하지 않고 강도/방향만 잡은 뒤
# 3번 이유의 상황을 함께 보고 감정을 좁힙니다.
# ------------------------------------------------------------
COLLOQUIAL_POSITIVE = [
    "해피", "happy", "좋아", "좋다",
    "미쳤다 너무 좋", "미치게 좋", "미치도록 좋", "개좋", "겁나 좋",
    "대박 좋", "미친 듯이 좋", "최고야", "짱이야"
]

COLLOQUIAL_NEGATIVE = [
    "지랄 같", "개같", "개판", "노답", "최악", "환장", "돌겠",
    "빡쳐", "빡친", "개빡", "미치겠", "미칠 것 같", "엉망", "망했다",
    "거지같", "답이 없", "끔찍하네", "진짜 싫"
]

# 문맥 없이도 비교적 분명한 표현
COLLOQUIAL_DIRECT = {
    "분노·짜증": ["빡쳐", "빡친", "개빡", "열받아", "개열받"],
    "저조·허탈": ["노답", "최악", "개판", "엉망", "망했다"],
}

# ------------------------------------------------------------
# 3. 이유/상황
# ------------------------------------------------------------
CONTEXT_RULES = {
    "관계갈등": [
        "다퉜", "싸웠", "서운", "배신", "의리", "신뢰", "동료", "친구와 어색",
        "친구랑 어색", "관계가 안 좋", "무시", "약속을 안 지", "말 때문에",
        "뒤에서 말", "험담", "거짓말"
    ],
    "관계긍정": [
        "함께 있어서", "같이 있어서", "친구를 만나", "가족과 함께", "대화가 잘",
        "좋은 사람과", "친구와 즐"
    ],
    "혼자휴식": [
        "혼자만의 시간", "혼자 있는 시간", "혼자 있어서 좋", "혼자라서 좋",
        "혼자 쉬", "내 시간을 즐", "혼자 보내는 시간이 좋"
    ],
    "외로움상황": [
        "혼자라서 외롭", "혼자여서 외롭", "아무도 없", "소외", "고립"
    ],
    "비교압박": [
        "사람들보다", "남들보다", "다른 사람보다", "친구보다", "뒤처", "뒤쳐",
        "못 따라", "속도가 느", "비교", "나만 못"
    ],
    "과제과다": [
        "할 일이 많", "해야 할 일이 많", "숙제", "과제가 많", "일이 쌓", "밀린 일",
        "바빠서", "할 게 많"
    ],
    "하루성과없음": [
        "하나도 못했", "아무것도 못했", "아무 일도 못했", "일을 못했",
        "계획을 못", "계획한 걸 못", "하루가 끝났", "시간이 다 갔", "시간만 갔",
        "한 게 없", "해놓은 게 없", "성과가 없"
    ],
    "학업압박": [
        "시험", "성적", "공부", "수능", "입시", "대학", "발표", "면접", "수업"
    ],
    "새로운도전": [
        "처음 해", "처음이라", "익숙하지", "새로운 걸", "처음 배우", "처음 해보"
    ],
    "실수실패": [
        "실수", "실패", "틀렸", "망했", "잘 안돼", "안 풀", "포기", "잘못했"
    ],
    "성취": [
        "잘했", "성공", "끝냈", "해냈", "칭찬", "성과", "완성", "좋은 결과"
    ],
    "수면부족": [
        "잠을 못", "잠 부족", "늦게 자", "밤샘", "잠이 부족"
    ],
    "신체불편": [
        "몸이 안 좋", "아파서", "감기", "두통", "몸살", "배가 아"
    ],
    "안도·무사함": [
        "무사히 지나", "무사히 끝", "잘 지나갔", "별일 없이", "아무 일 없이", "큰일 없이", "오늘도 지나갔"
    ],
    "기대상황": [
        "기대돼", "기다리던", "여행", "약속", "행사", "만나기로"
    ],
    "불확실": [
        "결과를 몰라", "어떻게 될지", "결정 못", "앞으로가", "모르겠", "막막"
    ],
}

WISH_RULES = {
    "위로": ["편해졌", "편안해", "마음이 가벼", "덜 힘들", "괜찮아지고"],
    "휴식": ["쉬고 싶", "푹 쉬", "잠을 자고", "휴식하고"],
    "자기신뢰": ["나를 믿", "자신감", "잘하고 싶", "내가 할 수", "스스로 믿"],
    "재도전": ["다시 해", "다시 시작", "포기하지", "재도전", "한번 더"],
    "관계회복": ["화해", "친해지고", "관계가 좋아", "잘 지내고", "오해가 풀"],
    "긍정유지": ["계속 행복", "좋은 기분", "이 기분 유지", "즐겁게", "행복했으면"],
    "집중": ["집중하고", "오늘 잘 보내", "차분히", "해야 할 일"],
    "가능성": ["가능성을", "희망", "잘됐으면", "좋은 결과", "앞으로 잘"],
    "이해": ["정리됐으면", "이해하고", "생각이 정리", "알고 싶"],
    "자기속도": ["내 속도", "천천히", "조급하지", "비교하지"],
}

EMOTION_TO_TAGS = {
    "행복·즐거움": ["오늘", "희망"],
    "평온·편안": ["오늘", "위로"],
    "감사·감동": ["관계", "오늘", "희망"],
    "기대·설렘": ["희망", "가능성", "오늘"],
    "만족·자신감": ["자기신뢰", "희망", "오늘"],
    "저조·허탈": ["위로", "다시 시작", "관점 전환"],
    "분노·짜증": ["관점 전환", "자기이해"],
    "서운·배신": ["관계", "위로", "관점 전환"],
    "슬픔·상실": ["위로", "희망"],
    "불안·걱정": ["위로", "관점 전환", "자기신뢰"],
    "두려움": ["위로", "용기", "자기신뢰"],
    "피로·버거움": ["위로", "오늘"],
    "무기력·권태": ["위로", "가능성", "오늘"],
    "답답·막막": ["관점 전환", "가능성"],
    "당황·혼란": ["관점 전환", "자기이해"],
    "부끄러움·죄책감": ["위로", "자기이해", "다시 시작"],
    "외로움·고독": ["관계", "위로", "자기존재"],
    "억울·모욕": ["관점 전환", "자기이해"],
    "후회·아쉬움": ["다시 시작", "위로", "관점 전환"],
}

CONTEXT_TO_TAGS = {
    "관계갈등": ["관계", "위로", "관점 전환"],
    "관계긍정": ["관계", "오늘", "희망"],
    "혼자휴식": ["자기이해", "자기신뢰", "오늘"],
    "외로움상황": ["관계", "위로", "자기존재"],
    "비교압박": ["자기신뢰", "위로", "관점 전환"],
    "과제과다": ["위로", "오늘", "자기신뢰"],
    "하루성과없음": ["다시 시작", "위로", "오늘", "관점 전환"],
    "학업압박": ["자기신뢰", "오늘", "관점 전환"],
    "새로운도전": ["용기", "가능성", "자기신뢰"],
    "실수실패": ["다시 시작", "자기신뢰", "위로"],
    "성취": ["자기신뢰", "희망", "오늘"],
    "수면부족": ["위로", "오늘"],
    "신체불편": ["위로"],
    "안도·무사함": ["오늘", "위로", "희망"],
    "기대상황": ["희망", "가능성", "오늘"],
    "불확실": ["관점 전환", "가능성", "위로"],
}

WISH_TO_TAGS = {
    "위로": ["위로"],
    "휴식": ["위로", "오늘"],
    "자기신뢰": ["자기신뢰"],
    "재도전": ["다시 시작", "용기"],
    "관계회복": ["관계", "위로"],
    "긍정유지": ["오늘", "희망"],
    "집중": ["오늘"],
    "가능성": ["가능성", "희망"],
    "이해": ["관점 전환", "자기이해"],
    "자기속도": ["자기신뢰", "위로"],
}

SPECIAL_QUOTE_RULES = [
    {
        "emotion": "행복·즐거움",
        "context": "성취",
        "preferred": [
            "우리는 해보면서 배운다.",
            "나는 지금의 나로 존재한다. 그것으로 충분하다.",
            "삶에는 우리에게 내어 줄 아름다움이 있다."
        ]
    },
    {
        "emotion": "평온·편안",
        "context": "안도·무사함",
        "preferred": [
            "삶에는 우리에게 내어 줄 아름다움이 있다.",
            "오늘 하루의 빛깔을 바꾸는 것, 그것이 가장 높은 예술이다.",
            "나는 지금의 나로 존재한다. 그것으로 충분하다."
        ]
    },
    {
        "emotion": "저조·허탈",
        "context": "하루성과없음",
        "preferred": [
            "태양은 날마다 새롭다.",
            "어제로 돌아가도 소용없어. 나는 이미 그때와 다른 사람이니까.",
            "절뚝이며 가더라도 뒤로 가는 것은 아니다.",
            "우리는 해보면서 배운다.",
            "시간의 좋은 점은 미리 낭비해 버릴 수 없다는 것이다."
        ]
    },
    {
        "emotion": "피로·버거움",
        "context": "과제과다",
        "preferred": [
            "서두를 필요도, 빛나 보일 필요도, 자기 아닌 다른 사람이 될 필요도 없다.",
            "지혜의 기술은 무엇을 지나쳐도 되는지 아는 기술이다.",
            "시간의 좋은 점은 미리 낭비해 버릴 수 없다는 것이다."
        ]
    },
    {
        "emotion": None,
        "context": "비교압박",
        "preferred": [
            "서두를 필요도, 빛나 보일 필요도, 자기 아닌 다른 사람이 될 필요도 없다.",
            "절뚝이며 가더라도 뒤로 가는 것은 아니다.",
            "나는 지금의 나로 존재한다. 그것으로 충분하다.",
            "남을 흉내 내 성공하는 것보다 자기 방식으로 실패하는 편이 낫다."
        ]
    },
    {
        "emotion": "행복·즐거움",
        "context": "혼자휴식",
        "preferred": [
            "세상에서 가장 큰 일은 자기 자신에게 속할 줄 아는 것이다.",
            "삶에는 우리에게 내어 줄 아름다움이 있다.",
            "나는 지금의 나로 존재한다. 그것으로 충분하다."
        ]
    },
    {
        "emotion": "분노·짜증",
        "context": "관계갈등",
        "preferred": [
            "사람의 행동을 비웃거나 미워하기보다 이해하려고 했다.",
            "사람의 말 속에 완전한 진실이 그대로 담기는 경우는 아주 드물다.",
            "한 가지 일을 여러 관점에서 바라보지 못하는 것은 좁은 생각이다."
        ]
    },
    {
        "emotion": "서운·배신",
        "context": "관계갈등",
        "preferred": [
            "사람의 말 속에 완전한 진실이 그대로 담기는 경우는 아주 드물다.",
            "네가 강과 하늘을 보며 느끼는 것처럼, 나도 그렇게 느꼈다.",
            "사람의 행동을 비웃거나 미워하기보다 이해하려고 했다."
        ]
    },
    {
        "emotion": "불안·걱정",
        "context": None,
        "preferred": [
            "우리는 현실보다 상상 속에서 더 자주 괴로워한다.",
            "어떤 것은 우리에게 달려 있고, 어떤 것은 그렇지 않다.",
            "가장 용감한 사람도 잠시 더듬으며 걷는다."
        ]
    },
    {
        "emotion": None,
        "context": "신체불편",
        "preferred": [
            "서두를 필요도, 빛나 보일 필요도, 자기 아닌 다른 사람이 될 필요도 없다.",
            "회오리바람도 아침 내내 불지는 않고, 소나기도 하루 종일 내리지는 않는다.",
            "제비 한 마리가 여름을 만들지 않듯, 하루가 한 사람의 삶 전체를 결정하지 않는다.",
            "절뚝이며 가더라도 뒤로 가는 것은 아니다."
        ]
    },
]

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())

def detect_label(text: str, rules: dict, default=None):
    t = normalize(text)
    best_label = default
    best_hits = 0
    for label, keywords in rules.items():
        hits = sum(1 for keyword in keywords if keyword in t)
        if hits > best_hits:
            best_hits = hits
            best_label = label
    return best_label

def detect_context(text: str):
    t = normalize(text)
    if any(k in t for k in ["혼자만의 시간", "혼자 있는 시간", "혼자 있어서 좋", "혼자라서 좋", "내 시간을 즐"]):
        return "혼자휴식"
    if any(k in t for k in ["혼자라서 외롭", "혼자여서 외롭", "아무도 없", "소외", "고립"]):
        return "외로움상황"
    return detect_label(text, CONTEXT_RULES, None)

def infer_from_colloquial(mood_text: str, reason_text: str):
    mood = normalize(mood_text)
    reason = normalize(reason_text)
    context = detect_context(reason)

    # 긍정 강도 표현
    if any(p in mood for p in COLLOQUIAL_POSITIVE):
        if any(k in mood for k in ["설레", "기대", "두근"]):
            return "기대·설렘"
        return "행복·즐거움"

    # 비교적 직접적인 구어 표현
    direct = detect_label(mood, COLLOQUIAL_DIRECT, None)
    if direct:
        return direct

    # 부정 강도 표현: 이유를 함께 해석
    if any(p in mood for p in COLLOQUIAL_NEGATIVE):
        if context == "관계갈등":
            if any(k in reason for k in ["배신", "의리", "신뢰", "서운", "섭섭"]):
                return "서운·배신"
            return "분노·짜증"
        if context == "비교압박":
            return "저조·허탈"
        if context == "과제과다":
            return "피로·버거움"
        if context == "하루성과없음":
            return "후회·아쉬움"
        if context == "실수실패":
            return "후회·아쉬움"
        if context == "학업압박":
            if any(k in reason for k in ["걱정", "결과", "어떻게 될", "불안"]):
                return "불안·걱정"
            return "피로·버거움"
        if context == "불확실":
            return "불안·걱정"
        if context == "수면부족":
            return "피로·버거움"
        if context == "신체불편":
            return "피로·버거움"
        if context == "외로움상황":
            return "외로움·고독"
        return "저조·허탈"

    return None


AMBIGUOUS_MOOD_PATTERNS = [
    "그냥 그래",
    "그저 그래",
    "평범해",
    "평범",
    "보통이야",
    "보통",
    "모르겠어",
    "잘 모르겠어",
    "애매해",
    "애매",
    "별 생각 없어",
    "별생각 없어",
    "딱히 없어",
    "딱히",
    "그럭저럭",
    "똑같아",
]

def has_explicit_emotion(text: str) -> bool:
    t = normalize(text)

    # 명시적 감정어
    for keywords in EMOTION_RULES.values():
        if any(keyword in t for keyword in keywords):
            return True

    # 강한 구어/비속어/은어 표현
    if any(p in t for p in COLLOQUIAL_POSITIVE):
        return True
    if any(p in t for p in COLLOQUIAL_NEGATIVE):
        return True
    for keywords in COLLOQUIAL_DIRECT.values():
        if any(keyword in t for keyword in keywords):
            return True

    return False

NON_EMOTION_STATE_PATTERNS = [
    "피곤", "졸려", "졸림", "배고파", "배불러", "아파", "아픔",
    "체했", "체해서", "속이 안 좋", "소화가 안", "머리 아파", "두통",
    "춥", "덥", "목말라", "어지러", "몸이 무거", "컨디션",
]

AMBIGUOUS_BODY_MOOD_PATTERNS = [
    "답답", "무거워", "무겁다",
]

def needs_emotion_clarification(text: str, reason_text: str = "") -> bool:
    """
    감정이 아닌 상태·사건이면 감정어를 한 번 더 묻습니다.
    신체/감정 양쪽으로 쓰이는 말은 이유가 신체불편일 때 재확인합니다.
    """
    t = normalize(text)
    context = detect_context(reason_text) if reason_text else None

    if any(p in t for p in NON_EMOTION_STATE_PATTERNS):
        return True

    if context == "신체불편" and any(p in t for p in AMBIGUOUS_BODY_MOOD_PATTERNS):
        return True

    if has_explicit_emotion(t):
        return False

    if any(pattern in t for pattern in AMBIGUOUS_MOOD_PATTERNS):
        return True

    # 감정어가 없으면 길이에 상관없이 다시 확인
    return True

def detect_emotion(mood_text: str, reason_text: str):
    mood = normalize(mood_text)

    # 부정형 먼저 처리: "안 좋아", "좋진 않아" 등을 긍정으로 오인하지 않게 함
    if any(p in mood for p in ["안 좋아", "좋지 않아", "좋진 않아", "별로", "썩 좋지", "안 괜찮아", "괜찮지 않아"]):
        return "저조·허탈"

    # 구어/비속어 층을 먼저 살펴봄
    colloquial = infer_from_colloquial(mood_text, reason_text)
    if colloquial:
        return colloquial

    # 그 다음 명시적 감정어
    explicit = detect_label(mood_text, EMOTION_RULES, None)
    if explicit:
        return explicit

    # 감정어가 없으면 이유를 보조 근거로 사용
    context = detect_context(reason_text)
    context_fallback = {
        "관계갈등": "서운·배신",
        "외로움상황": "외로움·고독",
        "비교압박": "저조·허탈",
        "과제과다": "피로·버거움",
        "하루성과없음": "후회·아쉬움",
        "학업압박": "불안·걱정",
        "실수실패": "후회·아쉬움",
        "수면부족": "피로·버거움",
        "신체불편": "피로·버거움",
        "불확실": "불안·걱정",
        "성취": "만족·자신감",
        "기대상황": "기대·설렘",
        "혼자휴식": "평온·편안",
        "관계긍정": "행복·즐거움",
        "안도·무사함": "평온·편안",
    }
    return context_fallback.get(context, "저조·허탈")

def detect_wish(text: str):
    return detect_label(text, WISH_RULES, None)

def special_bonus(quote, emotion, context):
    bonus = 0
    for rule in SPECIAL_QUOTE_RULES:
        if rule["emotion"] is not None and rule["emotion"] != emotion:
            continue
        if rule["context"] is not None and rule["context"] != context:
            continue
        if quote["text"] in rule["preferred"]:
            rank = rule["preferred"].index(quote["text"])
            bonus += 42 - rank * 4
    return bonus

def quote_score(quote, emotion, context, wish):
    tags = quote["tags"]
    score = 0

    if wish:
        for tag in WISH_TO_TAGS[wish]:
            if tag in tags:
                score += 17

    if context:
        for tag in CONTEXT_TO_TAGS[context]:
            if tag in tags:
                score += 11

    for tag in EMOTION_TO_TAGS.get(emotion, []):
        if tag in tags:
            score += 7

    score += special_bonus(quote, emotion, context)
    return score

def choose_quote(mood_text: str, reason_text: str, wish_text: str):
    context = detect_context(reason_text)
    emotion = detect_emotion(mood_text, reason_text)
    wish = detect_wish(wish_text)

    scored = [
        (quote_score(q, emotion, context, wish), idx)
        for idx, q in enumerate(QUOTES)
    ]
    scored.sort(key=lambda item: (-item[0], item[1]))

    # 적합성은 유지하되 후보 폭은 이전보다 넓힘.
    # 최고점에서 12점 이내, 최대 12개를 후보로 둠.
    best_score = scored[0][0]
    candidate_pool = [
        (score, idx)
        for score, idx in scored
        if score >= best_score - 12
    ][:12]

    # 같은 세션에서 이미 나온 문장에는 감점을 주어
    # 100개 문장 중 더 다양한 문장이 순환하도록 함.
    usage = st.session_state.get("quote_usage", {})
    recent = st.session_state.get("recent_quotes", [])

    adjusted = []
    for base_score, idx in candidate_pool:
        used_count = usage.get(idx, 0)
        recent_penalty = 10 if idx in recent[-5:] else 0
        usage_penalty = used_count * 5
        adjusted_score = base_score - recent_penalty - usage_penalty
        adjusted.append((adjusted_score, base_score, idx))

    adjusted.sort(key=lambda item: (-item[0], -item[1], item[2]))

    # 조정 점수가 높은 상위 4개 중 하나를 선택해
    # 맥락 적합성과 다양성을 함께 확보.
    top_adjusted = adjusted[:4]
    chosen_idx = random.choice([idx for _, _, idx in top_adjusted])

    usage[chosen_idx] = usage.get(chosen_idx, 0) + 1
    st.session_state["quote_usage"] = usage
    st.session_state["recent_quotes"] = (recent + [chosen_idx])[-5:]

    return chosen_idx, emotion, context, wish

def normalize_name_input(name: str) -> str:
    """
    '선영이야', '써니야', '선영이에요'처럼 자연스럽게 답해도
    이름 부분만 남기도록 최소한으로 정리합니다.
    """
    n = name.strip().rstrip(".!? ")
    endings = [
        "이라고 합니다", "라고 합니다",
        "이라고 해", "라고 해",
        "이에요", "예요", "입니다",
        "이야", "야",
    ]
    for ending in endings:
        if n.endswith(ending) and len(n) > len(ending):
            candidate = n[:-len(ending)].strip()
            if candidate:
                return candidate
    return n


def vocative_name(name: str) -> str:
    clean = name.strip()
    if not clean:
        return ""
    last = clean[-1]
    if "가" <= last <= "힣":
        jong = (ord(last) - ord("가")) % 28
        return clean + ("아" if jong else "야")
    return clean + "아"



def natural_reason_clause(reason: str) -> str:
    """
    학생이 적은 이유를 결과 문장에서 자연스러운 원인절로 바꿉니다.
    여러 문장으로 적은 경우에는 앞 문장은 연결하고, 마지막 문장은 원인절로 정리합니다.
    """
    raw = reason.strip().replace("\n", " ").strip()
    if not raw:
        return "특별한 이유를 딱 짚기는 어렵지만"

    parts = [p.strip() for p in re.split(r"[.!?]+\s*", raw) if p.strip()]
    if not parts:
        parts = [raw]

    vague_map = {
        "그냥": "특별한 이유를 딱 짚기는 어렵지만",
        "잘 모르겠어": "이유를 딱 짚기 어렵지만",
        "모르겠어": "이유를 딱 짚기 어렵지만",
        "모르겠음": "이유를 딱 짚기 어렵지만",
        "별일 없어": "특별한 일은 없지만",
        "없어": "특별한 이유는 없지만",
    }
    if len(parts) == 1 and parts[0] in vague_map:
        return vague_map[parts[0]]

    def normalize_polite(s: str) -> str:
        polite_map = [
            ("배웠어요", "배웠어"), ("끝냈어요", "끝냈어"), ("마쳤어요", "마쳤어"),
            ("완성했어요", "완성했어"), ("성공했어요", "성공했어"), ("해냈어요", "해냈어"),
            ("거쳤어요", "거쳤어"), ("되었어요", "되었어"), ("됐어요", "됐어"),
            ("했어요", "했어"), ("있어요", "있어"), ("없어요", "없어"),
            ("좋아요", "좋아"), ("싫어요", "싫어"), ("힘들어요", "힘들어"),
            ("피곤해요", "피곤해"), ("졸려요", "졸려"), ("불안해요", "불안해"),
            ("서운해요", "서운해"), ("아파요", "아파"),
        ]
        for ending, converted in polite_map:
            if s.endswith(ending):
                return s[:-len(ending)] + converted
        return s

    def to_connective(s: str) -> str:
        s = normalize_polite(s).strip().rstrip(".!? ")
        if s.endswith(("해서", "어서", "아서", "고", "니까", "면서", "는데")):
            return s
        connective_map = [
            ("완성했어", "완성했고"), ("완성했다", "완성했고"),
            ("성공했어", "성공했고"), ("성공했다", "성공했고"),
            ("해냈어", "해냈고"), ("해냈다", "해냈고"),
            ("끝냈어", "끝냈고"), ("끝냈다", "끝냈고"),
            ("마쳤어", "마쳤고"), ("마쳤다", "마쳤고"),
            ("거쳤어", "거쳤고"), ("거쳤다", "거쳤고"),
            ("배웠어", "배웠고"), ("배웠다", "배웠고"),
            ("했어", "했고"), ("했다", "했고"),
            ("있어", "있고"), ("없어", "없고"),
            ("좋아", "좋고"), ("싫어", "싫고"),
            ("피곤해", "피곤하고"), ("불안해", "불안하고"),
            ("서운해", "서운하고"), ("아파", "아프고"),
        ]
        for old, new in connective_map:
            if s.endswith(old):
                return s[:-len(old)] + new
        return s + " 그리고"

    def to_causal(s: str) -> str:
        s = normalize_polite(s).strip().rstrip(".!? ")
        if s.endswith(("해서", "어서", "아서", "니까", "때문에", "라서", "이라서", "여서", "는데")):
            return s

        if s.endswith("이야"):
            return s[:-2] + "이기 때문에"
        if s.endswith("야") and not s.endswith("이야"):
            return s[:-1] + "이기 때문에"
        if s.endswith("이었어"):
            return s[:-3] + "이어서"
        if s.endswith("였어"):
            return s[:-2] + "여서"

        direct_map = [
            ("완성했어", "완성했기 때문에"), ("완성했다", "완성했기 때문에"),
            ("성공했어", "성공했기 때문에"), ("성공했다", "성공했기 때문에"),
            ("해냈어", "해냈기 때문에"), ("해냈다", "해냈기 때문에"),
            ("끝냈어", "끝냈기 때문에"), ("끝냈다", "끝냈기 때문에"),
            ("마쳤어", "마쳤기 때문에"), ("마쳤다", "마쳤기 때문에"),
            ("거쳤어", "거쳤기 때문에"), ("거쳤다", "거쳤기 때문에"),
            ("배웠어", "배워서"), ("배웠다", "배워서"), ("나왔어", "나와서"), ("왔다", "와서"), ("왔어", "와서"), ("갔어", "가서"), ("갔다", "가서"), ("먹었어", "먹어서"), ("봤어", "봐서"), ("들었어", "들어서"), ("읽었어", "읽어서"),
            ("되었어", "되어서"), ("됐어", "돼서"),
            ("했어", "해서"), ("했다", "해서"),
            ("있어", "있어서"), ("없어", "없어서"),
            ("좋아", "좋아서"), ("싫어", "싫어서"),
            ("힘들어", "힘들어서"), ("피곤해", "피곤해서"), ("졸려", "졸려서"),
            ("늦었어", "늦어서"), ("끝났어", "끝나서"), ("못했어", "못해서"),
            ("안 됐어", "안 돼서"), ("안돼", "안 돼서"),
            ("바빠", "바빠서"), ("아파", "아파서"),
            ("서운해", "서운해서"), ("불안해", "불안해서"),
            ("걱정돼", "걱정돼서"), ("망쳤어", "망쳐서"), ("틀렸어", "틀려서"),
        ]
        for old, new in direct_map:
            if s.endswith(old):
                return s[:-len(old)] + new

        return s + " 때문에"

    if len(parts) == 1:
        return to_causal(parts[0])

    front = [to_connective(p) for p in parts[:-1]]
    last = to_causal(parts[-1])
    return " ".join(front + [last])


ENGLISH_EMOTION_ALIASES = {
    "happy": "행복",
    "joy": "기쁨",
    "joyful": "기쁨",
    "sad": "슬픔",
    "depressed": "우울",
    "anxious": "불안",
    "anxiety": "불안",
    "nervous": "초조",
    "tired": "피곤",
    "sleepy": "졸림",
    "calm": "평온",
    "peaceful": "평온",
    "comfortable": "편안",
    "proud": "뿌듯",
    "confident": "자신감",
    "angry": "화남",
    "annoyed": "짜증",
    "lonely": "외로움",
    "grateful": "고마움",
    "excited": "설렘",
    "okay": "괜찮음",
    "fine": "괜찮음",
    "so so": "그냥 그래",
}

def normalize_raw_emotion_word(word: str) -> str:
    w = word.strip().lower()
    phrase_aliases = {
        "답답해": "답답", "답답하다": "답답", "답답함": "답답",
        "피곤해": "피곤", "피곤하다": "피곤", "피곤함": "피곤",
        "졸려": "졸림", "졸리다": "졸림", "졸림": "졸림",
        "불안해": "불안", "불안하다": "불안", "불안함": "불안",
        "초조해": "초조", "초조하다": "초조", "초조함": "초조",
        "우울해": "우울", "우울하다": "우울", "우울함": "우울",
        "행복해": "행복", "행복하다": "행복", "행복함": "행복",
        "기뻐": "기쁨", "기쁘다": "기쁨", "기쁨": "기쁨",
        "뿌듯해": "뿌듯", "뿌듯하다": "뿌듯", "뿌듯함": "뿌듯",
        "편안해": "편안", "편안하다": "편안", "편안함": "편안",
        "평온해": "평온", "평온하다": "평온", "평온함": "평온",
        "서운해": "서운", "서운하다": "서운", "서운함": "서운",
        "슬퍼": "슬픔", "슬프다": "슬픔", "슬픔": "슬픔",
        "짜증나": "짜증", "짜증남": "짜증",
        "화나": "화남", "화가 나": "화남", "화남": "화남",
        "설레": "설렘", "설렌다": "설렘", "설렘": "설렘",
        "자신감": "자신감", "자신감이 생김": "자신감",
    }
    if w in phrase_aliases:
        return phrase_aliases[w]
    return ENGLISH_EMOTION_ALIASES.get(w, word.strip())


def emotion_phrase_for_result(emotion_label: str, raw_emotion: str = "") -> str:
    label_map = {
        "행복·즐거움": "행복하고 즐겁구나",
        "평온·편안": "평온하고 편안하구나",
        "감사·감동": "고맙고 마음이 따뜻하구나",
        "기대·설렘": "기대되고 설레는구나",
        "만족·자신감": "뿌듯하고 자신감이 생기는구나",
        "저조·허탈": "마음이 가라앉고 허탈하구나",
        "분노·짜증": "화가 나고 짜증이 나는구나",
        "서운·배신": "서운하고 실망스럽구나",
        "슬픔·상실": "슬프고 마음이 무겁구나",
        "불안·걱정": "불안하고 걱정되는구나",
        "두려움": "두렵고 무섭구나",
        "피로·버거움": "피곤하고 버겁구나",
        "무기력·권태": "의욕이 없고 무기력하구나",
        "답답·막막": "답답하고 막막하구나",
        "당황·혼란": "당황스럽고 마음이 복잡하구나",
        "부끄러움·죄책감": "부끄럽고 마음이 무겁구나",
        "외로움·고독": "외롭고 쓸쓸하구나",
        "억울·모욕": "억울하고 마음이 상했구나",
        "후회·아쉬움": "아쉽고 후회되는구나",
    }

    raw = raw_emotion.strip()
    if not raw:
        return label_map.get(emotion_label, "그런 마음이 드는구나")

    whole = normalize_raw_emotion_word(raw)
    raw = whole

    parts = [normalize_raw_emotion_word(p) for p in re.split(r"[,\s/]+", raw) if p]
    if len(parts) >= 2:
        first, second = parts[0], parts[1]
        first_map = {
            "불안": "불안하고", "초조": "초조하고", "행복": "행복하고",
            "기쁨": "기쁘고", "뿌듯": "뿌듯하고", "자신감": "자신감이 생기고",
            "즐거움": "즐겁고", "슬픔": "슬프고", "서운": "서운하고",
            "짜증": "짜증이 나고", "화남": "화가 나고", "우울": "우울하고",
            "피곤": "피곤하고", "졸림": "졸리고", "답답": "답답하고",
            "허무": "허무하고", "허탈": "허탈하고", "평온": "평온하고",
            "편안": "편안하고", "설렘": "설레고", "기대": "기대되고",
            "감사": "고맙고",
        }
        last_map = {
            "불안": "불안하구나", "초조": "초조하구나", "행복": "행복하구나",
            "기쁨": "기쁘구나", "뿌듯": "뿌듯하구나", "자신감": "자신감이 생기는구나",
            "즐거움": "즐겁구나", "슬픔": "슬프구나", "서운": "서운하구나",
            "짜증": "짜증이 나는구나", "화남": "화가 나는구나", "우울": "우울하구나",
            "피곤": "피곤하구나", "졸림": "졸리구나", "답답": "답답하구나",
            "허무": "허무하구나", "허탈": "허탈하구나", "평온": "평온하구나",
            "편안": "편안하구나", "설렘": "설레는구나", "기대": "기대되는구나",
            "감사": "고맙구나",
        }
        return f"{first_map.get(first, first + '하고')} {last_map.get(second, second + '하구나')}"

    single = parts[0]
    single_map = {
        "행복": "행복하구나", "기쁨": "기쁘구나", "뿌듯": "뿌듯하구나",
        "자신감": "자신감이 생기는구나", "즐거움": "즐겁구나",
        "불안": "불안하구나", "초조": "초조하구나", "우울": "우울하구나",
        "슬픔": "슬프구나", "서운": "서운하구나", "짜증": "짜증이 나는구나",
        "화남": "화가 나는구나", "피곤": "피곤하구나", "졸림": "졸리구나",
        "답답": "답답하구나", "허무": "허무하구나", "허탈": "허탈하구나",
        "평온": "평온하구나", "편안": "편안하구나", "설렘": "설레는구나",
        "기대": "기대되는구나", "감사": "고맙구나",
    }
    return single_map.get(single, label_map.get(emotion_label, "그런 마음이 드는구나"))

def split_sentences_for_letter(text: str):
    """마침표/물음표/느낌표 단위로 편지 문장을 줄바꿈하기 위한 보조 함수."""
    chunks = re.findall(r"[^.!?]+[.!?]?", text.strip())
    return [c.strip() for c in chunks if c.strip()]


def pastel_class(emotion: str):
    if emotion in ["행복·즐거움", "감사·감동", "기대·설렘", "만족·자신감"]:
        return "pastel-warm"
    if emotion in ["불안·걱정", "두려움", "피로·버거움", "답답·막막", "저조·허탈"]:
        return "pastel-calm"
    if emotion in ["슬픔·상실", "서운·배신", "외로움·고독", "후회·아쉬움"]:
        return "pastel-soft"
    return "pastel-fresh"


def choose_second_quote(mood: str, reason: str, wish: str, first_idx: int) -> int:
    """
    첫 번째 문장과 겹치지 않는 두 번째 문장을 고릅니다.
    같은 감정·상황·바람 입력을 기준으로 추천하되, 최대한 기존 추천 로직을 그대로 활용합니다.
    """
    tried = set()
    for _ in range(20):
        idx, _, _, _ = choose_quote(mood, reason, wish)
        if idx != first_idx:
            return idx
        tried.add(idx)

    # 드물게 같은 문장만 반복되면, 태그가 겹치는 다른 문장을 우선 탐색
    first_tags = set(QUOTES[first_idx].get("tags", []))
    candidates = []
    for i, q in enumerate(QUOTES):
        if i == first_idx:
            continue
        overlap = len(first_tags & set(q.get("tags", [])))
        candidates.append((overlap, i))

    candidates.sort(reverse=True)
    if candidates:
        top_overlap = candidates[0][0]
        pool = [i for overlap, i in candidates if overlap == top_overlap]
        return random.choice(pool)

    return first_idx

def build_support_message(emotion, context, wish):
    if context == "신체불편":
        return (
            "몸이 불편하면 기분까지 가라앉거나 답답해질 수 있어. 지금은 무리해서 평소처럼 하려고 하기보다 몸이 보내는 신호를 먼저 살펴도 괜찮아.",
            "몸이 편하지 않은 날에는 스스로를 몰아붙이기보다 잠시 쉬어 가도 괜찮다는 뜻이 담겨 있어서",
        )

    if emotion == "저조·허탈":
        if context == "하루성과없음":
            return (
                "하루가 기대한 만큼 흘러가지 않으면 허탈하고 아쉬울 수 있어. 오늘 해낸 일이 적다고 해서 오늘 하루 전체가 의미 없어진 것은 아니야. 지금부터 할 수 있는 작은 한 가지나 내일의 첫걸음을 정해도 충분해.",
                "오늘을 실패로 단정하기보다 다시 시작할 수 있다는 뜻이 담겨 있어서",
            )
        return (
            "마음이 썩 좋지 않은 날에는 그 이유가 또렷하지 않을 때도 있어. 억지로 기분을 바꾸려 하기보다 지금의 상태를 잠깐 인정해도 괜찮아.",
            "오늘의 마음을 끝으로 단정하지 않고 조금 다르게 바라볼 수 있게 해 주는 뜻이 담겨 있어서",
        )

    if emotion == "후회·아쉬움":
        if context == "하루성과없음":
            return (
                "하루가 끝나고 나서 한 일이 없다고 느끼면 아쉬움이 크게 남을 수 있어. 하지만 오늘의 아쉬움은 내일 무엇부터 시작할지 알려 주는 신호가 될 수도 있어.",
                "지나간 하루를 자책으로 끝내기보다 다음 시작으로 이어 갈 수 있다는 뜻이 담겨 있어서",
            )
        return (
            "이미 지나간 일을 다시 바꿀 수는 없지만, 그때의 선택을 돌아본 마음은 다음 선택을 다르게 만드는 데 쓰일 수 있어.",
            "지나간 일을 끝으로 두기보다 다시 시작할 수 있다는 뜻이 담겨 있어서",
        )

    if emotion == "행복·즐거움":
        if context == "성취":
            return (
                "해내고 싶었던 일을 실제로 끝냈을 때의 기쁨은 충분히 누려도 좋아. 결과뿐 아니라 그 과정에서 네가 시도하고 해결해 온 시간도 함께 기억해 두면 좋겠다.",
                "무언가를 해낸 지금의 기쁨과 성취를 오래 기억하게 해 주는 뜻이 담겨 있어서",
            )
        if context == "혼자휴식":
            return (
                "혼자 있는 시간이 꼭 외로운 시간인 것은 아니지. 누구의 속도에도 맞출 필요 없이 네가 좋아하는 방식으로 시간을 보내고 있다는 게 지금의 좋은 마음과 잘 이어지는 것 같아.",
                "자기 자신에게 온전히 머무는 시간의 의미를 담고 있어서",
            )
        return (
            "좋은 마음이 드는 순간은 이유를 분석하기보다 충분히 누려도 좋아. 오늘의 기분이 하루를 조금 더 가볍게 만들어 주면 좋겠다.",
            "지금의 좋은 마음을 오래 간직하는 데 어울리는 뜻이 담겨 있어서",
        )

    if emotion == "평온·편안":
        if context == "안도·무사함":
            return (
                "특별한 일이 없었다는 사실이 오히려 마음을 놓이게 하는 날도 있어. 오늘 하루를 무사히 지나왔다는 것만으로도 충분히 괜찮은 하루일 수 있어.",
                "무사히 지나온 오늘을 가볍게 인정하고 편안하게 바라보게 해 주는 뜻이 담겨 있어서",
            )
        return (
            "마음이 잔잔한 순간은 생각보다 귀해. 무엇을 더 채우기보다 지금의 편안함을 그대로 느껴도 좋아.",
            "지금의 고요한 마음을 소중히 바라보게 해 주는 뜻이 담겨 있어서",
        )

    if emotion == "분노·짜증":
        if context == "관계갈등":
            return (
                "믿었던 사람이나 가까운 사람 때문에 화가 나면 감정이 더 크게 흔들릴 수 있어. 지금 당장 이해하거나 용서하려고 서두르지 않아도 괜찮아.",
                "상대와 상황을 조금 떨어져 바라보는 데 도움이 될 수 있어서",
            )
        return (
            "화가 난 마음에는 그만한 이유가 있을 수 있어. 감정을 억지로 없애기보다 왜 그런 마음이 들었는지 천천히 살펴봐도 괜찮아.",
            "지금의 감정을 한 번 다른 각도에서 바라보게 해 줄 수 있어서",
        )

    if emotion == "서운·배신":
        return (
            "기대했던 사람이 다르게 행동하면 서운함이 오래 남을 수 있어. 네가 느낀 실망을 너무 빨리 작게 만들 필요는 없어.",
            "사람의 마음과 관계를 한쪽 모습만으로 단정하지 않게 해 주는 뜻이 담겨 있어서",
        )

    if emotion == "슬픔·상실":
        return (
            "슬프거나 마음이 무거운 날에는 빨리 괜찮아지려고 애쓰지 않아도 돼. 오늘은 그런 마음이 있다는 사실만 인정해도 충분해.",
            "지금의 마음이 오래 그대로일 필요는 없다는 뜻을 전해 주고 싶어서",
        )

    if emotion == "불안·걱정":
        return (
            "아직 정해지지 않은 일은 마음을 쉽게 지치게 해. 지금 당장 모든 답을 정하지 않아도 괜찮아.",
            "불안한 순간에도 마음을 조금 넓게 바라볼 수 있게 해 주는 뜻이 담겨 있어서",
        )

    if emotion == "두려움":
        return (
            "무서운 마음이 든다고 해서 네가 약한 것은 아니야. 두려움을 안고도 한 걸음씩 움직일 수 있어.",
            "용기는 두려움이 없는 상태가 아니라 그 마음을 안고도 움직이는 것이라는 뜻이 담겨 있어서",
        )

    if emotion == "피로·버거움":
        if context == "과제과다":
            return (
                "해야 할 일이 한꺼번에 겹치면 몸보다 마음이 먼저 지칠 때도 있어. 오늘 모든 일을 완벽하게 끝내기보다 하나씩 해도 괜찮아.",
                "해야 할 일에 떠밀리기보다 자기 속도로 가도 괜찮다는 뜻이 담겨 있어서",
            )
        return (
            "피곤한 날에는 평소처럼 해내는 것만으로도 충분히 애쓰고 있는 거야. 잠시 속도를 늦춰도 괜찮아.",
            "오늘 하루를 너무 몰아붙이지 않아도 된다는 뜻이 담겨 있어서",
        )

    if emotion == "무기력·권태":
        return (
            "아무것도 하고 싶지 않은 날도 있어. 의욕이 바로 생기지 않더라도 작은 움직임 하나부터 시작해도 괜찮아.",
            "멈춘 것처럼 느껴져도 다시 움직일 가능성은 남아 있다는 뜻이 담겨 있어서",
        )

    if emotion == "답답·막막":
        return (
            "지금 답이 바로 보이지 않는다고 해서 길이 없는 것은 아니야. 생각이 정리되는 데는 시간이 필요할 때도 있어.",
            "지금 보이는 것만으로 가능성을 다 정하지 않아도 된다는 뜻이 담겨 있어서",
        )

    if emotion == "외로움·고독":
        return (
            "외로운 마음은 주변에 사람이 있는지와 꼭 같은 문제는 아니야. 네 마음이 누군가에게 닿고 싶다는 신호일 수도 있어.",
            "혼자라고 느끼는 순간에도 사람과 삶의 연결을 떠올리게 해 주는 뜻이 담겨 있어서",
        )

    return (
        "지금 느끼는 마음을 이렇게 적어 본 것만으로도 네 상태를 한 번 돌아본 셈이야.",
        "오늘의 마음을 조금 다른 시선으로 바라보는 데 도움이 될 것 같아서",
    )

if "page" not in st.session_state:
    st.session_state.page = "input"

def today_korean_date() -> str:
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    today = date.today()
    return f"{today.year}. {today.month}. {today.day}. ({weekdays[today.weekday()]})"


def format_quote_card_text(text: str) -> str:
    """
    긴 문장을 카드 안에서 읽기 좋게 정리합니다.
    문장 자체는 바꾸지 않고, 필요한 경우 의미 단위에서만 줄을 바꿉니다.
    """
    formatted = text

    replacements = [
        (", 너도", ",<br>너도"),
        (" 삶이 계속되고, 너도", " 삶이 계속되고,<br>너도"),
        (" 것을 보는 데 있다.", " 것을<br>보는 데 있다."),
        (" 그것으로 충분하다.", "<br>그것으로 충분하다."),
        (" 한 구절을 보탤 수 있다는 것.", "<br>한 구절을 보탤 수 있다는 것."),
    ]
    for old, new in replacements:
        if old in formatted:
            formatted = formatted.replace(old, new)
            break

    return formatted


if st.session_state.page == "input":
    st.title("오늘 체크인 🌿")
    st.markdown("네 마음을 천천히 적어줘.  \n오늘의 마음에 어울리는 문장 하나를 골라 줄게.")

    if "needs_clarification" not in st.session_state:
        st.session_state.needs_clarification = False

    with st.form("morning_checkin"):
        name = st.text_input("1. 이름을 알려줘.", key="name_input")
        mood = st.text_area("2. 지금 기분은 어떠니?", height=90, key="mood_input")

        clarified_emotion = ""
        if st.session_state.needs_clarification:
            st.markdown(
                '<div class="clarify-note">지금 감정을 한두 단어로 표현한다면 뭐라고 할 수 있을까?</div>'
                '<div class="clarify-sub">예: 답답함, 불안, 속상함, 편안함, 뿌듯함</div>',
                unsafe_allow_html=True,
            )
            clarified_emotion = st.text_input(
                "감정 한두 단어",
                label_visibility="collapsed",
                key="clarified_emotion_input",
            )

        reason = st.text_area("3. 지금 그런 기분이 드는 이유가 있어?", height=105, key="reason_input")
        wish = st.text_area("4. 바라는 것이 있어?", height=105, key="wish_input")

        button_label = (
            "감정 적고 열어보세요"
            if st.session_state.needs_clarification
            else "열어보세요"
        )

        submitted = st.form_submit_button(
            button_label,
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not all([name.strip(), mood.strip(), reason.strip(), wish.strip()]):
            st.warning("네 가지 질문에 모두 답해 줘.")

        elif not st.session_state.needs_clarification and needs_emotion_clarification(mood, reason):
            # 추가 감정 질문 단계로 넘어갈 때 현재 답변을 안전하게 보관
            st.session_state.pending_checkin = {
                "name": name.strip(),
                "mood": mood.strip(),
                "reason": reason.strip(),
                "wish": wish.strip(),
            }
            st.session_state.needs_clarification = True
            st.rerun()

        elif st.session_state.needs_clarification and not clarified_emotion.strip():
            st.warning("떠오르는 감정을 한두 단어로 적어 줘.")

        else:
            # 추가 질문 단계에서는 보관된 원래 답변을 기준으로 결과 생성
            pending = st.session_state.get(
                "pending_checkin",
                {
                    "name": name.strip(),
                    "mood": mood.strip(),
                    "reason": reason.strip(),
                    "wish": wish.strip(),
                },
            )

            # 사용자가 추가 질문 화면에서 기존 답변을 수정했다면 최신 값 반영
            pending["name"] = name.strip()
            pending["mood"] = mood.strip()
            pending["reason"] = reason.strip()
            pending["wish"] = wish.strip()

            was_clarified = st.session_state.needs_clarification
            clarified_value = clarified_emotion.strip() if was_clarified else ""
            mood_for_analysis = clarified_value if was_clarified else pending["mood"]

            chosen_idx, emotion, context, wish_label = choose_quote(
                mood_for_analysis,
                pending["reason"],
                pending["wish"],
            )

            clean_name = normalize_name_input(pending["name"])

            if "second_quote_idx" in st.session_state:
                del st.session_state["second_quote_idx"]

            st.session_state.result = {
                "name": clean_name,
                "mood": pending["mood"],
                "clarified_emotion": clarified_value,
                "analysis_mood": mood_for_analysis,
                "reason": pending["reason"],
                "wish": pending["wish"],
                "chosen_idx": chosen_idx,
                "emotion": emotion,
                "context": context,
                "wish_label": wish_label,
            }

            # 결과 페이지로 넘어가기 전에 추가 질문 상태를 종료
            st.session_state.needs_clarification = False
            if "pending_checkin" in st.session_state:
                del st.session_state["pending_checkin"]

            st.session_state.page = "result"
            st.rerun()

else:
    if "result" not in st.session_state:
        st.session_state.page = "input"
        st.session_state.needs_clarification = False
        st.rerun()

    result = st.session_state.result
    q = QUOTES[result["chosen_idx"]]
    call_name = vocative_name(result["name"])
    comfort, reason_for_quote = build_support_message(
        result["emotion"], result["context"], result["wish_label"]
    )
    card_class = pastel_class(result["emotion"])

    st.title("오늘 체크인 🌿")

    emotion_sentence = emotion_phrase_for_result(
        result["emotion"], result.get("clarified_emotion", "")
    ).rstrip(".!? ")

    first_line = f"{natural_reason_clause(result['reason'])} {emotion_sentence}."
    letter_lines = [first_line]
    letter_lines.extend(split_sentences_for_letter(comfort))
    letter_lines.append("네가 바라는 것이 이루어지기를 바라.")
    letter_lines.append(f"그래서 오늘은 {reason_for_quote} 이 문장을 골랐어.")

    result_sentence = "".join(
        f'<div class="letter-sentence">{line}</div>'
        for line in letter_lines
    )

    st.markdown(
        f"""
        <div class="result-box">
            <div class="letter-date">{today_korean_date()}</div>
            <div class="letter-body">
                <span class="letter-greeting">{call_name}.</span>
                {result_sentence}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="quote-card primary-card {card_class}">
            <div class="quote-inner">
                <div class="quote-title">오늘 {result['name']}에게 건네는 한 문장</div>
                <div class="quote-text">“{format_quote_card_text(q['text'])}”</div>
                <div class="quote-meta">— {q['author']}</div>
                <div class="quote-note">지금도<br>충분히 좋아 ♥</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "second_quote_idx" not in st.session_state:
        with st.container(key="gift_shell"):
            if st.button(
                "하나 더 선물",
                key="gift_shell_button",
                help="다른 문장 하나를 더 볼 수 있어.",
            ):
                st.session_state.second_quote_idx = choose_second_quote(
                    result["analysis_mood"],
                    result["reason"],
                    result["wish"],
                    result["chosen_idx"],
                )
                st.rerun()
        st.markdown(
            '<div class="gift-hint">조개를 톡 눌러봐</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="otter-static"><img src="assets/otter_shell_button.png" alt="수달"/></div>',
            unsafe_allow_html=True,
        )
        q2 = QUOTES[st.session_state.second_quote_idx]
        st.markdown(
            f"""
            <div class="quote-card secondary-card {card_class}" style="margin-top: 0.25rem;">
                <div class="quote-inner">
                    <div class="quote-title">하나 더 건네는 문장</div>
                    <div class="quote-text">“{format_quote_card_text(q2['text'])}”</div>
                    <div class="quote-meta">— {q2['author']}</div>
                    <div class="quote-note">지금 이 순간도<br>소중해 ♥</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("처음으로 돌아가기", use_container_width=True):
        st.session_state.page = "input"
        if "result" in st.session_state:
            del st.session_state.result
        if "second_quote_idx" in st.session_state:
            del st.session_state.second_quote_idx
        st.session_state.needs_clarification = False
        if "pending_checkin" in st.session_state:
            del st.session_state["pending_checkin"]
        for key in [
            "name_input",
            "mood_input",
            "reason_input",
            "wish_input",
            "clarified_emotion_input",
        ]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    st.markdown(
        '<div class="small-note">입력한 내용은 별도로 저장하지 않습니다.</div>',
        unsafe_allow_html=True,
    )
