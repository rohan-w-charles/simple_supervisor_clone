import subprocess
import argparse
import os
import ast
import errno
import select

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help='File name')
args = parser.parse_args()


def is_processrunning(file_name, pid):
    cmd = [f'pgrep -f .*python3.*{file_name}']
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    my_pid, err = process.communicate()
    running_pids = list(map(int, my_pid.splitlines()))
    return pid in running_pids


def run_process(file_name, log_name):
    return subprocess.Popen(['python3', file_name],
                            stdout=open(f'{log_name}.txt', 'a'))


"""
-- Old Version of reading from fifo

def read_fifo(FIFO):
    with open(FIFO) as fifo:
        while True:
            data = fifo.read()
            return data
"""


def strip_values(val):
    return "".join([i for
                    i in ss if (i in ["{", "}", ":", '"', "'"]
                                or i.isalpha())])


def read_fifo(FIFO_PATH):
    with open(FIFO_PATH) as fifo:
        while True:
            select.select([fifo], [], [fifo])
            data = fifo.read()
            return data


if __name__ == "__main__":
    IPC_FIFO_NAME = "TEST"
    try:
        os.mkfifo(IPC_FIFO_NAME)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            print("PIPE ALREADY EXISTS .....!!")

    process = run_process(args.file, args.file)
    ss = read_fifo(IPC_FIFO_NAME)
    ss = strip_values(ss)
    json_values = ast.literal_eval(ss)
    print(json_values["Hey"])
    os.remove(IPC_FIFO_NAME)
