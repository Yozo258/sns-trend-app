import streamlit as st
import pandas as pd
from googlesearch import search
import time

st.set_page_config(page_title="SNSトレンド分析", layout="wide")

st.title("🚀 SNSトレンド分析エージェント (梅プラン・安定版)")

with st.sidebar:
    st.header("🔍 分析設定")
    industry = st.selectbox("業界を選択", ["英語学習", "カレー", "SNSマーケティング", "その他カスタム"])
    if industry == "その他カスタム":
        industry = st.text_input("業界名を入力")
    
    num_results = st.slider("取得件数 (各SNS)", 1, 5, 3) # 負荷を下げて確実に取得
    run_analysis = st.button("分析を開始")

def get_sns_trends(keyword, platform, platform_domain, num):
    # クエリをより具体的にしてヒット率を上げる
    query = f"site:{platform_domain} {keyword} 人気 投稿 2026"
    results = []
    try:
        # 検索実行を可視化
        st.write(f"📡 {platform} をスキャン中...")
        search_results = search(query, num_results=num, lang="ja", sleep_interval=2)
        
        for url in search_results:
            results.append({
                "プラットフォーム": platform,
                "URL": url,
                "要約": f"{keyword}に関する注目の投稿です。",
                "推測ターゲット": "全年代 / 男女"
            })
    except Exception as e:
        st.error(f"{platform} の取得でエラーが発生しました。時間を空けて試してください。")
    return results

if run_analysis:
    if not industry:
        st.warning("業界を入力してください。")
    else:
        with st.spinner(f"「{industry}」のトレンドを調査しています..."):
            platforms = {
                "X (Twitter)": "x.com",
                "YouTube": "youtube.com",
                "Instagram": "instagram.com",
                "TikTok": "tiktok.com"
            }
            
            all_data = []
            progress_bar = st.progress(0)
            
            for i, (p_name, p_domain) in enumerate(platforms.items()):
                data = get_sns_trends(industry, p_name, p_domain, num_results)
                all_data.extend(data)
                progress_bar.progress((i + 1) / len(platforms))
            
            if all_data:
                df = pd.DataFrame(all_data)
                st.success(f"合計 {len(all_data)} 件のデータが見つかりました！")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("データが1件も見つかりませんでした。Googleの検索制限にかかっている可能性があるため、5分ほど待ってから別のキーワード（例：『スパイスカレー』など具体的に）で試してください。")