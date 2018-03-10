export DATA_PATH=/mnt/DATA/Datasets/EuRoC_dataset/BagFiles

export BLUR_POSEFIX=_blur_5
# export BLUR_POSEFIX=_blur_9


export BAG_NAME=MH_01_easy
python bag_to_puturb_images.py $DATA_PATH/$BAG_NAME.bag $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag /cam0/image_raw /cam1/image_raw

# rosbag reindex $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag
# rm $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.orig.bag

export BAG_NAME=MH_02_easy
python bag_to_puturb_images.py $DATA_PATH/$BAG_NAME.bag $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag /cam0/image_raw /cam1/image_raw

# rosbag reindex $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag
# rm $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.orig.bag

export BAG_NAME=MH_03_medium
python bag_to_puturb_images.py $DATA_PATH/$BAG_NAME.bag $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag /cam0/image_raw /cam1/image_raw

# rosbag reindex $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag
# rm $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.orig.bag

export BAG_NAME=MH_04_difficult
python bag_to_puturb_images.py $DATA_PATH/$BAG_NAME.bag $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag /cam0/image_raw /cam1/image_raw

# rosbag reindex $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag
# rm $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.orig.bag

export BAG_NAME=MH_05_difficult
python bag_to_puturb_images.py $DATA_PATH/$BAG_NAME.bag $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag /cam0/image_raw /cam1/image_raw

# rosbag reindex $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag
# rm $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.orig.bag



export BAG_NAME=V1_01_easy
python bag_to_puturb_images.py $DATA_PATH/$BAG_NAME.bag $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag /cam0/image_raw /cam1/image_raw

# rosbag reindex $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag
# rm $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.orig.bag

export BAG_NAME=V1_02_medium
python bag_to_puturb_images.py $DATA_PATH/$BAG_NAME.bag $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag /cam0/image_raw /cam1/image_raw

# rosbag reindex $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag
# rm $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.orig.bag

export BAG_NAME=V1_03_difficult
python bag_to_puturb_images.py $DATA_PATH/$BAG_NAME.bag $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag /cam0/image_raw /cam1/image_raw

# rosbag reindex $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag
# rm $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.orig.bag

export BAG_NAME=V2_01_easy
python bag_to_puturb_images.py $DATA_PATH/$BAG_NAME.bag $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag /cam0/image_raw /cam1/image_raw

# rosbag reindex $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag
# rm $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.orig.bag

export BAG_NAME=V2_02_medium
python bag_to_puturb_images.py $DATA_PATH/$BAG_NAME.bag $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag /cam0/image_raw /cam1/image_raw

# rosbag reindex $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag
# rm $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.orig.bag

export BAG_NAME=V2_03_difficult
python bag_to_puturb_images.py $DATA_PATH/$BAG_NAME.bag $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag /cam0/image_raw /cam1/image_raw

# rosbag reindex $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag
# rm $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.orig.bag