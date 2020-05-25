#!/usr/bin/env python3
"""
Extract/parse AWS Deepracer SIM logs
"""
import re
from collections import namedtuple
import pandas as pd
import numpy as np
from reinvent2018 import target_points

Row = namedtuple('logs', 'episode, step, x_coord, y_coord, heading, steering, speed, action_taken, reward, '
                         'job_completed, all_wheels_on_track, progress, closest_waypoint_index,'
                         'track_length, time, status')

numerics = ['episode', 'step', 'x_coord', 'y_coord', 'heading', 'steering', 'speed', 'action_taken', 'reward',
            'progress', 'closest_waypoint_index', 'track_length', 'time']
booleans = ['job_completed', 'all_wheels_on_track']
strings = ['status']
truth_map = {'True': True, 'False': False}

episode = None
in_episode = False
good_episodes = []
num_offtracks = 0

filename = 'roger-sim-24may.log'

with open(filename) as f:
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
                    raise TypeError(f'DataFrame not initialized: len(good_episodes)={len(good_episodes)}')
                row = Row(*obj.group(0).split(','))
                if row.status == 'off_track':
                    in_episode = False
                    num_offtracks += 1
                    continue
                data.append(row)
                if row.status == 'lap_complete':
                    in_episode = False
                    df = pd.DataFrame(data=data)
                    df[numerics] = df[numerics].apply(pd.to_numeric)
                    for b in booleans:
                        df[b] = df[b].map(truth_map)
                    df[strings] = df[strings].astype(str)
                    indices = df.closest_waypoint_index.mod(70)
                    x2, y2 = zip(*np.array(target_points)[indices])
                    best_heading = np.degrees(np.arctan2(y2 - df['y_coord'], x2 - df['x_coord']))
                    df['best_heading'] = best_heading
                    df['direction_diff'] = abs(((best_heading - df['heading']) + 180) % 360 - 180)
                    good_episodes.append(df)

lap_times = []
steps = []
PlotPts = namedtuple('PlotPts', 'x y speed reward')
plot_pts = []
for ep in good_episodes:
    lap_time = ep.time.iloc[-1] - ep.time.iloc[0]
    print(f'episode: {ep.episode.iloc[0]}', f'steps: {ep.step.iloc[-1]}', f'lap_time={lap_time}')
    plot_pts += zip(ep.x_coord, ep.y_coord, ep.speed, ep.reward)
    lap_times.append(lap_time)
    steps.append(ep.step.iloc[-1])
print(f'\nAnalyzing {len(good_episodes) + num_offtracks} episodes...')
print(f'\tNumber of "lap_complete" episodes = {len(good_episodes)}')
print(f'\tNumber of "off_track" episodes = {num_offtracks} ... ignoring for analysis')
if len(lap_times):
    print(f'\tAverage Lap Time = {np.mean(lap_times):.2f}s (StdDev: {np.std(lap_times):.4f})')
    print(f'\tMin Lap Time(Steps) = {min(lap_times):.2f}s({steps[lap_times.index(min(lap_times))]})')
    print(f'\tMax Lap Time(Steps)= {max(lap_times):.2f}s({steps[lap_times.index(max(lap_times))]})')
    print(f'\tAverage # Steps = {np.mean(steps):.1f} (StdDev: {np.std(steps):.4f})')
    print(f'\tMin Steps(Lap Time) = {min(steps)}({lap_times[steps.index(min(steps))]:.2f}s)')
    print(f'\tMax Steps(Lap Time) = {max(steps)}({lap_times[steps.index(max(steps))]:.2f}s)')
    print(f'plot_pts = {plot_pts}')
    combined_episodes = pd.concat(good_episodes) if len(good_episodes) > 1 else good_episodes
    combined_episodes.to_excel(f'{filename.rstrip(".log")}.xlsx', index=False)
else:
    print('NO DATA COLLECTED !!!!')

