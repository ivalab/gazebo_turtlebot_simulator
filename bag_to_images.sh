export BAG_NAME=wood_wall

mkdir ./$BAG_NAME
mkdir ./$BAG_NAME/cam0
mkdir ./$BAG_NAME/cam0/data/
mkdir ./$BAG_NAME/cam1
mkdir ./$BAG_NAME/cam1/data/
python bag_to_images.py ./$BAG_NAME/$BAG_NAME.bag ./$BAG_NAME/cam0/data/ /multisense_sl/camera/left/image_raw
python bag_to_images.py ./$BAG_NAME/$BAG_NAME.bag ./$BAG_NAME/cam1/data/ /multisense_sl/camera/right/image_raw