import numpy as np
import random
from scipy.optimize import root
from Q1_1 import get_angle,f_p2
from matplotlib import pyplot as plt

# 两个三个飞机随机
# 载入数据
plane = np.array([[10, np.deg2rad(0)], [100, np.deg2rad(0)], [98, np.deg2rad(40.10)],
                  [112, np.deg2rad(80.21)], [105, np.deg2rad(119.75)], [98, np.deg2rad(159.86)],
                  [112, np.deg2rad(199.96)], [105, np.deg2rad(240.07)], [98, np.deg2rad(280.17)],
                  [112, np.deg2rad(320.28)]])

plane_hat = plane
iter_max = 5
lr = 1
d = 100
fixed = 1
t = 1

position_remember_xy = np.zeros((10,2))

launch = np.zeros(3)
start = 3 # 开始轮循的第一架飞机

for iter in range(start,start + iter_max):
    launch[0] = iter % 9 + 1
    # launch_1 += 1
    # launch_1 = launch_1 % 9 + 1
    launch[1] = (launch[0] + 3) % 9
    if launch[1] == 0:
        launch[1] = 9
    launch[2] = (launch[1] + 3) % 9
    if launch[2] == 0:
        launch[2] = 9

    # 发射信号,其余无人机得到角度
    for i in range(1,10):
        if (i == launch[0]) or (i == launch[1]) or (i == launch[2]):
            continue

        # 分三次测量
        alpha = np.zeros(3)
        # 角度0-i-launch[0]
        alpha[0] = get_angle(np.array([plane[0, :], plane[i, :], plane[int(launch[0]), :]]))
        # 角度0-i-launch[1]
        alpha[1] = get_angle(np.array([plane[0, :], plane[i, :], plane[int(launch[1]), :]]))
        # 角度0-i-launch[2]
        alpha[2] = get_angle(np.array([plane[0, :], plane[i, :], plane[int(launch[2]), :]]))

        position_measure_xy_list = np.zeros((3,2))
        for k in range(3):
            # 估算i的位置
            angle = np.zeros(4)  # angle1,angle2,beta1,beta2
            # 每次取launch_a,launch_b
            launch_a = k % 3
            launch_b = (k + 1) % 3

            # alpha
            angle[0] = alpha[launch_a]
            angle[1] = alpha[launch_b]
            # beta
            angle[2] = (launch[launch_a] - 1) * 2 / 9 * np.pi
            angle[3] = (launch[launch_b] - 1) * 2 / 9 * np.pi
            ideal_angle = (i - 1) * 2 / 9 * np.pi

            # 求相对坐标
            # 注意相对坐标是指极径用相对值表示！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
            position = root(f_p2, [1, ideal_angle], args=(angle)).x
            # 近似转化成绝对坐标
            position[0] = position[0] * d
            position_measure_xy_list[k,:] = np.array([position[0] * np.cos(position[1]), position[0] * np.sin(position[1])])

        position_measure_xy = np.mean(position_measure_xy_list,axis = 0)
        # 首次更新记忆坐标
        if not np.any(position_remember_xy[i,:]):
            position_remember_xy[i, :] = position_measure_xy

        position_esimate_xy = t * position_measure_xy + (1 - t) * position_remember_xy[i, :]

        position_now_xy = np.array([plane[i,0] * np.cos(plane[i,1]),plane[i,0] * np.sin(plane[i,1])])
        ideal_xy = np.array([d * np.cos(ideal_angle),d * np.sin(ideal_angle)])
        w = ideal_xy - position_esimate_xy
        # 位置调整
        position_new_xy = position_now_xy + lr * w

        # 更新记忆位置
        position_remember_xy[i, :] = position_measure_xy + lr * w

        # 得到角度
        if (position_new_xy[0] >= 0) and (position_new_xy[1] >= 0): # 第一象限
            a = np.arctan(position_new_xy[1]/position_new_xy[0])
        elif (position_new_xy[0] < 0) and (position_new_xy[1] >= 0): # 第二象限
            a = np.arctan(position_new_xy[1]/position_new_xy[0]) + np.pi
        elif (position_new_xy[0] < 0) and (position_new_xy[1] < 0): # 第三象限
            a = np.arctan(position_new_xy[1]/position_new_xy[0]) + np.pi
        else: # 第四象限
            a = np.arctan(position_new_xy[1]/position_new_xy[0]) + 2 * np.pi
        plane_hat[i,:] = np.array([np.sqrt(position_new_xy[0]**2 + position_new_xy[1]**2),a])

print('/******************************************************/')
print('plane_hat')
'''
for i in range(10):
    plane_hat[i,1] = np.rad2deg(plane_hat[i,1])
'''
print(plane_hat)


ax1 = plt.subplot(121, projection='polar')  #极坐标轴
# ax1.scatter(plane[:,1],plane[:,0],color='r')
ax1.scatter(plane_hat[:,1],plane_hat[:,0],color='b')


plt.show()

print(360-359.93761995)
pro_max_min= np.max(plane_hat[1:,0]) - np.min(plane_hat[1:,0])
pro_mean = np.mean(plane_hat[1:,0])
print('mean:',pro_mean)
print('max_min:',pro_max_min)
print('pho_wucha:',pro_max_min / pro_mean)

delta_theta = np.zeros(9)
for i in range(9):
    next = i
    if next == 0:
        next =9

    delta_theta[i] = plane_hat[i+1,1] - plane_hat[next,1]

    if delta_theta[i] < 0:
        delta_theta[i] = 360 + delta_theta[i]

print('delta_theta',delta_theta)
theta_max_min= np.max(delta_theta) - np.min(delta_theta)
theta_mean = np.mean(delta_theta)
print('mean:',theta_mean)
print('max_min:',theta_max_min)
print('pho_wucha:',theta_max_min / theta_mean)


