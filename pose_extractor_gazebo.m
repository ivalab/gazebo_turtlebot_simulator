close all
clear all

%% Gazebo Maze config
bag_path = {
  '/mnt/DATA/Datasets/GazeboMaze/brick_wall_0.01/';
  '/mnt/DATA/Datasets/GazeboMaze/brick_wall_0.025/';
  '/mnt/DATA/Datasets/GazeboMaze/brick_wall_0.05/';
  %
  '/mnt/DATA/Datasets/GazeboMaze/hard_wood_0.01/';
  '/mnt/DATA/Datasets/GazeboMaze/hard_wood_0.025/';
  '/mnt/DATA/Datasets/GazeboMaze/hard_wood_0.05/';
  %
  '/mnt/DATA/Datasets/GazeboMaze/wood_wall_0.01/';
  '/mnt/DATA/Datasets/GazeboMaze/wood_wall_0.025/';
  '/mnt/DATA/Datasets/GazeboMaze/wood_wall_0.05/';
  };

bag_name = {
  'brick_wall_0.01';
  'brick_wall_0.025';
  'brick_wall_0.05';
  %
  'hard_wood_0.01';
  'hard_wood_0.025';
  'hard_wood_0.05';
  %
  'wood_wall_0.01';
  'wood_wall_0.025';
  'wood_wall_0.05';
  };

pose_path = '/mnt/DATA/Datasets/GazeboMaze/Pose_GT/'

T_stereo_2_base = SE3([0.05 0.0 0.21], quat2rotm([0.5 -0.5 0.5 -0.5]));

for bn = 1:length(bag_name)
  
  bag = rosbag([bag_path{bn} bag_name{bn} '.bag'])
  bagselect = select(bag, 'Topic', '/tf')
  clear bag
  
  st_idx = 1;
  batch_size = 100;
  pose_arr = [];
  
  TimeStamp_st = 0;
  
  %% convert from base to stereo frame
  while st_idx < bagselect.NumMessages
    
    st_idx
    msgs = readMessages(bagselect, ...
      st_idx : min(st_idx+batch_size, bagselect.NumMessages));
    %   size(msgs)
    
    for i=1:size(msgs, 1)
      for j=1:size(msgs{i}.Transforms, 1)
        %       if strcmp(string(msgs{i}.Transforms(j).ChildFrameId), 'stereo_camera_optical_frame')
        if strcmp(string(msgs{i}.Transforms(j).ChildFrameId), 'base_footprint')
          if ~isempty(pose_arr) && ...
              abs( msgs{i}.Transforms(j).Header.Stamp.seconds - pose_arr(end, 1) ) < 0.0005
            continue ;
          end
          if msgs{i}.Transforms(j).Header.Stamp.seconds < TimeStamp_st
            continue ;
          end
          %
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
          T_base_2_world = SE3(pose_base(2:4), quat2rotm([pose_base(8) pose_base(5:7)']));
          T_stereo_2_world = T_base_2_world * T_stereo_2_base;
          %
          quat_stereo = rotm2quat(T_stereo_2_world.getRotation)';
          %         quat_stereo = q_C2q(T_stereo_2_world.getRotation);
          pose_stereo = [
            pose_base(1);
            T_stereo_2_world.getTranslation;
            quat_stereo(2:4);
            quat_stereo(1)
            ];
          pose_arr = [pose_arr; pose_stereo'];
          %         pose_arr = [pose_arr; pose_base'];
        end
      end
    end
    
    st_idx = st_idx + batch_size;
    
  end
  
  clear bagselect
  
  %% save to text
  fileID = fopen([pose_path bag_name{bn} '_tum.txt'], 'w');
  
  for i=1:size(pose_arr, 1)
    %
    fprintf(fileID, '%.06f', pose_arr(i, 1));
    for j=2:size(pose_arr, 2)
      fprintf(fileID, ' %.07f', pose_arr(i, j));
    end
    fprintf(fileID, '\n');
  end
  
  fclose(fileID);
  
  %% plot the x-y track
  figure(99);
  hold on
  for i=1:1000:size(pose_arr, 1)
    if i == 1
      plotPose(pose_arr(i, 2:4), [pose_arr(i, 8) pose_arr(i, 5:7)], 'stereo', 0.5)
    else
      %   plot(pose_arr(:,2), pose_arr(:,3))
      plotPose(pose_arr(i, 2:4), [pose_arr(i, 8) pose_arr(i, 5:7)], '', 0.15)
    end
  end
  axis equal
  
end
