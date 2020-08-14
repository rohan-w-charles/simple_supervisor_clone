import os
import struct


def encode_msg_size(size):
    return struct.pack("<I", size)


def decode_msg_size(size_bytes):
    return struct.unpack("<I", size_bytes)[0]


def create_msg(content):
    size = len(content)
    return encode_msg_size(size) + content


def get_message(fifo):
    """Get a message from the named pipe."""
    msg_size_bytes = os.read(fifo, 4)
    msg_size = decode_msg_size(msg_size_bytes)
    msg_content = os.read(fifo, msg_size).decode("utf8")
    return msg_content


def write2fifo(text, fifo):
    try:
        content = f"{text}".encode("utf8")
        msg = create_msg(content)
        os.write(fifo, msg)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    print(encode_msg_size(12))
    print(decode_msg_size(b'\x0c\x00\x00\x00'))
