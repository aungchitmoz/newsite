#!/usr/bin/env python3
"""
Generate polymarket_strategies.pdf — Polymarket Quant Trading Bot Strategies (Burmese)
Run: python3 generate_pdf.py
Requires: reportlab, fonts-noto (NotoSansMyanmar)
"""

import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)

# ---------------------------------------------------------------------------
# Font registration
# ---------------------------------------------------------------------------
_FONT_PATHS = [
    "/usr/share/fonts/truetype/noto/NotoSansMyanmar-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansMyanmarUI-Regular.ttf",
]
_FONT_BOLD_PATHS = [
    "/usr/share/fonts/truetype/noto/NotoSansMyanmar-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansMyanmarUI-Bold.ttf",
]

FONT_REG = next((p for p in _FONT_PATHS if os.path.exists(p)), None)
FONT_BOLD = next((p for p in _FONT_BOLD_PATHS if os.path.exists(p)), None)

if FONT_REG is None or FONT_BOLD is None:
    raise RuntimeError(
        "NotoSansMyanmar fonts not found. "
        "Install with: sudo apt-get install fonts-noto"
    )

pdfmetrics.registerFont(TTFont("NotoMyanmar", FONT_REG))
pdfmetrics.registerFont(TTFont("NotoMyanmar-Bold", FONT_BOLD))

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
W, H = A4
MARGIN = 20 * mm

title_style = ParagraphStyle(
    "title",
    fontName="NotoMyanmar-Bold",
    fontSize=18,
    leading=30,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#1a237e"),
    spaceAfter=6,
)

subtitle_style = ParagraphStyle(
    "subtitle",
    fontName="NotoMyanmar",
    fontSize=11,
    leading=18,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#37474f"),
    spaceAfter=10,
)

section_style = ParagraphStyle(
    "section",
    fontName="NotoMyanmar-Bold",
    fontSize=14,
    leading=22,
    alignment=TA_LEFT,
    textColor=colors.HexColor("#0d47a1"),
    spaceBefore=14,
    spaceAfter=4,
)

subsection_style = ParagraphStyle(
    "subsection",
    fontName="NotoMyanmar-Bold",
    fontSize=12,
    leading=20,
    alignment=TA_LEFT,
    textColor=colors.HexColor("#1565c0"),
    spaceBefore=10,
    spaceAfter=3,
)

body_style = ParagraphStyle(
    "body",
    fontName="NotoMyanmar",
    fontSize=10,
    leading=18,
    alignment=TA_JUSTIFY,
    textColor=colors.HexColor("#212121"),
    spaceAfter=4,
)

bullet_style = ParagraphStyle(
    "bullet",
    fontName="NotoMyanmar",
    fontSize=10,
    leading=18,
    alignment=TA_LEFT,
    textColor=colors.HexColor("#212121"),
    leftIndent=12,
    spaceAfter=2,
)

note_style = ParagraphStyle(
    "note",
    fontName="NotoMyanmar",
    fontSize=9,
    leading=16,
    alignment=TA_LEFT,
    textColor=colors.HexColor("#546e7a"),
    leftIndent=8,
    spaceAfter=4,
)

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#90a4ae"), spaceAfter=6)


def sp(h=4):
    return Spacer(1, h * mm)


def sec(text):
    return [sp(2), Paragraph(text, section_style), hr()]


def subsec(text):
    return [Paragraph(text, subsection_style)]


def body(text):
    return Paragraph(text, body_style)


def bullets(items):
    return [Paragraph(f"• {item}", bullet_style) for item in items]


def note(text):
    return Paragraph(f"မှတ်ချက်: {text}", note_style)


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------

