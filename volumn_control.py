# 📸 用 Mediapipe 製作手勢音量控制器
# 請於本地環境執行（Colab 無法存取攝影機）

import cv2
import mediapipe as mp
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# 初始化 Mediapipe 的手部模組與繪圖工具
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)  # 偵測單手
mp_draw = mp.solutions.drawing_utils

# 初始化系統音量控制器
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_controller = cast(interface, POINTER(IAudioEndpointVolume))

# 嘗試使用 DirectShow 開啟攝影機（Windows 專用）
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("⚠️ 攝影機開啟失敗")
    exit()

while True:
    success, img = cap.read()
    if not success or img is None:
        print("⚠️ 無法讀取攝影機畫面")
        continue  # 不跳出，繼續嘗試

    print("frame shape:", img.shape)

    # 加上測試文字檢查畫面是否顯示
    cv2.putText(img, "Test", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # 轉換為 RGB，讓 Mediapipe 能處理
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # 將 landmark 座標轉換為像素位置
            h, w, _ = img.shape
            x1 = int(hand_landmarks.landmark[4].x * w)
            y1 = int(hand_landmarks.landmark[4].y * h)
            x2 = int(hand_landmarks.landmark[8].x * w)
            y2 = int(hand_landmarks.landmark[8].y * h)

            # 計算距離
            distance = math.hypot(x2 - x1, y2 - y1)

            # 映射距離到音量 0~100
            min_dist = 30
            max_dist = 200
            volume = int((distance - min_dist) / (max_dist - min_dist) * 100)
            volume = max(0, min(100, volume))

            # 控制實際系統音量
            volume_level = volume / 100.0
            volume_controller.SetMasterVolumeLevelScalar(volume_level, None)

            # 顯示音量數值
            cv2.putText(img, f'Volume: {volume}%', (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # 畫出拇指與食指的圓點與連線
            cv2.circle(img, (x1, y1), 8, (0, 255, 255), -1)
            cv2.circle(img, (x2, y2), 8, (0, 255, 255), -1)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # 顯示畫面
    print("正在顯示畫面")
    cv2.imshow("Hand Volume Control", img)

    # 按下 ESC 鍵結束（鍵碼為 27）
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 清理
cap.release()
cv2.destroyAllWindows()
