#!/usr/bin/env python3
"""
Extract/parse AWS Deepracer SIM logs
"""
import re
from collections import namedtuple
import pandas as pd
import numpy as np
from data.reinvent2018 import target_points

Row = namedtuple('logs', 'episode, step, x_coord, y_coord, heading, steering, speed, action_taken, reward, '
                         'job_completed, all_wheels_on_track, progress, closest_waypoint_index,'
                         'track_length, time, status')

numerics = ['episode', 'step', 'x_coord', 'y_coord', 'heading', 'steering', 'speed', 'action_taken', 'reward',
            'progress', 'closest_waypoint_index', 'track_length', 'time']
booleans = ['job_completed', 'all_wheels_on_track']
strings = ['status']
truth_map = {'True': True, 'False': False}

PlotPts = namedtuple('PlotPts', 'x y speed reward')


class SimLogParser:

    def __init__(self, logfile='aws.log', verbose=False):
        self.logfile = logfile
        self.verbose = verbose
        self.num_offtracks = 0
        self.good_episodes, self.lap_times, self.steps, self.plot_pts = [], [], [], []
        self.logfile = logfile
        self._parse()
        self._aggregate()
        if len(self.good_episodes):
            combined_episodes = pd.concat(self.good_episodes) if len(self.good_episodes) > 1 else self.good_episodes
            combined_episodes.to_excel(f'{self.logfile.rstrip(".log")}.xlsx', index=False)
        print(self)

    def _parse(self):
        in_episode = False
        with open(self.logfile) as f:
            data = None
            for line in f.readlines():
                if not len(line.strip()):
                    continue
                if not in_episode:
                    if re.search('Reset agent', line):
                        in_episode = True
                        data = []
                else:
                    obj = re.search(r'(?<=SIM_TRACE_LOG:)(.+)', line)
                    if obj:
                        if data is None:
                            raise TypeError(f'DataFrame not initialized: len(good_episodes)={len(self.good_episodes)}')
                        row = Row(*obj.group(0).split(','))
                        if row.status == 'off_track':
                            in_episode = False
                            self.num_offtracks += 1
                            continue
                        data.append(row)
                        if row.status == 'lap_complete':
                            in_episode = False
                            df = pd.DataFrame(data=data)
                            df[numerics] = df[numerics].apply(pd.to_numeric)
                            df.closest_waypoint_index = df.closest_waypoint_index.mod(70)
                            for b in booleans:
                                df[b] = df[b].map(truth_map)
                            df[strings] = df[strings].astype(str)
                            x2, y2 = zip(*np.array(target_points)[df.closest_waypoint_index])
                            best_heading = np.degrees(np.arctan2(y2 - df['y_coord'], x2 - df['x_coord']))
                            df['best_heading'] = best_heading
                            df['direction_diff'] = abs(((best_heading - df['heading']) + 180) % 360 - 180)
                            self.good_episodes.append(df)

    def _aggregate(self):
        for ep in self.good_episodes:
            lap_time = ep.time.iloc[-1] - ep.time.iloc[0]
            if self.verbose:
                print(f'episode: {ep.episode.iloc[0]}, steps: {ep.step.iloc[-1]}, lap_time={lap_time}')
            self.plot_pts += zip(ep.x_coord, ep.y_coord, ep.closest_waypoint_index, ep.speed, ep.reward)
            self.lap_times.append(lap_time)
            self.steps.append(ep.step.iloc[-1])

    def __str__(self):
        out = f'\nAnalyzing {len(self.good_episodes) + self.num_offtracks} episodes...\n'
        out += f'\tNumber of "lap_complete" episodes = {len(self.good_episodes)}\n'
        out += f'\tNumber of "off_track" episodes = {self.num_offtracks} ... ignoring for analysis\n'
        if len(self.lap_times):
            min_time = min(self.lap_times)
            min_time_idx = self.lap_times.index(min_time)
            max_time = max(self.lap_times)
            max_time_idx = self.lap_times.index(max_time)
            min_step = min(self.steps)
            min_step_idx = self.steps.index(min_step)
            max_step = max(self.steps)
            max_step_idx = self.steps.index(max_step)
            out += f'\tAverage Lap Time = {np.mean(self.lap_times):.2f}s (StdDev: {np.std(self.lap_times):.4f})\n'
            out += f'\tMin Lap Time(Steps) = {min_time:.2f}s({self.steps[min_time_idx]})\n'
            out += f'\tMax Lap Time(Steps)= {max_time:.2f}s({self.steps[max_time_idx]})\n'
            out += f'\tAverage # Steps = {np.mean(self.steps):.1f} (StdDev: {np.std(self.steps):.4f})\n'
            out += f'\tMin Steps(Lap Time) = {min_step}({self.lap_times[min_step_idx]:.2f}s)\n'
            out += f'\tMax Steps(Lap Time) = {max_step}({self.lap_times[max_step_idx]:.2f}s)\n'
        else:
            out += 'NO DATA COLLECTED !!!!\n'
        return out

    def __getitem__(self, idx):
        return self.plot_pts[idx]


if __name__ == '__main__':
    SimLogParser('roger-sim-24may.log')
