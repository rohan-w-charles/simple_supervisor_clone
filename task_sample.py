from message import write2fifo

IPC_FIFO_NAME = "TEST"


def TestOne():
    transfer = {"Function_NAME": "1", "Status": "DONE", "Error": None}
    write2fifo(transfer, IPC_FIFO_NAME)
    return 0


def TesTwo():
    transfer = {"Function_NAME": "2", "Status": "DONE", "Error": None}
    write2fifo(transfer, IPC_FIFO_NAME)
    return 0


def TesThree():
    transfer = {"Function_NAME": "3", "Status": "DONE", "Error": None}
    write2fifo(transfer, IPC_FIFO_NAME)
    return 0


def TesFour():
    transfer = {"Function_NAME": "4", "Status": "DONE", "Error": None}
    write2fifo(transfer, IPC_FIFO_NAME)
    return 0


if __name__ == "__main__":
    """
    Write to Fifo
    Pass along dict
    """
    IPC_FIFO_NAME = "TEST"
    TestOne()
    TesTwo()
    TesThree()
    TesFour()
    transfer_dict = {"Function_NAME": "__main__",
                     "Status": "DONE", "Error": None}
    write2fifo(transfer_dict, IPC_FIFO_NAME)
