% ------------------------------------------------------------------------------
% Function : plot pose
% Project  : IJRR MAV Datasets
% Author   : www.asl.ethz.ch
% Version  : V01  28AUG2015 Initial version.
% Comment  :
% Status   : under review
% ------------------------------------------------------------------------------

function plotPose(t_B_2_W, q_B_2_W, caption, scale)

I = eye(3);

C_WB = quat2rotm(q_B_2_W);
V = C_WB * I * scale;

plot3([0 V(1,1)] + t_B_2_W(1),[0 V(2,1)] + t_B_2_W(2),[0 V(3,1)] + t_B_2_W(3),'r','LineWidth',2);  % x.
hold on;
plot3([0 V(1,2)] + t_B_2_W(1),[0 V(2,2)] + t_B_2_W(2),[0 V(3,2)] + t_B_2_W(3),'g','LineWidth',2);  % y.
plot3([0 V(1,3)] + t_B_2_W(1),[0 V(2,3)] + t_B_2_W(2),[0 V(3,3)] + t_B_2_W(3),'b','LineWidth',2);  % z.
text(t_B_2_W(1), t_B_2_W(2), t_B_2_W(3), caption,'FontSize',6, 'BackgroundColor',[.7 .9 .7]);
xlabel 'x';
ylabel 'y';
zlabel 'z';

end
