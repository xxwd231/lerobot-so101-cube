#采集代码

(lerobot) PS E:\windows_tools\lerobot> lerobot-record `
  --robot.type=so101_follower `
  --robot.port=COM9 `
  --robot.calibration_dir="D:\BaiduNetdiskDownload\calibration\so_follower" `
  --robot.id=my_awesome_follower_arm `
  --robot.cameras="{ front: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30, fourcc: 'MJPG'}, wrist: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: 'MJPG'}}" `
  --teleop.type=so101_leader `
  --teleop.port=COM8 `
  --teleop.calibration_dir="D:\BaiduNetdiskDownload\calibration\so_leader" `
  --teleop.id=my_awesome_leader_arm `
  --dataset.fps=30 `
  --display_data=true `
  --dataset.repo_id=Yeahbotros/lerobot_yeahbot_dataset_cube `
  --dataset.num_episodes=15 `
  --dataset.single_task="Pick up the cube" `
  --dataset.push_to_hub=false `
  --dataset.episode_time_s=15 `
  --dataset.reset_time_s=6 



#部署代码
lerobot-rollout `
  --strategy.type=base `
  --robot.type=so101_follower `
  --robot.port=COM9 `
  --robot.calibration_dir="D:\BaiduNetdiskDownload\calibration\so_follower" `
  --robot.id=my_awesome_follower_arm `
  --robot.cameras="{ front: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30, fourcc: 'MJPG'}, wrist: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: 'MJPG'}}" `
  --task="Pick up the cube" `
  --policy.path="E:\edge_download\cube_model_v2_fast\data\output_lerobot_train\cube_finetune\checkpoints\last\pretrained_model"

#微调补录代码
lerobot-record `
  --robot.type=so101_follower `
  --robot.port=COM9 `
  --robot.calibration_dir="D:\BaiduNetdiskDownload\calibration\so_follower" `
  --robot.id=my_awesome_follower_arm `
  --robot.cameras="{ front: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30, fourcc: 'MJPG'}, wrist: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30, fourcc: 'MJPG'}}" `
  --teleop.type=so101_leader `
  --teleop.port=COM8 `
  --teleop.calibration_dir="D:\BaiduNetdiskDownload\calibration\so_leader" `
  --teleop.id=my_awesome_leader_arm `
  --dataset.fps=30 `
  --display_data=true `
  --dataset.repo_id=Yeahbotros/lerobot_yeahbot_dataset_cube `
  --dataset.root="C:\Users\Administrator\.cache\huggingface\lerobot\Yeahbotros\lerobot_yeahbot_dataset_cube" `
  --dataset.num_episodes=25 `
  --dataset.single_task="Pick up the cube" `
  --dataset.push_to_hub=false `
  --dataset.episode_time_s=15 `
  --dataset.reset_time_s=6 `
  --resume=true

#微调训练代码
lerobot-train \
  --dataset.repo_id=Yeahbotros/lerobot_yeahbot_dataset_cube \
  --dataset.root=/data/lerobot_yeahbot_dataset_cube \
  --dataset.streaming=false \
  --policy.path=/data/last/pretrained_model \
  --output_dir=/data/output_lerobot_train/cube_finetune \
  --job_name=cube_finetune_job \
  --policy.device=cuda \
  --wandb.enable=false \
  --policy.push_to_hub=false \
  --steps=5000 \
  --batch_size=64 \
  --save_freq=1000