# Getting AWS logs via CLI
### For more documentation on AWSLOGS, go [here](https://github.com/jorgebastida/awslogs)

1. Install AWSLOGS in python3 environment
    ```bash
    pip install awslogs
    ```

2. Prevents Git bash (MINGW64) from converting args to full windows path. 
   Example: /aws/robomaker/SimulationJobs gets changed to something like 
   C:/User/Roger/aws/robomaker/SimulationJobs
    ```bash
    # Only if using Git Bash (MINGW64)
    export MSYS_NO_PATHCONV=1
    ```

3. How to get name of stream from the GROUP in CLI. Only works for __*active*__ streams. 
   To get streams that have already completed, goto AWS Deepracer Console to get name.
    ```bash
    awslogs streams /aws/robomaker/SimulationJobs --profile adfs
    ```

4. Example of pulling logs.  Get the stream name either from the command above or from AWS Deepracer Console. 
   This will pull all data from a log in the last hour matching either "Reset" or SIM_TRACE_LOG 
   * NOTE: "Reset agent" signifies start of an episode (lap or partial lap)
    ```bash
    export STREAM=sim-bsghzkmhtnrj/2020-05-24T14-25-35.916Z_62906fdd-b366-4702-b037-1f71fb05e422/SimulationApplicationLogs
    awslogs get /aws/robomaker/SimulationJobs ${STREAM} --profile adfs --start='1 hour' --filter-pattern=?Reset\ ?SIM_TRACE_LOG > sim-24may.log
    ```
    * Example log contents from command (2 partial episodes shown below - From "Reset agent" to lap_complete/off_track)
    ```bash
    ...
    ... Reset agent
    ... SIM_TRACE_LOG:115,1,0.7063,3.5078,-94.6289,10.00,1.33,12,30.6025,False,True,0.7872,53,17.67,1590332225.6433063,in_progress
    ... SIM_TRACE_LOG:115,2,0.7068,3.5044,-94.3540,0.00,1.33,9,31.3052,False,True,0.8068,53,17.67,1590332225.710158,in_progress
    ... ...
    ... SIM_TRACE_LOG:115,118,6.0697,3.1955,156.5356,30.00,1.33,18,36.4504,True,False,63.1696,25,17.67,1590332233.4615955,off_track
    ... Reset agent
    ... SIM_TRACE_LOG:116,1,0.8919,2.6426,-78.2675,30.00,1.33,18,92.7929,False,True,0.7944,55,17.67,1590332233.888272,in_progress
    ... SIM_TRACE_LOG:116,2,0.8925,2.6412,-78.1419,-30.00,1.33,0,88.4836,False,True,0.8031,55,17.67,1590332233.9341087,in_progress
    ... ...
    ... SIM_TRACE_LOG:116,180,0.9021,2.7571,-54.7038,-30.00,1.33,0,1.5581,True,True,100.0000,54,17.67,1590332245.833309,lap_complete
    ...
    ```
# Creating Target Points
Run Targets Creator script to show all 3 possible angles.
__*targets_refs*__ in data/reinvent2018.py sets all of the selected angles and number of endpoints dependent. 
These endpoints and angles in __*targets_refs*__ were chosen by using this tool.
```bash
    python targets_creator.py -h  # show help menu
    python targets_creator.py  # show best angle (previously selected)
    python targets_creator.py -show_all_angles
    python targets_creator.py -hide_angles
```

# Plotting AWS Logs
After downloading AWS log, you can run the LogPlotter to plot log data.
Either plot a heatmap of rewards / speeds, or you can plot best headings for a group of points and click through each.
```bash
    python log_plotter.py -h  # show help menu
    python log_plotter.py -log 'roger-sim-24may.log' -groupsize 10
    python log_plotter.py -log 'roger-sim-24may.log' -heatmap reward
    python log_plotter.py -log 'roger-sim-24may.log' -heatmap speed
```
