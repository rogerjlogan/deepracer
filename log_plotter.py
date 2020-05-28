#!/usr/bin/env python3
"""

"""
from collections import namedtuple
import math
import matplotlib.pyplot as plt
import matplotlib

from data.reinvent2018 import track, waypoints, targets_refs
from simlogparser import SimLogParser
from data.misc import cmap
from util.math import calc_distance, convert_degree_angle, average, weighted_avg

matplotlib.use('TkAgg')  # Prevents PyCharm from embedding image in IDE

Plots = namedtuple('Plots', 'nfp, idx, last_point_line, avg_angle_line, wtd_avg_angle_line, angle_type, num_points')

all_xs, all_ys = zip(*waypoints)


class LogPlotter:
    def __init__(self, log, heatmap=''):
        """
        :param log: [string] Name of log file to pull data from.  Will use actual position with car for given episode.
        :param heatmap: [string] Options: '', 'Reward', 'Speed'
                        If Null, will show angles interactive plot,
                        but if not Null, the it will override self.*_angles below.
        """
        self.log = log
        self.heatmap = heatmap

        self.plots = []
        self.curr_pos = 0

        self.plot_pts = SimLogParser(log)
        self._get_target_points()
        self.plot()

    @staticmethod
    def _get_line_coord(heading, length, curr_x, curr_y):
        heading = convert_degree_angle(heading)
        endy = curr_y + length * math.sin(math.radians(heading))
        endx = curr_x + length * math.cos(math.radians(heading))
        return [curr_x, endx], [curr_y, endy]

    def _get_plot_data(self, idx, angle_type, num_points, curr_x, curr_y):
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
            angle = convert_degree_angle(math.degrees(math.atan2(y - curr_y, x - curr_x)), pos_neg=False)
            angles.append(angle)

        length = calc_distance(curr_x, curr_y, nfp_xs[-1], nfp_ys[-1])

        if angle_type == 'end':
            last_point_line = ([curr_x, nfp_xs[-1]], [curr_y, nfp_ys[-1]])

        elif angle_type == 'avg':
            avg_best_heading = average(angles)
            avg_angle_line = self._get_line_coord(avg_best_heading, length, curr_x, curr_y)

        elif angle_type == 'wtd_avg':
            wtd_avg_best_heading = weighted_avg(angles)
            wtd_avg_angle_line = self._get_line_coord(wtd_avg_best_heading, length, curr_x, curr_y)
        else:
            raise ValueError(f"Unknown angle_type: {angle_type}")

        self.plots.append(Plots(nfp=nfp,
                                idx=idx,
                                last_point_line=last_point_line,
                                avg_angle_line=avg_angle_line,
                                wtd_avg_angle_line=wtd_avg_angle_line,
                                angle_type=angle_type,
                                num_points=num_points))

    def _get_target_points(self):
        for x, y, idx, _, _ in self.plot_pts:
            self._get_plot_data(idx, *targets_refs[idx], x, y)

    def _draw_heatmap(self, idx):
        d_xs, d_ys, _, d_speeds, d_rewards = zip(*self.plot_pts)
        plt.text(2.5, 3.2, f'cmap: {cmap[idx]}', fontsize=16)
        plt.text(2.5, 3.0, f'{self.heatmap} HEATMAP', fontsize=16)
        plt.text(2.2, 2.8, '<--- Smallest to Biggest -->', fontsize=16)
        if self.heatmap.lower() == 'reward':
            plt.scatter([2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4],
                        [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5], s=24, c=range(0, 10), cmap=cmap[idx])
            plt.scatter(d_xs, d_ys, s=1, c=d_rewards, cmap=cmap[idx])
        elif self.heatmap.lower() == 'speed':
            plt.scatter([2.9, 3.0, 3.1],
                        [2.5, 2.5, 2.5], s=24, c=range(0, 3), cmap=cmap[idx])
            plt.scatter(d_xs, d_ys, s=1, c=d_speeds, cmap=cmap[idx])
        else:
            raise ValueError(
                f"Invalid constant value. self.heatmap='{self.heatmap}'. Value must be '', 'Reward', or 'Speed'")
        plt.plot(all_xs, all_ys, 'bo')

    def _draw_lines(self, idx, nfp, curr_x, curr_y):
        # plt.plot(all_xs, all_ys, 'bo')
        nfp_xs, nfp_ys = zip(*nfp)
        # This is closest_waypoint[1]
        plt.plot(nfp_xs[0], nfp_ys[0], 'k*', markersize=12)

        plt.plot(nfp_xs[1:], nfp_ys[1:], 'ro')
        plt.autoscale(False)
        if self.plots[idx].last_point_line is not None:
            end_x, end_y = self.plots[idx].last_point_line
            plt.plot([end_x[0], end_x[1]], [end_y[0], end_y[1]], 'c--', linewidth=2, label="Endpoint")
        if self.plots[idx].avg_angle_line is not None:
            avg_x, avg_y = self.plots[idx].avg_angle_line
            plt.plot([avg_x[0], avg_x[1]], [avg_y[0], avg_y[1]], 'g--', linewidth=2, label="Avg")
        if self.plots[idx].wtd_avg_angle_line is not None:
            wtd_avg_x, wtd_avg_y = self.plots[idx].wtd_avg_angle_line
            plt.plot([wtd_avg_x[0], wtd_avg_x[1]], [wtd_avg_y[0], wtd_avg_y[1]], 'm--', linewidth=2, label="WtdAvg")
        plt.plot(curr_x, curr_y, 'rs', markersize=12)

        plt.legend(loc="center")
        plt.text(1.4, 2.8, f'waypoint(black star):{idx}', fontsize=24)
        plt.text(1.4, 2.6, f'sim car(red square):{idx}', fontsize=24)
        plt.text(1.8, 2.0, f'Angle Type/# of Points={self.plots[idx].angle_type}/'
                           f'{self.plots[idx].num_points}', fontsize=24)
        plt.text(1.8, 1.8, 'Note: Using point before waypoint to simulate position of car.', fontsize=16)

    def key_event(self, e, items, ax, fig):
        if e.key == "right":
            self.curr_pos += 1
        elif e.key == "left":
            self.curr_pos -= 1
        else:
            return
        self.curr_pos %= len(items)

        ax.cla()
        plt.imshow(plt.imread(track), extent=[0, 8, 0, 5.2])
        if self.heatmap:
            self._draw_heatmap(self.curr_pos)
        else:
            self._draw_lines(self.curr_pos)
        fig.canvas.draw()

    def plot(self):
        fig = plt.figure(num=None, figsize=(20, 15), dpi=80, facecolor='w', edgecolor='k')
        plt.imshow(plt.imread(track), extent=[0, 8, 0, 5.2])
        ax = fig.add_subplot(111)

        if self.heatmap:
            self._draw_heatmap(0)
            fig.canvas.mpl_connect('key_press_event', lambda event: self.key_event(event, cmap, ax, fig))
        else:
            self._draw_lines(0)
            fig.canvas.mpl_connect('key_press_event', lambda event: self.key_event(event, cmap, ax, fig))
        plt.show()


if __name__ == '__main__':
    # LogPlotter(log='sim-27may.log')
    LogPlotter(heatmap='Reward', log='roger-sim-24may.log')
    # LogPlotter(heatmap='Speed', log='roger-sim-24may.log')
