#!/usr/bin/env python3
"""
Plot either a heatmap (reward or speed) or best headings from actual points in aws log file.
Examples:
    python log_plotter.py -h  # show help menu
    python log_plotter.py 'awslog-sim.log' -groupsize -1  # show one whole episode per click
    python log_plotter.py 'roger-sim-24may.log' -groupsize 10
    python log_plotter.py 'roger-sim-24may.log' -heatmap reward
    python log_plotter.py 'roger-sim-24may.log' -heatmap speed
"""
from argparse import ArgumentParser, ArgumentTypeError, RawTextHelpFormatter
from collections import namedtuple
import matplotlib.pyplot as plt

from data.reinvent2018 import track, waypoints
from simlogparser import SimLogParser
from data.colors import cmap
from util.misc import valid_aws_log_file

# this file is generated by another script
from data.reinvent2018_targets import target_points


Plots = namedtuple('Plots', 'nfp, idx, last_point_line, avg_angle_line, wtd_avg_angle_line, angle_type, num_points')

all_xs, all_ys = zip(*waypoints)


class LogPlotter:
    def __init__(self, log, heatmap='', groupsize=-1):
        """
        :param log: [string] Name of log file to pull data from.  Will use actual position with car for given episode.
        :param heatmap: [string] Options: '', 'Reward', 'Speed'
                        If Null, will show angles interactive plot,
                        but if not Null, the it will override self.*_angles below.
        :param groupsize: [int] Number of points per click when plotting lines.  Ignored if heatmap != ''
                          If -1, this will display all points from one episode at a time (per click).
        """
        self.log = log
        self.heatmap = heatmap
        self.groupsize = groupsize
        self.curr_episode = None  # only used if groupsize is -1

        self.plots = []
        self.curr_pos = 0
        self.plot_dir_right = True

        self.parsed_log = SimLogParser(log, verbose=True)
        self.plot_pts = self.parsed_log.plot_pts
        self.good_episode_list = tuple(self.parsed_log.good_episode_list)
        self.episode_data = self.parsed_log.episode_data
        self.plot()

    def _draw_lines(self, idx):
        plt.autoscale(False)
        plt.plot(all_xs, all_ys, 'bo')
        # WARNING: This line must match what is PACKED UPSTREAM in SimLogParser (simlogparser.py)
        ep_start, stp_start, wpi_start = None, None, None
        if self.groupsize == -1:
            # get one whole episode
            episode_key = self.good_episode_list[idx]
            assert isinstance(episode_key, int), f"Bad value for episode:{episode_key}"
            plot_pts = ((episode, step, x, y, nearest_waypoint_idx, speed)
                        for episode, step, x, y, nearest_waypoint_idx, speed, _
                        in self.plot_pts if episode == episode_key)
            plt.text(2.5, 1.3, self.episode_data[episode_key], fontsize=12)
        else:
            plot_pts = ((episode, step, x, y, nearest_waypoint_idx, speed)
                        for (episode, step, x, y, nearest_waypoint_idx, speed, _)
                        in self.plot_pts[idx:idx + self.groupsize])
            if self.plot_dir_right:
                self.curr_pos += self.groupsize
            else:
                self.curr_pos -= self.groupsize
        for episode, step, x, y, nearest_waypoint_idx, speed in plot_pts:
            x2, y2 = target_points[nearest_waypoint_idx]
            plt.plot((x, x2), (y, y2), 'c--', linewidth=1)
            if speed > 3.9:
                plt.plot(x, y, 'gs', markersize=12)
            elif speed > 2:
                plt.plot(x, y, 'ys', markersize=12)
            else:
                plt.plot(x, y, 'rs', markersize=12)
            # This is closest_waypoint[1]
            nwp_x, nwp_y = waypoints[nearest_waypoint_idx]
            plt.plot(nwp_x, nwp_y, 'k*', markersize=12)
            if ep_start is None:
                plt.text(2.5, 1.3, self.episode_data[episode], fontsize=12)
                ep_start = episode
                stp_start = step
                wpi_start = nearest_waypoint_idx
        plt.text(1.5, 2.6, f'Nearest Waypoint(black star)', fontsize=12)
        plt.text(1.5, 2.5, f'Log position of Car (square)', fontsize=12)
        plt.text(1.5, 2.4, f'square: green=fast (> 3.9 m/s), yellow=medium, red=slow (<= 2 m/s)', fontsize=12)
        explain = '(displaying entire episode)' if self.groupsize == -1 else ''
        plt.text(1.5, 2.3, f'Groupsize: {self.groupsize} {explain}', fontsize=12)

        plt.text(1.5, 2.2, f'First point episode: {ep_start}', fontsize=12)
        plt.text(1.5, 2.1, f'First point step: {stp_start}', fontsize=12)
        plt.text(1.5, 2.0, f'First point nearest waypoint index: {wpi_start}', fontsize=12)

        plt.text(2.0, 1.6, 'Click right/left arrow to cycle through next point(s).', fontsize=12)

    def _draw_heatmap(self, idx):
        # WARNING: This line must match what is PACKED UPSTREAM in SimLogParser (simlogparser.py)
        _, _, xs, ys, _, d_speeds, d_rewards = zip(*self.plot_pts)
        plt.text(2.5, 3.2, f'cmap: {cmap[idx]}', fontsize=16)
        plt.text(2.5, 3.0, f'{self.heatmap} HEATMAP', fontsize=16)
        plt.text(2.2, 2.8, '<--- Smallest to Biggest -->', fontsize=16)
        if self.heatmap.lower() == 'reward':
            plt.scatter([2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4],
                        [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5], s=24, c=range(0, 10), cmap=cmap[idx])
            plt.scatter(xs, ys, s=1, c=d_rewards, cmap=cmap[idx])
        elif self.heatmap.lower() == 'speed':
            plt.scatter([2.9, 3.0, 3.1],
                        [2.5, 2.5, 2.5], s=24, c=range(0, 3), cmap=cmap[idx])
            plt.scatter(xs, ys, s=1, c=d_speeds, cmap=cmap[idx])
        else:
            raise ValueError(
                f"Invalid constant value. self.heatmap='{self.heatmap}'. Value must be '', 'Reward', or 'Speed'")
        plt.text(2.0, 2.0, 'Click right/left arrow to cycle through color maps.', fontsize=12)
        plt.plot(all_xs, all_ys, 'bo')

    def key_event(self, e, items, ax, fig):
        if e.key == "right":
            self.curr_pos += 1
            self.plot_dir_right = True
        elif e.key == "left":
            self.curr_pos -= 1
            self.plot_dir_right = False
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
            fig.canvas.mpl_connect('key_press_event', lambda event: self.key_event(event, self.plot_pts, ax, fig))
        plt.show()


def valid_heatmap(heatmap):
    valid_heatmap_values = ('', 'speed', 'reward')
    if heatmap.lower() not in valid_heatmap_values:
        ArgumentTypeError(f'Invalid heatmap argument passed.  Must be one of these: {valid_heatmap_values}')
    return heatmap


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument('log', type=valid_aws_log_file,
                        help="AWS Log file containing 'SIM_TRACE_LOG' and 'Reset'")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-groupsize', type=int, default=-1,
                       help="Group size to show log points and their headings one group per click. "
                            "Ignored if heatmap != ''. If -1, this will display all points from one "
                            "episode at a time (per click).")
    group.add_argument('-heatmap', type=valid_heatmap, default='',
                       help="Valid options: '', 'Speed', 'Reward'. If '' (null) then points/headings will be plotted")
    args = parser.parse_args()
    LogPlotter(log=args.log, groupsize=args.groupsize, heatmap=args.heatmap)
