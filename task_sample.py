import os
from message import write2fifo
import time


def hey():
    return "hi Ter"


if __name__ == "__main__":

    IPC_FIFO_NAME = "TEST"
    fifo = os.open(IPC_FIFO_NAME, os.O_WRONLY)
    time.sleep(2)
    print(hey())
    transfer_dict = {"Hey": "BYE"}
    write2fifo(transfer_dict, fifo)
    time.sleep(2)
    print("Done")
    os.close(fifo)
