import subprocess
import argparse
import os
import ast
import errno
import time
import select
from message import get_message
import asyncio

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', required=True, help='File name')
parser.add_argument('--pid', '-p', required=False, help='File name')
args = parser.parse_args()


async def async_is_processrunning(process):
    return True if process.poll() is None else False


def is_processrunning(process):
    return True if process.poll() is None else False


def run_process(file_name, log_name):
    return subprocess.Popen(['python3', file_name],
                            stdout=open(f'{log_name}.txt', 'a'))


def read_fifo(FIFO_PATH):
    fifo = open(FIFO_PATH)
    while True:
        select.select([fifo], [], [fifo])
        data = fifo.read()
        return data


def reader(IPC_FIFO_NAME, start_time):
    fifo = os.open(IPC_FIFO_NAME, os.O_RDONLY | os.O_NONBLOCK)
    while True and (start_time + 3 > time.time()):
        try:
            msg = get_message(fifo)
            return msg
        except Exception as e:
            if e != "unpack requires a buffer of 4 bytes":
                assert True, "Error in reading message"
    return None


async def async_ipc_interface(IPC_FIFO_NAME):
    try:
        os.mkfifo(IPC_FIFO_NAME)
        time.sleep(1)
    except OSError as oe:
        if oe.errno == errno.EEXIST:
            pass
        else:
            assert False, f"Error {os.errno}"
    output = reader(IPC_FIFO_NAME, time.time())
    if output is None:
        return None
    json_values = ast.literal_eval(output)
    os.remove(IPC_FIFO_NAME)
    return json_values


def ipc_interface(IPC_FIFO_NAME):
    try:
        os.mkfifo(IPC_FIFO_NAME)
        time.sleep(1)
    except OSError as oe:
        if oe.errno == errno.EEXIST:
            pass
        else:
            assert False, f"Error {os.errno}"
    output = reader(IPC_FIFO_NAME, time.time())
    if output is None:
        return None
    json_values = ast.literal_eval(output)
    os.remove(IPC_FIFO_NAME)
    return json_values


async def main(process, IPC_FIFO_NAME):
    output = await asyncio.gather(async_is_processrunning(process),
                                  async_ipc_interface(IPC_FIFO_NAME))
    return output


if __name__ == "__main__":
    IPC_FIFO_NAME = "TEST"
    process = run_process(args.file, args.file)
    flag = True
    while flag:
        output = asyncio.run(main(process, IPC_FIFO_NAME))
        print("Is Process Running ::", output[0])
        print("Message From process ::", output[1])
        flag = output[0]
    os.remove(IPC_FIFO_NAME)

"""
Sync Running the process
if __name__ == "__main__":
    # Asyc process
    # Sub process messages
    process = run_process(args.file, args.file)
    flag = is_processrunning(process)
    while flag:
        output = ipc_interface(IPC_FIFO_NAME)
        if output is not None:
            print(output)
        flag = is_processrunning(process)
        print("Is process running ::", flag)
        print("Process Id ::", process.pid)
    output = ipc_interface(IPC_FIFO_NAME)
    poll = process.poll()
    while output is not None:
        print("Outside--->", output)
    os.remove(IPC_FIFO_NAME)
"""
