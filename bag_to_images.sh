export DATA_PATH=/mnt/DATA/Datasets/GazeboMaze

export BAG_NAME=wood_wall_0.01

mkdir $DATA_PATH/$BAG_NAME
mkdir $DATA_PATH/$BAG_NAME/cam0
mkdir $DATA_PATH/$BAG_NAME/cam0/data/
mkdir $DATA_PATH/$BAG_NAME/cam1
mkdir $DATA_PATH/$BAG_NAME/cam1/data/
python bag_to_images.py $DATA_PATH/$BAG_NAME/$BAG_NAME.bag $DATA_PATH/$BAG_NAME/cam0/data/ /multisense_sl/camera/left/image_raw
python bag_to_images.py $DATA_PATH/$BAG_NAME/$BAG_NAME.bag $DATA_PATH/$BAG_NAME/cam1/data/ /multisense_sl/camera/right/image_raw


export BAG_NAME=wood_wall_0.025

mkdir $DATA_PATH/$BAG_NAME
mkdir $DATA_PATH/$BAG_NAME/cam0
mkdir $DATA_PATH/$BAG_NAME/cam0/data/
mkdir $DATA_PATH/$BAG_NAME/cam1
mkdir $DATA_PATH/$BAG_NAME/cam1/data/
python bag_to_images.py $DATA_PATH/$BAG_NAME/$BAG_NAME.bag $DATA_PATH/$BAG_NAME/cam0/data/ /multisense_sl/camera/left/image_raw
python bag_to_images.py $DATA_PATH/$BAG_NAME/$BAG_NAME.bag $DATA_PATH/$BAG_NAME/cam1/data/ /multisense_sl/camera/right/image_raw


export BAG_NAME=wood_wall_0.05

mkdir $DATA_PATH/$BAG_NAME
mkdir $DATA_PATH/$BAG_NAME/cam0
mkdir $DATA_PATH/$BAG_NAME/cam0/data/
mkdir $DATA_PATH/$BAG_NAME/cam1
mkdir $DATA_PATH/$BAG_NAME/cam1/data/
python bag_to_images.py $DATA_PATH/$BAG_NAME/$BAG_NAME.bag $DATA_PATH/$BAG_NAME/cam0/data/ /multisense_sl/camera/left/image_raw
python bag_to_images.py $DATA_PATH/$BAG_NAME/$BAG_NAME.bag $DATA_PATH/$BAG_NAME/cam1/data/ /multisense_sl/camera/right/image_raw
