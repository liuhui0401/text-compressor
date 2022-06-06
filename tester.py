# -*- coding:utf-8 -*-
import os
from compressor import *
import argparse

text_folder = "./text"
temp_file = "out.c"
rec_file = "recover.txt"


def testfile(filename, compressor):
    os.system("rm -f " + temp_file + " " + rec_file)
    compressor.compress(filename, temp_file)
    compressor.decompress(temp_file, rec_file)
    with open(filename, "rb") as f:
        s1 = f.read()
    try:
        with open(rec_file, "rb") as f:
            s2 = f.read()
    except FileNotFoundError:
        return False, 0, 0, "output file not found"

    originalSize = os.path.getsize(filename)
    compressSize = os.path.getsize(temp_file)
    return s1 == s2, compressSize, originalSize, "files does not match"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("compressor", type=str)
    parser.add_argument("-t", type=str, help="indicate which text file to test")
    args = parser.parse_args()
    exec("compressor = " + args.compressor + "()")
    print("Start testing " + args.compressor + " ...")
    incorrect_count = 0
    corrects = []
    filenames = (args.t,) if args.t is not None else os.listdir(text_folder)

    filelen = 0
    for each in filenames:
        filelen = max(filelen, len(each))
    filelen += 8

    for filename in filenames:
        if os.path.splitext(filename)[-1] == ".txt":
            fullpath = os.path.join(text_folder, filename)
            print(filename + ":" + " " * (filelen - len(filename)), end="")
            correct, compressSize, originalSize, msg = testfile(fullpath, compressor)
            if not correct:
                print("\t\033[1;31mIncorrect!\033[0m", msg)
                incorrect_count += 1
            else:
                print(
                    "\t\033[1;34mCorrect!\033[0m Compress rate: \033[1;36m{:.4f}\033[0m%\t({}/{}) ".format(
                        100 * compressSize / originalSize, compressSize, originalSize
                    )
                )
                corrects.append(compressSize / originalSize)

    print()
    if incorrect_count == 0:
        print("\033[1;32mAll tests passed!\033[0m")
    if len(corrects) != 0:
        acr = sum(corrects) / len(corrects)
        print("Average compression rate: \033[1;33m{:.4f}\033[0m".format(acr))
        score = max(0, min(80 - 20 * incorrect_count, 400 * (0.7 - acr)))
        print("\033[1;33mYour score: {:.2f}\033[0m".format(score))
        if score == 80:
            print("✨ \033[1;32mCongratulations!\033[0m ✨")
    else:
        print("\033[1;31mNo test passed!\033[0m")

    try:
        os.remove(temp_file)
        os.remove(rec_file)
    except FileNotFoundError:
        pass
