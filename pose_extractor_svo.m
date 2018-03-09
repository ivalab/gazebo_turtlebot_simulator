close all
clear all

%% SVO EuRoC config
bag_path = '/mnt/DATA/tmp/EuRoC/SVO2/';

bag_name = {
  'MH_01_easy';
  'MH_02_easy';
  'MH_03_medium';
  'MH_04_difficult';
  'MH_05_difficult';
  'V1_01_easy';
  'V1_02_medium';
  'V1_03_difficult';
  'V2_01_easy';
  'V2_02_medium';
  'V2_03_difficult';
  };

% pose_path = '/mnt/DATA/tmp/EuRoC/SVO2/'

T_stereo_2_base = SE3([0 0 0], eye(3));
round_num = 1;

for bn = 1 % 1:length(bag_name)
  
  for rn = 1 : round_num
    
    bag = rosbag([bag_path 'Round' num2str(rn) '/' bag_name{bn} '_svo_new.bag'])
    %     bagselect = select(bag, 'Topic', '/svo/pose_cam/0')
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
        %         for j=1%:size(msgs{i}.Pose, 1)
        %       if strcmp(string(msgs{i}.Transforms(j).ChildFrameId), 'stereo_camera_optical_frame')
        if strcmp(string(msgs{i}.Transforms.Header.FrameId), 'cam_pos')
          %           if ~isempty(pose_arr) && ...
          %               abs( msgs{i}.Transforms.Header.Stamp.seconds - pose_arr(end, 1) ) < 0.0005
          %             continue ;
          %           end
          if msgs{i}.Transforms.Header.Stamp.seconds < TimeStamp_st
            continue ;
          end
          %
          %           if ~isempty(pose_arr) && ...
          %               msgs{i}.Transforms.Header.Stamp.seconds + ...
          %               msgs{i}.Transforms.Header.Stamp.Nsec * 1e-9 < pose_arr(end, 1)
          %             continue ;
          %           end
          %
          pose_base = [
            msgs{i}.Transforms.Header.Stamp.seconds + msgs{i}.Transforms.Header.Stamp.Nsec * 1e-9;
            msgs{i}.Transforms.Transform.Translation.X;
            msgs{i}.Transforms.Transform.Translation.Y;
            msgs{i}.Transforms.Transform.Translation.Z;
            msgs{i}.Transforms.Transform.Rotation.X;
            msgs{i}.Transforms.Transform.Rotation.Y;
            msgs{i}.Transforms.Transform.Rotation.Z;
            msgs{i}.Transforms.Transform.Rotation.W
            ];
          %
          T_base_2_world = SE3(pose_base(2:4), quat2rotm([pose_base(8) pose_base(5:7)']));
          T_base_2_world = T_base_2_world.inv();
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
        %         end
      end
      
      st_idx = st_idx + batch_size;
      
    end
    
    clear bagselect
    
    %% save to text
    fileID = fopen([bag_path 'Round' num2str(rn) '/' bag_name{bn} '_AllFrameTrajectory.txt'], 'w');
    
    fprintf(fileID, '#TimeStamp Tx Ty Tz Qx Qy Qz Qw\n');
    
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
    for i=1:20:size(pose_arr, 1)
      if i == 1
        plotPose(pose_arr(i, 2:4), [pose_arr(i, 8) pose_arr(i, 5:7)], 'stereo', 0.5)
      else
        %   plot(pose_arr(:,2), pose_arr(:,3))
        plotPose(pose_arr(i, 2:4), [pose_arr(i, 8) pose_arr(i, 5:7)], '', 0.15)
      end
    end
    axis equal
    
  end
end
