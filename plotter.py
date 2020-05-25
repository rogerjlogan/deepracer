import math
import matplotlib.pyplot as plt
import matplotlib
from reinvent2018 import waypoints, targets_refs
from collections import namedtuple

# If True (for debugging), will show avg, wtd_avg, and endpoint angles from point before first point (aka car)
# If False, will only show angle type specified in targets_refs for that index
SHOW_ALL_ANGLES = False
HIDE_ANGLES = False  # NOTE: If True, this will override SHOW_ALL_ANGLES  !!!!
matplotlib.use('TkAgg')  # Prevents PyCharm from embedding image in IDE

Plots = namedtuple('Plots', 'nfp, last_point_line, avg_angle_line, wtd_avg_angle_line, angle_type, num_points')

plots = []
all_xs, all_ys = zip(*waypoints)


def calc_distance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist


def generate_targets(idx, angle_type, num_points):

    # USED FOR SCRIPT ONLY: using previous point to simulate position of car
    prev_idx = idx-1 if idx > 0 else len(waypoints)-1
    curr_x, curr_y = all_xs[prev_idx], all_ys[prev_idx]

    target_angles_, target_points_ = [], []

    nfp = waypoints[idx:idx + num_points]
    len_nfp = len(nfp)
    if len_nfp < num_points:
        # lap restarting, so wrap around to get next few points
        nfp += waypoints[:num_points - len_nfp]
    # get x's and y's for next few points
    nfp_xs, nfp_ys = zip(*nfp)

    last_point_line, avg_angle_line, wtd_avg_angle_line = None, None, None
    angles = []
    for x, y in nfp[2:]:
        # using 360 degrees (no negative angles), so we can average
        # (can't average pos & neg angles and get meaningful results)
        r = math.atan2(y - curr_y, x - curr_x)
        angles.append((r if r > 0 else (2*math.pi + r)) * 360 / (2*math.pi))

    length = calc_distance(curr_x, curr_y, nfp_xs[-1], nfp_ys[-1])

    def get_line_coord(heading_):
        if heading_ > 180:
            heading_ -= 360
        endy = curr_y + length * math.sin(math.radians(heading_))
        endx = curr_x + length * math.cos(math.radians(heading_))
        return [curr_x, endx], [curr_y, endy]

    if SHOW_ALL_ANGLES or angle_type == 'end':
        last_point_line = ([curr_x, nfp_xs[-1]], [curr_y, nfp_ys[-1]])
        if angle_type == 'end':
            target_angles_.append(math.degrees(math.atan2(nfp_ys[-1] - curr_y, nfp_xs[-1] - curr_x)))
            target_points_.append((nfp_xs[-1], nfp_ys[-1]))

    if SHOW_ALL_ANGLES or angle_type == 'avg':
        # average of points
        avg_best_heading = sum(angles)/len(angles)
        avg_angle_line = get_line_coord(avg_best_heading)
        if angle_type == 'avg':
            target_angles_.append(avg_best_heading)
            target_points_.append((avg_angle_line[0][1], avg_angle_line[1][1]))

    if SHOW_ALL_ANGLES or angle_type == 'wtd_avg':
        # weighted average of points (using square of indices)
        sqrs = [float(n**2) for n, _ in enumerate(angles)]
        weights = [n/sum(sqrs) for n in sqrs]
        wtd_avg_best_heading = sum([a*w for a, w in zip(angles, weights)])
        wtd_avg_angle_line = get_line_coord(wtd_avg_best_heading)
        if angle_type == 'wtd_avg':
            target_angles_.append(wtd_avg_best_heading)
            target_points_.append((wtd_avg_angle_line[0][1], wtd_avg_angle_line[1][1]))

    # USED ONLY FOR RENDERING
    plots.append(Plots(nfp=nfp,
                       last_point_line=last_point_line,
                       avg_angle_line=avg_angle_line,
                       wtd_avg_angle_line=wtd_avg_angle_line,
                       angle_type=angle_type,
                       num_points=num_points))

    return target_angles_, target_points_


target_angles, target_points = [], []
for i, _ in enumerate(waypoints):
    targets = generate_targets(i, *targets_refs[i])
    target_angles += targets[0]
    target_points += targets[1]
print('target_angles =', target_angles)
print('target_points =', target_points)
assert len(target_angles) == len(waypoints), \
    f'Mismatch size between waypoints({len(waypoints)}) and target_angles({len(target_angles)})'
