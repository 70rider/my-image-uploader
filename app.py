import streamlit as st
import requests
import base64

st.title("GitHub画像アップローダー")

# 1. Secretsから情報を取得（ブラウザからは絶対に見えない）
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
REPO_NAME = "70rider/webcamera"
BRANCH = "main"

uploaded_file = st.file_uploader("画像を選択してください", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    file_name = uploaded_file.name
    st.image(uploaded_file, caption="プレビュー", use_container_width=True)

    if st.button("GitHubにアップロード"):
        # 画像をBase64に変換
        content = base64.b64encode(uploaded_file.read()).decode("utf-8")
        
        # GitHub API のエンドポイント
        url = f"https://api.github.com/repos/{REPO_NAME}/contents/images/{file_name}"
        
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "message": f"Upload {file_name} via Streamlit",
            "content": content,
            "branch": BRANCH
        }

        # API実行
        response = requests.put(url, json=data, headers=headers)

        if response.status_code in [200, 201]:
            # アップロードしたファイルの直リンクURLを生成
            raw_url = f"https://raw.githubusercontent.com/{REPO_NAME}/{BRANCH}/images/{file_name}"
            
            st.success("GitHubへのアップロードが完了しました！")
            
            # URLを表示してコピーしやすくする
            st.code(raw_url, language="text")
            st.markdown(f"[画像をブラウザで確認する]({raw_url})")
            
            # Markdown用の貼り付けコードもついでに表示
            st.subheader("Markdown用コード")
            st.code(f"![{file_name}]({raw_url})", language="markdown")
        else:
            st.error(f"失敗しました: {response.json().get('message')}")