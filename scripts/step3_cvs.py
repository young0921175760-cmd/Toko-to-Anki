import csv
import os

# 設定檔案路徑
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "toko")
input_csv = os.path.join(desktop_path, "toko_video_final.csv")
output_csv = os.path.join(desktop_path, "toko_anki_ready.csv")

def transform_csv():
    if not os.path.exists(input_csv):
        print(f"❌ 找不到原始檔案：{input_csv}")
        return

    processed_rows = []

    with open(input_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader) # 讀取標題列 ['English (Front)', 'Chinese (Back)']
        
        header.append("標籤")

        for row in reader:
            if len(row) < 2:
                continue
            
            eng = row[0].strip()
            chi = row[1].strip()
            
            # 核心邏輯：將中文欄位修改為 [換行 + 英文內容 + 原本中文]
            # \n 是換行符號
            new_chi_content = f"{chi}"
            new_eng_content = f"> {eng}"
            tag = "口語"
            processed_rows.append([new_chi_content,new_eng_content,tag])

    # 寫回新的 CSV
    with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(processed_rows)

    print(f"🎉 處理完成！新檔案已存至：{output_csv}")

if __name__ == "__main__":
    transform_csv()