assert len(target_points) == len(waypoints), \
    f'Mismatch size between waypoints({len(waypoints)}) and target_points({len(target_points)})'


def draw_lines(idx):
    # --------------------------------------------------------------------------------
    # HEAT MAPS FOR REWARD AND SPEED .. RUN SEPARATELY AND COMMENT OUT OTHER PLOTS
    # from data import plot_pts
    # d_xs, d_ys, d_speeds, d_rewards = zip(*plot_pts)
    # plt.text(2.5, 3.0, 'REWARDS', fontsize=16)
    # # plt.text(2.5, 3.0, 'SPEEDS', fontsize=16)
    # plt.text(2.2, 2.8, '<--- Smallest to Biggest -->', fontsize=16)
    # plt.scatter([2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4],
    #             [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5], s=24,
    #             c=range(0, 10), cmap='CMRmap_r')
    # # plt.scatter([2.9, 3.0, 3.1],
    # #             [2.5, 2.5, 2.5], s=24,
    # #             c=range(0, 3), cmap='YlOrRd')
    # plt.scatter(d_xs, d_ys, s=1, c=d_rewards, cmap='CMRmap_r')
    # # plt.scatter(d_xs, d_ys, s=1, c=d_speeds, cmap='YlOrRd')
    # --------------------------------------------------------------------------------
    plt.plot(all_xs, all_ys, 'bo')

    nfp_xs, nfp_ys = zip(*plots[idx].nfp)
    # This is closest_waypoint[1]
    plt.plot(nfp_xs[0], nfp_ys[0], 'k*', markersize=12)

    # simulated car x, y is closest_waypoint[0]
    # USED FOR SCRIPT ONLY: using previous point to simulate position of car
    prev_idx = idx-1 if idx > 0 else len(waypoints)-1
    curr_x, curr_y = all_xs[prev_idx], all_ys[prev_idx]

    plt.plot(nfp_xs[1:], nfp_ys[1:], 'ro')
    plt.autoscale(False)
    if not HIDE_ANGLES:
        if plots[idx].last_point_line is not None:
            end_x, end_y = plots[idx].last_point_line
            plt.plot([end_x[0], end_x[1]], [end_y[0], end_y[1]], 'c--', linewidth=2, label="Endpoint")
        if plots[idx].avg_angle_line is not None:
            avg_x, avg_y = plots[idx].avg_angle_line
            plt.plot([avg_x[0], avg_x[1]], [avg_y[0], avg_y[1]], 'g--', linewidth=2, label="Avg")
        if plots[idx].wtd_avg_angle_line is not None:
            wtd_avg_x, wtd_avg_y = plots[idx].wtd_avg_angle_line
            plt.plot([wtd_avg_x[0], wtd_avg_x[1]], [wtd_avg_y[0], wtd_avg_y[1]], 'm--', linewidth=2, label="WtdAvg")

    # plot car symbol
    plt.plot(curr_x, curr_y, 'rs', markersize=12)

    if not HIDE_ANGLES:
        plt.legend(loc="center")
    plt.text(1.4, 3.0, f'Ideal Angle:{target_angles[idx]:4f}', fontsize=24)
    plt.text(1.4, 2.8, f'waypoint(black star):{idx}', fontsize=24)
    plt.text(1.4, 2.6, f'sim car(red square):{idx}', fontsize=24)
    plt.text(1.8, 2.0, f'Angle Type/# of Points={plots[idx].angle_type}/{plots[idx].num_points}', fontsize=24)
    plt.text(1.8, 1.8, 'Note: Using point before waypoint to simulate position of car.', fontsize=16)


curr_pos = 0


def key_event(e):
    global curr_pos

    if e.key == "right":
        curr_pos += 1
    elif e.key == "left":
        curr_pos -= 1
    else:
        return
    curr_pos %= len(plots)

    ax.cla()
    plt.imshow(plt.imread('reinvent_track.png'), extent=[0, 8, 0, 5.2])
    draw_lines(curr_pos)
    fig.canvas.draw()


fig = plt.figure(num=None, figsize=(20, 15), dpi=80, facecolor='w', edgecolor='k')
plt.imshow(plt.imread('reinvent_track.png'), extent=[0, 8, 0, 5.2])
draw_lines(0)
fig.canvas.mpl_connect('key_press_event', key_event)
ax = fig.add_subplot(111)
plt.show()
