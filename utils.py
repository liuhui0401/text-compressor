import math


def int2binary(val, l=None):
    """
    Convert an integer into binary string
        - val: value to be converted
        - l: if not none, the generated string will be at the length of len
    """
    st = bin(val)[2:]
    if l is not None:
        assert len(st) <= l, "length of val({}) is greater than l({})".format(val, l)
        st = "0" * (l - len(st)) + st
    return st


def binary2bytes(bstring, padding=False, mode="back"):
    """
    Convert a 0/1 string into a binary string
        - bstring: the original 0/1 string
        - padding: if True, use zero-padding to make the length of string a multiple of 8
        - mode: if "back", pad the zeros behind the string, otherwise in front of the string
    """
    l = len(bstring)
    if not padding:
        assert l % 8 == 0
    else:
        if mode == "back":
            bstring += "0" * ((-l) % 8)
        else:
            bstring = "0" * ((-l) % 8) + bstring
    st = []
    for i in range(0, l, 8):
        st.append(int(bstring[i : i + 8], 2))
    return bytes(st)


def bytes2binary(byts):
    """
    Convert some bytes to a 0/1 string
        - byts the original bytes
    """
    st = ""
    for each in byts:
        st += int2binary(each, 8)
    return st


def append_bytes(byts, length=3):
    byts = b"\x00" * (length - len(byts)) + byts
    return byts


def recover_bytes(byts):
    i = 0
    while i < len(byts) and byts[i] == 0:
        i += 1
    return byts[i:]
