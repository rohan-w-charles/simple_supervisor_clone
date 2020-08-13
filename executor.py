import time
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help='File name')

args = parser.parse_args()


def is_processRunning(file_name, pid):
    cmd = [f'pgrep -f .*python3.*{file_name}']
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    my_pid, err = process.communicate()
    my_pids = list(map(int, my_pid.splitlines()))
    if pid in my_pids:
        return True
    else:
        return False


def run_process(file_name, log_name):
    with open(f'{log_name}.txt', 'a') as f:
        process = subprocess.Popen(['python3', file_name], stdout=f)
    return process


if __name__ == "__main__":
    filename = args.file
    process = run_process(filename, f"log_for_{filename}")
    flag = True
    while flag:
        flag = is_processRunning(filename, pid=process.pid)
        print("Process running !!")
        time.sleep(1)
    print("Process Stopped !!!")
