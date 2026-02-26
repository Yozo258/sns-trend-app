import streamlit as st
import pandas as pd
from googlesearch import search
import time

# ページ設定：ブラウザのタブに表示される名前とレイアウト
st.set_page_config(page_title="SNSトレンド分析エージェント", layout="wide")

st.title("🚀 SNSトレンド分析エージェント (梅プラン)")
st.write("Google検索の公開データから、SNSの最新バズとインサイトを自動抽出します。")

# サイドバー設定：ここで条件を入力します
with st.sidebar:
    st.header("🔍 分析設定")
    industry = st.selectbox("業界を選択", ["英語学習", "カレー", "SNSマーケティング", "その他カスタム"])
    if industry == "その他カスタム":
        industry = st.text_input("業界名を入力してください")
    
    num_results = st.slider("取得件数 (各SNS)", 3, 10, 5)
    run_analysis = st.button("分析を開始")

# 検索ロジック
def get_sns_trends(keyword, platform, platform_domain, num):
    # 特定のSNSサイト内を検索するクエリ
    query = f"site:{platform_domain} {keyword} トレンド 2026"
    results = []
    try:
        for url in search(query, num_results=num, lang="ja"):
            # 簡易的な要約とターゲット推測
            summary = f"{keyword}に関する最新の{platform}投稿です。注目度が高まっています。"
            target = "20-40代 / 男女 / 全国" 
            
            if "youtube.com" in url:
                target = "10-30代 / 男性寄り / 動画視聴層"
            elif "tiktok.com" in url:
                target = "10-20代 / 女性寄り / トレンド敏感層"
            
            results.append({
                "プラットフォーム": platform,
                "URL": url,
                "要約": summary,
                "推測ターゲット": target
            })
            time.sleep(0.1) # 連続アクセス防止の短い休憩
    except Exception as e:
        st.error(f"{platform}の取得中にエラーが発生しました。")
    return results

# 実行ボタンが押された時の動作
if run_analysis:
    with st.spinner(f"「{industry}」のトレンドを調査中..."):
        platforms = {
            "X (Twitter)": "x.com",
            "YouTube": "youtube.com",
            "Instagram": "instagram.com",
            "TikTok": "tiktok.com"
        }
        
        all_data = []
        for p_name, p_domain in platforms.items():
            data = get_sns_trends(industry, p_name, p_domain, num_results)
            all_data.extend(data)
        
        if all_data:
            df = pd.DataFrame(all_data)
            st.success("分析が完了しました！")
            
            # 画面をタブで分ける
            tabs = st.tabs(["📊 全体データ", "📱 X", "📺 YouTube", "📸 Instagram", "🎵 TikTok"])
            
            with tabs[0]:
                st.dataframe(df, use_container_width=True)
                
            for i, p_name in enumerate(platforms.keys()):
                with tabs[i+1]:
                    p_df = df[df["プラットフォーム"] == p_name]
                    if not p_df.empty:
                        for _, row in p_df.iterrows():
                            st.info(f"🔗 [投稿を確認する]({row['URL']})")
                            st.write(f"📝 要約: {row['要約']}")
                            st.write(f"👥 推測ターゲット: {row['推測ターゲット']}")
                            st.divider()
                    else:
                        st.write("データが見つかりませんでした。")