非常棒！这个完整的四阶段消融实验（Ablation Study）演进过程，逻辑极其清晰、硬核且富有说服力！它真实还原了一个具身智能工程师从“面对难题 -> 变量控制对比 -> 数据清洗 -> 算法选型 -> 最终落地”的全过程。

我已经根据你纠正的真实四阶段过程，以及 `record_front.py` 和 `test_dual_cam.py` 的具体作用，为你重新更新了这份最精准、最具含金量的 **`README.md`**：

# 🤖 SO-101 Physical Robot Deployment with ACT Strategy (LeRobot)

本项目基于 **HuggingFace LeRobot** 框架，实现了低成本 6 自由度机械臂 **SO-101** 的端到端（Vision-to-Action）实机模仿学习部署。项目重点突破了低成本机械臂在小样本训练下的“ Shortcut 快捷记忆（死记硬背）”**、**“算法范式陷阱（DP vs ACT）”**与**“动作高频抖动”难题，最终实现了桌面任意随机位置下高精度、丝滑的物块视觉跟随与稳健抓取。

## 🌟 Highlights & Key Features

-   **数据驱动工程（Data-Centric Clean）**：通过消融实验诊断并消除了遥操作早期 25 组定点数据的 Shortcut 伪特征，构建了 **纯随机位置** 的高质量视觉-动作数据集。
    
-   **算法范式消融（DP vs ACT）**：深入消融对比 Diffusion Policy (DP) 与 ACT，证实 DP 在小样本下存在高维去噪空间稀疏与时延问题，选定 **ACT (Action Chunking with Transformers)** 极大地提升了响应速度。
    
-   **抗抖动与平滑（Temporal Ensembling）**：针对低成本 STS3215 舵机的跳变，引入 Temporal Ensembling 机制，通过 EMA 算法对 100-step Action Chunking 进行轨迹平滑融合，彻底消除高频抖动。
    
-   **端侧实机闭环（End-to-End Rollout）**：基于本地 NVIDIA RTX 5060，配合双路 RGB 摄像头（Front/Wrist）实现毫秒级闭环控制响应。
    

## 📂 Project Structure

Plaintext

```
lerobot/
├── calibration/                        # 机械臂硬件标定配置文件
├── outputs/captured_images/            # 摄像头测试与捕获图像
├── test_dual_cam.py                    # 双摄像头（Front/Wrist）画面预览与设备 Index 索引校验脚本
├── record_front.py                     # 前置单摄像头（Front Cam）测试与数据录制辅助脚本
├── act_last_model.zip                  # 训练完成的 ACT 最终模型权重包
├── lerobot_yeahbot_dataset_cube.zip    # 清洗并扩充后的纯随机高精度数据集
└── README.md                           # 项目说明文档

```
## 🔬 Four-Stage Ablation Demos (消融实验效果对比)

We compared the performance at different stages to show the effectiveness of data cleaning and temporal ensembling.

| ❌ 优化前：抖动与盲抓 | ✅ 优化后：平滑高精度抓取 |
| :---: | :---: |
| <img src="E:\windows_tools\lerobot-so101-cube\media\readme\Failed_grasp.gif" width="420"/> | <img src="E:\windows_tools\lerobot-so101-cube\media\readme\smooth_grasp.gif" width="420"/> |
| *开环 100-step 漂移 & 舵机高频抖动* | *Temporal Ensembling  +  纯随机数据* |

## 🛠️ Hardware & Setup

### 1. 硬件配置

-   **机械臂**：SO-101 Follower/Leader (6 DOF, STS3215 舵机)
    
-   **视觉传感器**：
    
    -   **Front Cam**: 全局视野 RGB 摄像头 (640x480, 30FPS)
        
    -   **Wrist Cam**: 手腕末端 RGB 摄像头 (640x480, 30FPS)
        
-   **计算终端**：NVIDIA RTX 5060 / 12GB VRAM + Windows/Linux
    

### 2. 环境安装

Bash

```
# 克隆仓库并安装基础环境
git clone https://github.com/Yeahbotros/lerobot.git
cd lerobot

# 使用 uv 或 conda 创建环境并安装依赖
pip install -e .

```

## 🚀 Quick Start & Rollout

### Step 1: 硬件与摄像头检测

在运行 Rollout 部署前，可运行测试脚本确认双摄像头索引与画质正常：

Bash

```
python test_dual_cam.py

```

### Step 2: 关键配置参数微调 (`config.json`)

为消除舵机运行中的高频抖动与开环累积误差，请确保模型配置文件 `pretrained_model/config.json` 中已启用 **Temporal Ensembling**：

JSON

```
{
  "type": "act",
  "chunk_size": 100,
  "n_action_steps": 1, // 👈 核心参数：必须为1，要不最新版本会报错
  "temporal_ensemble_coeff": 0.01  // 👈 核心参数：开启时序平滑 (EMA)
}

```

### Step 3: 实机端到端部署 (PowerShell/Terminal)

运行以下命令启动机械臂闭环抓取：

PowerShell

```
lerobot-rollout `
  --strategy.type=base `
  --robot.type=so101_follower `
  --robot.port=COM9 `
  --robot.calibration_dir="D:/BaiduNetdiskDownload/calibration/so_follower" `
  --robot.id=my_awesome_follower_arm `
  --robot.cameras="{ front: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30, fourcc: 'MJPG'}, wrist: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: 'MJPG'}}" `
  --task="Pick up the cube" `
  --policy.path="E:/edge_download/act_last_model/last/pretrained_model"

```

## 📊 Performance & Four-Stage Ablation Journey (消融实验演进)

**阶段**

**数据集组成**

**核心实验与表现**

**根本原因分析 (Root Cause)**

**优化策略与决胜方案**

**阶段 1**

25 组定点数据

实机部署“盲人抓空气”

数据集单一，模型对绝对位置产生了 Shortcut 快捷死记硬背

启动随机位置数据采集

**阶段 2**

60 组 (25定点 + 35随机)

ACT vs DP 消融；依然呈现定点抓取倾向且高频发抖

神经网络倾向于“偷懒”，前 25 组定点噪声数据严重污染全局特征映射

**数据硬核清洗**：彻底剔除前 25 组定点数据，仅保留纯随机轨迹

**阶段 3**

35 组纯随机数据

**DP 失败**：空间稀疏陷局部坍缩

  

**ACT 成功**：建立真正的视觉-机械臂跟随，但偶发空抓与抖动

1) DP 在小样本下去噪空间过于稀疏；

  

2) ACT 100-step Chunk 缺乏平滑；

  

3) 35 组插值锚点不足

1) **策略选型**：锁定 ACT，放弃 DP；

  

2) **平滑控制**：配置 `temporal_ensemble_coeff: 0.01` 消除抖动

![SO-101 Pick Task Demo](E:\windows_tools\lerobot-so101-cube\media\readme\successed_grasp.gif)

**阶段 4**

65 组 (扩充纯随机数据)

抖动彻底消失，桌面任意位置高精度抓取，成功率 95%+

样本量达到物理插值天花板，空间泛化与绝对精度建立

![SO-101 Pick Task Demo](E:\windows_tools\lerobot-so101-cube\media\readme\dif_pos1.gif)

![SO-101 Pick Task Demo](E:\windows_tools\lerobot-so101-cube\media\readme\dif_pos2.gif)

**最终闭环**：实现高质量 Sim2Real 极速闭环部署

## 🤝 Acknowledgements

-   [HuggingFace LeRobot Framework](https://github.com/huggingface/lerobot)
    
-   [SO-101 Hardware Design & Calibration](https://github.com/AlexanderKoch-Koch/low_cost_robot)