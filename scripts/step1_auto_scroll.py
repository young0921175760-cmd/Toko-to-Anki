import pyautogui
import time

# 初始等待，讓你有時間切換到 Toko 視窗
print("程式將在 5 秒後開始，請切換至 Toko 軟體...")
time.sleep(5)

try:
    while True:
        # 1. 停頓三秒
        print("等待 3 秒中...")
        time.sleep(5)
        
        # 2. 按下 18 下 Tab 鍵
        # interval=0.1 代表每按一下停 0.1 秒，這樣電腦比較跟得上
        print("正在按 18 下 Tab...")
        pyautogui.press('tab', presses=18, interval=0.001)
        
        # (選用) 如果你需要按完 Tab 之後按一下 Enter 來選取
        # pyautogui.press('enter')
        
        print("一次循環完成！")

except KeyboardInterrupt:
    print("\n程式已停止。")