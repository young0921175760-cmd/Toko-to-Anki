import pyautogui
import time

# 設定安全緩衝，讓你有時間切換視窗
print("程式將在 5 秒後開始...")
time.sleep(5)

# 1. 取得起始點位置（目前滑鼠停留的位置）
start_x, start_y = pyautogui.position()

# 設定參數
move_right = -500   # 往右平移的距離（像素）
move_down = 15     # 每次回到起點後，向下移動的距離（像素）
repeat_times = 30  # 重複次數

try:
    for i in range(repeat_times):
        # 計算這一輪的起點座標
        current_start_y = start_y + (i * move_down)
        
        # 先移動到該輪的起點
        pyautogui.moveTo(start_x, current_start_y)
        
        # 執行「按住並往右拖曳」
        # duration 是移動速度，設太快有些軟體會感應不到
        pyautogui.dragRel(move_right, 0, duration=0.3, button='left')
        
        time.sleep(2)  # 每次動作後停頓 2 秒
        
        print(f"完成第 {i+1}/{repeat_times} 次動作")

except KeyboardInterrupt:
    print("\n程式已手動停止。")