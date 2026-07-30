import cv2
import datetime
import time

# 替换为你前视摄像头的实际 ID（比如 1）
FRONT_CAM_ID = 1 

cap = cv2.VideoCapture(FRONT_CAM_ID, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

filename = f"front_camera_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(filename, fourcc, 30.0, (640, 480))

print(f"🎥 正在后台录制前视摄像头...")
print(f"📹 视频文件将保存为: {filename}")
print("⏹️  录制完成后，请在此终端按下 [Ctrl + C] 停止并保存视频！\n")

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("⚠️ 无法获取摄像头画面，请检查连接。")
            break
        out.write(frame)
        time.sleep(0.01)  # 降低 CPU 占用

except KeyboardInterrupt:
    print("\n✅ 已接收停止指令，正在保存视频...")

finally:
    cap.release()
    out.release()
    print(f"🎉 视频保存成功！文件名: {filename}")