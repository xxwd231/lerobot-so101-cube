import time
from pathlib import Path
import pandas as pd
import numpy as np
from lerobot.robots.so_follower import SOFollower, SOFollowerConfig

# ================= 1. 配置参数 =================
PORT = "COM7"
ROBOT_ID = "my_awesome_follower_arm"
CALIB_DIR = Path("D:/BaiduNetdiskDownload/calibration/so_follower")

# 数据集 parquet 文件路径
DATASET_PATH = Path("C:/Users/Administrator/.cache/huggingface/lerobot/Yeahbotros/lerobot_yeahbot_dataset_tape_20260727_215745/data/chunk-000/file-000.parquet")

FPS = 30  # 回放帧率

# ================= 2. 连接与初始化 =================
cfg = SOFollowerConfig(port=PORT)
cfg.id = ROBOT_ID
cfg.calibration_dir = CALIB_DIR
cfg.cameras = {}

robot = SOFollower(cfg)
robot.connect()

print("⚡ 正在强行开启所有电机的 Torque 扭矩使能...")
for motor in robot.bus.motors:
    robot.bus.write("Torque_Enable", motor, 1)

# ================= 3. 读取 parquet 数据集 =================
print(f"📂 正在读取数据集文件: {DATASET_PATH}")
df = pd.read_parquet(DATASET_PATH)

actions = np.array(df['action'].tolist())
motors = list(robot.bus.motors.keys())

print(f"📊 成功加载数据！共 {len(actions)} 帧，包含电机: {motors}")
print("▶️ 开始回放轨迹，按 Ctrl+C 可随时紧急终止...")

# ================= 4. 底层硬核回放 =================
interval = 1.0 / FPS
try:
    for i, frame in enumerate(actions):
        # 逐个电机写入当前帧的目标角度
        for motor_idx, motor_name in enumerate(motors):
            target_degree = float(frame[motor_idx])
            robot.bus.write("Goal_Position", motor_name, target_degree)
        
        # 控制帧率节奏
        time.sleep(interval)
        
        # 每 30 帧（1秒）打印一次进度
        if i % 30 == 0 or i == len(actions) - 1:
            print(f"⏳ 回放进度: [{i+1}/{len(actions)}] 帧 ({(i+1)/len(actions)*100:.1f}%)")

except KeyboardInterrupt:
    print("\n⚠️ 收到用户中断信号，终止回放！")
except Exception as e:
    print(f"\n❌ 回放过程中发生错误: {e}")
finally:
    print("🔌 正在安全断开与从臂的连接...")
    robot.disconnect()
    print("👋 回放结束！")