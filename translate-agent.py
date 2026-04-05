import os
import sys
from google import genai

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY 環境變數未設定。請確認 GitHub Secrets 是否有正確對應。")
        sys.exit(1)

    upstream_file = "repos/upstream/README.md"
    current_file = "repos/current/README.md"
    
    try:
        with open(upstream_file, "r", encoding="utf-8") as f:
            upstream_content = f.read()
    except FileNotFoundError:
        print(f"Error: 找不到上游文件 {upstream_file}，無需翻譯。")
        sys.exit(0)

    prompt = f"""
    你是一個精通軟體工程與開源專案的專業翻譯助理。
    你的任務是將以下 GitHub 專案的英文 README 文件翻譯為「繁體中文 (zh-TW)」。
    
    【嚴格限制】：
    1. 絕對不要破壞任何 Markdown 格式（包含標題、超連結、程式碼區塊、粗體等）。
    2. 絕對不要增加任何與翻譯無關的對話，直接輸出翻譯結果。
    
    【原文內容開始】
    {upstream_content}
    【原文內容結束】
    """

    print("🚀 啟動 Agent：與 Gemini 進行通訊中...")
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        translated_content = response.text.strip()
    except Exception as e:
        print(f"API 呼叫失敗: {e}")
        sys.exit(1)
    
    print(f"📝 翻譯完成，正在寫入 {current_file}")
    with open(current_file, "w", encoding="utf-8") as f:
        f.write(translated_content)
        
    print("✅ 任務執行完畢。")

if __name__ == "__main__":
    main()