def build_story():
    story = []

    # ---- Cover ----
    story += [
        sp(10),
        Paragraph("Polymarket Quant Trading Bot", title_style),
        Paragraph("ဗျူဟာများ စုစည်းမှု", title_style),
        sp(3),
        Paragraph(
            "ယေဘုယျ၊ E-Sports၊ Crypto နှင့် ၅-မိနစ် Crypto ဈေးကွက်များအတွက်",
            subtitle_style,
        ),
        Paragraph(
            "Polymarket တွင် အသုံးပြုနိုင်သော Algorithmic / Quant Strategy များ",
            subtitle_style,
        ),
        sp(4),
        hr(),
        PageBreak(),
    ]

    # ==================================================================
    # 1. GENERAL TRADING STRATEGIES
    # ==================================================================
    story += sec("၁။ ယေဘုယျ Trading Bot ဗျူဟာများ (General Trading Strategies)")
    story.append(body(
        "Polymarket သည် prediction market platform တစ်ခုဖြစ်ပြီး အမှန်တကယ် ဖြစ်ပျက်မည့် "
        "အဖြေများပေါ် YES/NO သဘောဆောင်သော shares ဝယ်ချင်းဖြင့် ကိုယ်စားပြုသည်။ "
        "Quant bot တစ်ခုကို ရေးသားရာတွင် အောက်ပါ ဗျူဟာများ အသုံးပြုနိုင်သည်။"
    ))

    # 1.1
    story += subsec("၁.၁ Market-Making (ဈေးကွက် ဖန်တီးခြင်း)")
    story.append(body(
        "Bot သည် YES နှင့် NO ဘက်နှစ်ဘက်လုံးတွင် bid/ask ကမ်းလှမ်းချက်များထည့်ကာ "
        "spread ကနေ အမြတ်ယူသည့် နည်းလမ်းဖြစ်သည်။"
    ))
    story += bullets([
        "Bid-Ask Spread ကို အနည်းဆုံး ၂-၃% ထားပါ။",
        "Volume နည်းသော market တွင် inventory risk ကြီးသောကြောင့် position size ကို ထိန်းချုပ်ပါ။",
        "Fair value ကို Kelly Criterion ဖြင့် တွက်ချက်ပြီး spread ကို ချိန်ညှိပါ။",
        "Inventory imbalance ဖြစ်ပါက ဘက်တစ်ဘက် quote ကို ရုတ်သိမ်းပါ။",
    ])

    # 1.2
    story += subsec("၁.၂ Arbitrage (ဈေးကွက်ကွာဟချက် အမြတ်ယူခြင်း)")
    story.append(body(
        "Polymarket နှင့် Manifold Markets၊ Kalshi၊ PredictIt ကဲ့သို့သော platform များအကြား "
        "ဈေးနှုန်းကွာခြားမှုကို ရှာဖွေ အမြတ်ယူသည်။"
    ))
    story += bullets([
        "Cross-platform price ကို real-time ဆွဲယူပြီး delta > ₵5 ဆိုပါက အမြတ်ယူပါ။",
        "Gas fee၊ slippage၊ latency တို့ကို ထည့်သွင်းတွက်ချက်ပါ။",
        "Correlated markets (ဥပမာ - presidential election) တွင် related contracts ကြား arbitrage ရှာပါ။",
        "Execution လုပ်ရာတွင် atomic ဖြစ်အောင် websocket + REST ပေါင်းသုံးပါ။",
    ])

    # 1.3
    story += subsec("၁.၃ Sentiment & News-Based Trading")
    story.append(body(
        "Social media (Twitter/X)၊ news API၊ Reddit တို့မှ sentiment ကို NLP ဖြင့် ဆန်းစစ်ကာ "
        "market ဈေးနှုန်းနှင့် drift ကို ခန့်မှန်းသည်။"
    ))
    story += bullets([
        "FinBERT သို့မဟုတ် GPT ကို fine-tune လုပ်ထားသော model ဖြင့် sentiment score ဆွဲပါ။",
        "Score > +0.7 ဆိုပါက YES ဝယ်၊ < -0.7 ဆိုပါက NO ဝယ် ဟု threshold သတ်မှတ်ပါ။",
        "News velocity (ဆောင်းပါး အရေအတွက် တစ်နာရီ) ကို signal အဖြစ် ထည့်သွင်းပါ။",
        "Contrarian mode: hype ပြင်းပါက ကိုယ်တိုင် probability check လုပ်ပြီး counter-trade ပြုလုပ်ပါ။",
    ])

    # 1.4
    story += subsec("၁.၄ Probability Calibration Model")
    story.append(body(
        "Statistical/ML model ဖြင့် fair probability ကို တွက်ချက်ကာ market ဈေးနှင့် "
        "ကွာဟမှုရှိပါက edge ယူသည်။"
    ))
    story += bullets([
        "Logistic Regression / XGBoost / LightGBM ဖြင့် binary outcome model တည်ဆောက်ပါ။",
        "Historical resolution data ကို training set အဖြစ် သုံးပါ (Polymarket API မှ ဒေါင်းလုပ်နိုင်)။",
        "Model probability vs market price ကွာ > ₵10 ဆိုပါက trade ဖွင့်ပါ။",
        "Ensemble method (stacking) ဖြင့် model accuracy ကို မြှင့်ပါ။",
    ])

    # 1.5
    story += subsec("၁.၅ Kelly Criterion Position Sizing")
    story.append(body(
        "Kelly formula ဖြင့် optimal bet size ကို တွက်ချက်ကာ bankroll ကို ကာကွယ်သည်။"
    ))
    story += bullets([
        "f* = (bp - q) / b ဖော်မြူလာ (b=odds, p=win prob, q=1-p) ကို အသုံးပြုပါ။",
        "Full Kelly ဆိုသည်မှာ ဘဏ္ဍာများ ဆုံးရှုံးနိုင်မှု မြင့်သောကြောင့် Quarter/Half Kelly ကို မြှောက်ပြေပြီး risk ချပါ။",
        "Portfolio ခြုံငုံ Kelly ကို ဆွက်ပြီး ဘဏ္ဍာ ၂%-၅% ထက် မကျော်ပါနှင့်။",
    ])
    story.append(note(
        "Risk management ကို အမြဲတမ်း ဦးစားပေးပါ။ Kelly သည် long-run optimal ဆိုသော်လည်း short-run variance ကြီးနိုင်သည်။"
    ))

    # ==================================================================
    # 2. ESPORTS STRATEGIES
    # ==================================================================
    story += sec("၂။ E-Sports ဈေးကွက် ဗျူဟာများ (Esports Market Strategies)")
    story.append(body(
        "CS2၊ Dota 2၊ League of Legends၊ Valorant ကဲ့သို့သော e-sports ပြိုင်ပွဲများ "
        "Polymarket တွင် ရနိုင်သည်။ အောက်ပါ ဗျူဟာများ ထူးထူးခြားခြား သက်ရောက်မှု ရှိသည်။"
    ))

    story += subsec("၂.၁ Head-to-Head Historical Performance Analysis")
    story += bullets([
        "Teams ၂ ဖွဲ့ကြားက ယခင်ပွဲဆိုင်ရာ ရလဒ်၊ win rate၊ map win rate ကို ဆန်းစစ်ပါ။",
        "Liquipedia / HLTV API မှ match data ဆွဲပြီး feature engineering လုပ်ပါ။",
        "Home/Away သဘောဆောင်မှု (LAN vs Online)၊ roster change ကို signal ထဲ ထည့်ပါ။",
        "Last 3-month form > All-time average ကို ပိုအလေးပေးပါ (exponential decay weight)။",
    ])

    story += subsec("၂.၂ Live In-Game Data Signals")
    story += bullets([
        "CS2: round win/loss economy (pistol round loss → lower buy probability) ကို real-time monitor လုပ်ပါ။",
        "Dota 2 / LoL: net worth lead > 10k gold ဆိုပါက ခေါင်းဆောင်သော team ၏ YES ကို buy ပါ။",
        "Live kill/death ratio signal ကို Polymarket API latency ထက် မြန်သော data source မှ ရယူပါ။",
        "In-play market ဈေးကွက်တွင် momentum trading: ၃ rounds ဆက်တိုက် win ဆိုပါက YES probability ကို reevaluate ပါ။",
    ])

    story += subsec("၂.၃ Tournament Bracket & Meta Analysis")
    story += bullets([
        "Tournament structure (single elimination vs double)၊ seeding ကို model ထဲ ထည့်ပါ။",
        "Current patch meta ကို ဆန်းစစ်ပြီး meta-favored team ကို edge ပေးပါ။",
        "Fatigue factor: back-to-back match ၃ ပွဲ ကျော်ပါက performance ကျသည် ကို model ထဲ ထည့်ပါ။",
        "Coach/analyst tier rating ကို proxy signal အဖြစ် ထည့်ပါ။",
    ])

    story += subsec("၂.၄ Odds Comparison with Bookmakers")
    story += bullets([
        "Bet365၊ Pinnacle မှ esports odds ကို base probability မှ extract လုပ်ပါ (margin ဖြုတ်)။",
        "Polymarket YES price < Bookmaker implied probability ဆိုပါက YES ဝယ်ပါ။",
        "Sharp bettor movement (line movement > 10%) ကို signal ထဲ ထည့်ပါ။",
    ])
    story.append(note(
        "E-Sports market မှာ liquidity နည်းသောကြောင့် large position ဝင်ပါက slippage ကြီးနိုင်သည်။ "
        "Position limit ကို ₵500 ခန့်ထားပါ။"
    ))

    story.append(PageBreak())

    # ==================================================================
    # 3. CRYPTO STRATEGIES
    # ==================================================================
    story += sec("၃။ Crypto ဈေးကွက် ဗျူဟာများ (Crypto Market Strategies)")
    story.append(body(
        "Bitcoin ETF approval၊ Ethereum upgrade၊ altcoin listing၊ regulatory decision ကဲ့သို့သော "
        "crypto-related prediction market များအတွက် အထူး ဗျူဟာများဖြစ်သည်။"
    ))

    story += subsec("၃.၁ On-Chain Metrics Signal")
    story += bullets([
        "Exchange net flow (negative = withdrawal surge = bullish) ကို signal ထဲ ထည့်ပါ။",
        "Whale wallet movement (> 1000 BTC transfer) ကို Whale Alert API မှ monitor လုပ်ပါ။",
        "Active addresses growth rate > ၃ month average ဆိုပါက bullish signal ဖြစ်သည်။",
        "SOPR (Spent Output Profit Ratio) > 1 ဆိုပါက bull market continuation signal။",
        "Glassnode / CryptoQuant API မှ on-chain data ဆွဲပြီး real-time signal ရပါ။",
    ])

    story += subsec("၃.၂ Regulatory & Fundamental Event Model")
    story += bullets([
        "SEC/CFTC ဆုံးဖြတ်ချက် ရက်စွဲကို calendar ထဲ ထည့်ကာ ၇ ရက် ကြိုတင် position ဝင်ပါ။",
        "ETF approval ဆိုင်ရာ court ruling ကို NLP ဖြင့် text classification ပြုလုပ်ပါ ('likely approve' → YES ဝယ်)။",
        "Fed interest rate decision နှင့် crypto correlation (negative) ကို ထည့်သွင်းပါ။",
        "FUD (Fear Uncertainty Doubt) event (exchange hack၊ rug pull) နောက် ၄၈ နာရီ mean reversion ကို ရှာပါ။",
    ])

    story += subsec("၃.၃ Technical Indicator-Based Signals")
    story += bullets([
        "BTC/ETH RSI > 70 (overbought) ဆိုပါက price target miss ဖြစ်နိုင်ချေ မြင့်သောကြောင့် NO ကို consider ပါ။",
        "200-day MA အပေါ် trade ဆိုပါက macro bull signal → price target hit YES ကို ဝယ်ပါ။",
        "Volume surge (average ၃x ကျော်) = breakout signal → directional bet ဖွင့်ပါ。",
        "Fear & Greed Index < 20 ဆိုပါက contrarian YES ဝယ် (extreme fear = buying opportunity)。",
    ])

    story += subsec("၃.၄ Correlation-Based Portfolio Hedging")
    story += bullets([
        "BTC ↗ ကိုယ်ပြောင်းကာ ETH/SOL YES ကို hedge အဖြစ် hold ပါ (correlation > 0.85)。",
        "Stablecoin dominance rise = risk-off environment → crypto YES markets တွင် exposure ကို လျှော့ပါ。",
        "Cross-market spread: Futures implied price vs Spot price → funding rate signal ကို ထည့်ပါ。",
    ])

    story += subsec("၃.၅ Machine Learning Price Prediction Integration")
    story += bullets([
        "LSTM/Transformer model ဖြင့် ၇-ရက် forward price ကို predict လုပ်ပြီး target YES/NO ဆုံးဖြတ်ပါ。",
        "Feature set: OHLCV, on-chain metrics, sentiment score, macro indicators ပေါင်းထည့်ပါ。",
        "Ensemble: model prediction + fundamental event calendar + sentiment = final signal。",
        "Backtesting ကို walk-forward validation ဖြင့် overfitting ကာကွယ်ပါ。",
    ])
    story.append(note(
        "Crypto market သည် 24/7 လည်ပတ်သောကြောင့် bot monitoring ကို alert system (Telegram/Slack) "
        "ဖြင့် ချိတ်ဆက်ထားပါ။"
    ))

    # ==================================================================
    # 4. 5-MINUTE UP/DOWN CRYPTO STRATEGIES
    # ==================================================================
    story += sec("၄။ ၅-မိနစ် Up/Down Crypto ဈေးကွက် ဗျူဟာများ (5-Minute Up/Down Crypto Strategies)")
    story.append(body(
        "Polymarket တွင် '5 မိနစ်အတွင်း BTC ဈေးနှုန်း တက်မည်လား ကျမည်လား' ဆိုသော "
        "short-term binary market များ ရနိုင်သည်။ ဤ high-frequency event market များသည် "
        "အောက်ပါ ဗျူဟာများ အသုံးဝင်သည်。"
    ))

    story += subsec("၄.၁ Order Book Imbalance (OBI) Strategy")
    story += bullets([
        "Top 5 bid/ask level ၏ cumulative volume ratio ကို real-time တွက်ပါ。",
        "OBI = (Bid Volume - Ask Volume) / (Bid Volume + Ask Volume)。",
        "OBI > +0.3 ဆိုပါက UP ဘက် (YES) ၊ OBI < -0.3 ဆိုပါက DOWN ဘက် (YES) ကို ဝယ်ပါ。",
        "Binance / Bybit websocket order book stream ကို low-latency ဖြင့် subscribe လုပ်ပါ。",
        "Stale order (၅ sec တော့ refresh မဖြစ်) ကို signal မှ ဖယ်ထုတ်ပါ。",
    ])

    story += subsec("၄.၂ Momentum & VWAP Signal")
    story += bullets([
        "Last 30-second candle pattern: ဆက်တိုက် ၃ bullish candle ဆိုပါက UP signal。",
        "Price vs ၅-မိနစ် VWAP: Price > VWAP = UP edge, Price < VWAP = DOWN edge。",
        "Tick speed (trades per second) acceleration = momentum continuation signal。",
        "Bid-ask midpoint rate of change > 0.05% per 10 sec = strong directional signal。",
    ])

    story += subsec("၄.၃ Micro-Structure Mean Reversion")
    story += bullets([
        "Price spike > 0.3% within 30 seconds ဆိုပါက mean reversion trade ဖွင့်ပါ。",
        "High spread + low volume = informed trading signal မဟုတ်ဘဲ noise ဖြစ်နိုင်ချေ မြင့်သည်。",
        "Liquidation cascade (large liquidations detected) နောက် bounce ကို ရှာပါ。",
        "Stop-loss cluster zones (round numbers: $100k, $95k) ကို support/resistance အဖြစ် သုံးပါ。",
    ])

    story += subsec("၄.၄ Volatility-Adjusted Sizing")
    story += bullets([
        "ATR (Average True Range) ၁-မိနစ် တိုင်းတာကာ volatility မြင့်ပါက position size ကို လျှော့ပါ。",
        "Low volatility window (ATR < threshold) တွင် OBI signal ကို ပိုယုံကြည်ပါ。",
        "High volatility: Model မှ bet ဖြုတ်ပြီး sideline နေပါ (choppy market = false signals)。",
    ])

    story += subsec("၄.၅ Latency & Execution Optimization")
    story += bullets([
        "WebSocket ကို REST ထက် သုံးပါ (data latency ၁၀x နည်းသည်)。",
        "Colocated server (AWS ap-southeast-1 / Tokyo) ကို Binance endpoint နားတွင် ထားပါ。",
        "Execution: market order ကို ဦးစားမပေးဘဲ aggressive limit order သုံးပါ (slippage ကာကွယ်)。",
        "Order fill monitoring: ၂ sec အတွင်း fill မဖြစ်ပါက cancel ပြီး recalculate ပြုလုပ်ပါ。",
        "Position open ပြီး Polymarket contract ဈေးနှုန်း ၁% ကျသွားပါက stop-loss ပိတ်ပါ。",
    ])

    story += subsec("၄.၆ Combining Signals (Multi-Factor Scoring)")
    story.append(body(
        "Single signal ထက် multiple signal ပေါင်းစပ် scoring system ကို အသုံးပြုပါ："
    ))
    story += bullets([
        "Score = OBI (weight 0.4) + Momentum (weight 0.3) + VWAP deviation (weight 0.2) + Volatility filter (weight 0.1)",
        "Score > 0.6 → UP (YES) trade, Score < -0.6 → DOWN (YES) trade, အလယ် → No trade。",
        "Walk-forward backtesting ဖြင့် weight ကို optimize လုပ်ပါ (overfitting ကို မဖြစ်စေရ)。",
        "Live paper trading ကို ၂ ပတ် ပြုလုပ်ပြီးမှ real capital ဝင်ပါ。",
    ])
    story.append(note(
        "₵5 မိနစ် market တွင် trading fee / gas cost သည် edge ကို ပြန်ဖျက်နိုင်သည်。 "
        "Net edge > transaction cost ဖြစ်မဖြစ် ပြန်စစ်ပါ。"
    ))

    # ==================================================================
    # 5. RISK MANAGEMENT & BOT INFRASTRUCTURE
    # ==================================================================
    story += sec("၅။ Risk Management နှင့် Bot Infrastructure")

    story += subsec("၅.၁ Risk Controls")
    story += bullets([
        "Daily loss limit: Bankroll ၁၀% ကျပါက bot ကို auto-stop ပြုလုပ်ပါ。",
        "Max concurrent positions: ၅-၁၀ ထက် မကျော်ပါနှင့်。",
        "Correlation check: Highly correlated positions ကို hedge မလုပ်ဘဲ ကြိုတင် လျှော့ပါ。",
        "Emergency kill switch: Manual override button ကို dashboard တွင် ထည့်ပါ。",
    ])

    story += subsec("၅.၂ Tech Stack Recommendations")
    story += bullets([
        "Language: Python 3.11+ (asyncio + aiohttp for async API calls)。",
        "Data pipeline: Apache Kafka / Redis Streams for real-time feed processing。",
        "Database: TimescaleDB (time-series) + PostgreSQL (fundamentals)。",
        "Monitoring: Grafana + Prometheus + PagerDuty alert。",
        "Backtesting: Backtrader / Zipline / VectorBT。",
        "Deployment: Docker + Kubernetes on AWS/GCP with auto-scaling。",
    ])

    story += subsec("₅.₃ Polymarket API Notes")
    story += bullets([
        "CLOB API (Central Limit Order Book) မှ real-time order book data ရပါသည်。",
        "GraphQL endpoint မှ market metadata, resolution, outcomes ဆွဲနိုင်သည်。",
        "Polygon network (USDC) ဖြင့် settlement ဖြစ်ပြီး wallet API key လိုအပ်သည်。",
        "Rate limit: API call တစ်မိနစ် ၁၂၀ ကျော်ပါက ban ဖြစ်နိုင်သောကြောင့် caching သုံးပါ。",
    ])

    # ---- Footer page ----
    story.append(PageBreak())
    story += [
        sp(6),
        hr(),
        Paragraph(
            "ကျမ်းကိုးများ (References)",
            ParagraphStyle(
                "ref_head",
                fontName="NotoMyanmar-Bold",
                fontSize=11,
                leading=18,
                textColor=colors.HexColor("#37474f"),
                spaceAfter=4,
            ),
        ),
    ]
    refs = [
        "Polymarket Developer Docs — https://docs.polymarket.com",
        "Kelly Criterion — Kelly, J. L. (1956). Bell System Technical Journal.",
        "Glassnode On-Chain Metrics — https://glassnode.com",
        "HLTV Esports Data — https://hltv.org",
        "Binance WebSocket API — https://binance-docs.github.io",
        "VectorBT Backtesting — https://vectorbt.pro",
    ]
    for r in refs:
        story.append(
            Paragraph(
                f"• {r}",
                ParagraphStyle(
                    "ref",
                    fontName="NotoMyanmar",
                    fontSize=9,
                    leading=15,
                    textColor=colors.HexColor("#546e7a"),
                    leftIndent=8,
                    spaceAfter=2,
                ),
            )
        )

    story += [
        sp(4),
        hr(),
        Paragraph(
            "ဤ PDF သည် Polymarket quant trading bot ဗျူဟာများဆိုင်ရာ "
            "အသိပညာမျှဝေမှုအတွက် ဖန်တီးထားသည်။ "
            "ရင်းနှီးမြှုပ်နှံမှု အကြံပေးချက် မဟုတ်ပါ။",
            ParagraphStyle(
                "disclaimer",
                fontName="NotoMyanmar",
                fontSize=8,
                leading=14,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#90a4ae"),
                spaceAfter=0,
            ),
        ),
    ]

    return story


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "polymarket_strategies.pdf")
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title="Polymarket Quant Trading Bot Strategies",
        author="aungchitmoz/newsite",
        subject="Polymarket ဗျူဟာများ - ဗမာဘာသာ",
    )
    doc.build(build_story())
    print(f"PDF created: {output_path}")


if __name__ == "__main__":
    main()
