import os
import argparse
from datetime import datetime

###################
# Parse arguments #
###################

abspath = os.path.dirname(os.path.abspath(__file__))
os.chdir(abspath)

parser = argparse.ArgumentParser(
    prog="reporting.py",
    description="Takes tracing from lgl_interpreter.py and generates a report",
    epilog="",
)
# nargs="+" means "at least one"
parser.add_argument("file", nargs="+", help="Specify lgl log files to report on")
cargs = parser.parse_args()

# Going through logfile
calls = {}
with open(cargs.file[0], "r") as f:
    lines = f.readlines()

for line in lines[1:]:
    line = line.strip().split(",")
    # Convert "2023-11-11 10:33:55.291360" back to datetime
    # or if it's a float, just convert it to float
    
    # timestamp = datetime.strptime(line[3], "%Y-%m-%d %H:%M:%S.%f")
    isdatetime = ":" in line[3]
    timestamp = float(line[3]) if not isdatetime else datetime.strptime(line[3], "%Y-%m-%d %H:%M:%S.%f")

    # First time function call is seen
    if not line[1] in calls: 
        calls[line[1]] = { line[0]: timestamp }
    # First uid is seen
    elif not line[0] in calls[line[1]]: 
        calls[line[1]][line[0]] = timestamp
    # Second time uid is seen and function is stopped
    elif line[2] == "stop": 
        delta = (timestamp - calls[line[1]][line[0]]) if not isdatetime else (timestamp - calls[line[1]][line[0]]).total_seconds()
        calls[line[1]][line[0]] = delta

# Table with f-strings
table = """
|    Function Name    | Num. of calls | Total Time (ms) | Average Time (ms) |
|---------------------------------------------------------------------------|\
"""
print(table)
for funcname, timings in calls.items():
    nrcalls = len(timings)
    totaltime = sum([timedelta for timedelta in timings.values()])
    avgtime = totaltime / nrcalls
    print(f"| {funcname:<19} | {nrcalls:^13} | {totaltime*1000:^15.3f} | {avgtime*1000:^17.3f} |")