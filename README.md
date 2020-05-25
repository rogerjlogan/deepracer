# Getting AWS logs via CLI
### For more documentation on AWSLOGS, go [here](https://github.com/jorgebastida/awslogs)
```bash
# Prevents Git bash (MINGW64) from converting args to full windows path
# Example: /aws/robomaker/SimulationJobs gets changed to something like C:/User/Roger/aws/robomaker/SimulationJobs

export MSYS_NO_PATHCONV=1
```
```bash
# Need to get name of stream from the GROUP
# Get list of *active* streams.  To get streams that have already completed, got AWS Deepracer Console to get name.

awslogs streams /aws/robomaker/SimulationJobs --profile adfs
```
```bash
# Example of pulling logs.  Get the stream name from AWS Deepracer Console
# This will pull all data from a log in the last hour matching either "Reset" or SIM_TRACE_LOG (Reset is start of an episode)

export STREAM=sim-bsghzkmhtnrj/2020-05-24T14-25-35.916Z_62906fdd-b366-4702-b037-1f71fb05e422/SimulationApplicationLogs
awslogs get /aws/robomaker/SimulationJobs $STREAM --profile adfs --start='1 hour' --filter-pattern=?Reset\ ?SIM_TRACE_LOG > sim-24may.log
```
 