close all
clear all


bag_path = './wood_wall/'
bag_name = 'wood_wall'

bag = rosbag([bag_path bag_name '.bag'])

bagselect = select(bag, 'Topic', '/tf')

clear bag

st_idx = 1;
batch_size = 100;
pose_arr = [];

while st_idx < bagselect.NumMessages
  
  st_idx
  msgs = readMessages(bagselect, ...
    st_idx : min(st_idx+batch_size, bagselect.NumMessages));
  %   size(msgs)
  
  for i=1:size(msgs, 1)
    for j=1:size(msgs{i}.Transforms, 1)
      %       if strcmp(string(msgs{i}.Transforms(j).ChildFrameId), 'stereo_camera_optical_frame')
      if strcmp(string(msgs{i}.Transforms(j).ChildFrameId), 'base_footprint')
        pose_base = [
          msgs{i}.Transforms(j).Header.Stamp.seconds;
          msgs{i}.Transforms(j).Transform.Translation.X;
          msgs{i}.Transforms(j).Transform.Translation.Y;
          msgs{i}.Transforms(j).Transform.Translation.Z;
          msgs{i}.Transforms(j).Transform.Rotation.X;
          msgs{i}.Transforms(j).Transform.Rotation.Y;
          msgs{i}.Transforms(j).Transform.Rotation.Z;
          msgs{i}.Transforms(j).Transform.Rotation.W
          ];
        %
        % convert from base to stereo frame
        %         pose_base
        %
        pose_arr = [pose_arr; pose_base'];
      end
    end
  end
  
  st_idx = st_idx + batch_size;
  
end

figure;plot(pose_arr(:,2), pose_arr(:,3))

% save to text
fileID = fopen([bag_path bag_name '_tum.txt'], 'w');

for i=1:size(pose_arr, 1)
  %
  fprintf(fileID, '%.06f', pose_arr(i, 1));
  for j=2:size(pose_arr, 2)
    fprintf(fileID, ' %.07f', pose_arr(i, j));
  end
  fprintf(fileID, '\n');
end

fclose(fileID);
