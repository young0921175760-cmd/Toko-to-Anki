import os
import subprocess
import pytesseract
from PIL import Image
import csv
import re

# --- 核心路徑設定 ---
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "toko")
video_path = os.path.join(desktop_path, "toko_video.mp4") # 您的影片檔名
temp_folder = os.path.join(desktop_path, "temp_frames")    # 暫存圖片夾
output_csv = os.path.join(desktop_path, "toko_video_final.csv")

def is_chinese(char):
    """檢查是否為中文字符"""
    return '\u4e00' <= char <= '\u9fff'

def clean_text(text):
    """修正 OCR 錯誤：將 | 統一換成 I，並清理前後空白"""
    # 解決問題 3：強制將辨識錯誤的 | 換回 I
    text = text.replace('|', 'I')
    """修正 OCR 錯誤：將 > 統一換成 ，，並清理前後空白"""
    # 解決問題 3：強制將辨識錯誤的 | 換回 I
    text = text.replace('>', '，')
    return text.strip()

def clean_chinese_text(text):
    """專門清理中文：去除中文間的空格與換行"""
    # 解決問題 1 的中文部分：讓中文更緊湊
    text = text.replace('\n', '').replace(' ', '')
    return text.strip()

def process_content(raw_text, processed_set):
    """解析文字並自動分欄、換行、去重"""
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    results = []
    current_eng = ""
    
    for line in lines:
        line = clean_text(line) 
        has_chinese = any(is_chinese(char) for char in line)
        
        if not has_chinese:
            # 【邏輯：英文】如果這行沒中文，視為英文句子的一部分
            if current_eng:
                current_eng += " " + line
            else:
                current_eng = line
        else:
            # 【邏輯：中文】看到中文代表這組英文結束了
            chi_sentence = clean_chinese_text(line)
            eng_sentence = current_eng.strip()
            
            # 解決問題 2：去重檢查（英文+中文組合沒出現過才存入）
            unique_key = f"{eng_sentence}{chi_sentence}"
            if eng_sentence and chi_sentence and unique_key not in processed_set:
                # 解決問題 1：英文放左欄，中文放右欄
                results.append([eng_sentence, chi_sentence])
                processed_set.add(unique_key)
            
            # 重置英文緩衝，準備下一組
            current_eng = ""
            
    return results

def main():
    # 檢查影片是否存在
    if not os.path.exists(video_path):
        print(f"❌ 找不到影片檔案：{video_path}")
        return

    # 1. 建立暫存資料夾
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # 2. 呼叫 FFmpeg 擷取畫面 (每 3 秒抓一張)
    print("🚀 步驟 1: 正在使用 FFmpeg 擷取影片畫面...")
    subprocess.run([
        'ffmpeg', '-i', video_path, 
        '-vf', 'fps=1/5', 
        os.path.join(temp_folder, 'frame_%04d.jpg'),
        '-y'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 3. 辨識圖片內容
    all_data = []
    processed_set = set() # 用於全域去重
    files = sorted([f for f in os.listdir(temp_folder) if f.endswith('.jpg')])
    
    print(f"🚀 步驟 2: 開始辨識 {len(files)} 張擷取畫面...")

    for filename in files:
        img_path = os.path.join(temp_folder, filename)
        # 使用 psm 6 適合對話塊格式
        raw_text = pytesseract.image_to_string(Image.open(img_path), lang='eng+chi_tra', config='--psm 6')
        
        # 智慧解析與去重
        pairs = process_content(raw_text, processed_set)
        all_data.extend(pairs)
        print(f"✅ 已處理時間點: {filename}")

    # 4. 寫入 CSV
    with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['English (Front)', 'Chinese (Back)'])
        writer.writerows(all_data)

    print(f"\n🎉 任務完成！")
    print(f"📊 共擷取到 {len(all_data)} 條不重複對話。")
    print(f"📍 檔案已存至桌面：{output_csv}")

if __name__ == "__main__":
    main()