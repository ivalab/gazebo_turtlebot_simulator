export DATA_PATH=/mnt/DATA/Datasets/EuRoC_dataset/BagFiles

export BAG_NAME=V1_03_difficult
export BLUR_POSEFIX=_blur_9

# mkdir $DATA_PATH/$BAG_NAME
# mkdir $DATA_PATH/$BAG_NAME/cam0
# mkdir $DATA_PATH/$BAG_NAME/cam0/data/
# mkdir $DATA_PATH/$BAG_NAME/cam1
# mkdir $DATA_PATH/$BAG_NAME/cam1/data/
python bag_to_puturb_images.py $DATA_PATH/$BAG_NAME.bag $DATA_PATH/$BAG_NAME$BLUR_POSEFIX.bag /cam0/image_raw /cam1/image_raw
# python bag_to_images.py $DATA_PATH/$BAG_NAME/$BAG_NAME.bag $DATA_PATH/$BAG_NAME/cam1/data/ /multisense_sl/camera/right/image_raw


# export BAG_NAME=wood_wall_0.025

# mkdir $DATA_PATH/$BAG_NAME
# mkdir $DATA_PATH/$BAG_NAME/cam0
# mkdir $DATA_PATH/$BAG_NAME/cam0/data/
# mkdir $DATA_PATH/$BAG_NAME/cam1
# mkdir $DATA_PATH/$BAG_NAME/cam1/data/
# python bag_to_images.py $DATA_PATH/$BAG_NAME/$BAG_NAME.bag $DATA_PATH/$BAG_NAME/cam0/data/ /multisense_sl/camera/left/image_raw
# python bag_to_images.py $DATA_PATH/$BAG_NAME/$BAG_NAME.bag $DATA_PATH/$BAG_NAME/cam1/data/ /multisense_sl/camera/right/image_raw


# export BAG_NAME=wood_wall_0.05

# mkdir $DATA_PATH/$BAG_NAME
# mkdir $DATA_PATH/$BAG_NAME/cam0
# mkdir $DATA_PATH/$BAG_NAME/cam0/data/
# mkdir $DATA_PATH/$BAG_NAME/cam1
# mkdir $DATA_PATH/$BAG_NAME/cam1/data/
# python bag_to_images.py $DATA_PATH/$BAG_NAME/$BAG_NAME.bag $DATA_PATH/$BAG_NAME/cam0/data/ /multisense_sl/camera/left/image_raw
# python bag_to_images.py $DATA_PATH/$BAG_NAME/$BAG_NAME.bag $DATA_PATH/$BAG_NAME/cam1/data/ /multisense_sl/camera/right/image_raw
