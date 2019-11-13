#!/usr/bin/env python

import argparse
import os
import stat

def map_id(old_id, source, destination):
    if old_id < source:
        return -1
    offset = old_id - source
    return destination + offset

def shift_id(path, source, destination, shift_uids, shift_gids):
    st = os.lstat(path)

    old_uid = st.st_uid
    new_uid = map_id(old_uid, source, destination) if shift_uids else -1

    old_gid = st.st_gid
    new_gid = map_id(old_gid, source, destination) if shift_gids else -1

    if new_uid >= 0 or new_gid >= 0:
        os.lchown(path, new_uid, new_gid)
        if not stat.S_ISLNK(st.st_mode):
            os.chmod(path, st.st_mode)

parser = argparse.ArgumentParser(description="Shifts UIDs/GIDs of the directory entries.")
parser.add_argument("convert", choices=["b", "u", "g"])
parser.add_argument("path", help="Path to shift.")
parser.add_argument("src", type=int, help="First ID in souce range.")
parser.add_argument("dst", type=int, help="First ID in destination range.")

args = parser.parse_args()

shift_uids = args.convert in ["u", "b"]
shift_gids = args.convert in ["g", "b"]

def shift_id_helper(path):
    return shift_id(path, args.src, args.dst, shift_uids, shift_gids)

for root, dirs, files in os.walk(args.path):
    shift_id_helper(root)
    for file_name in files:
        file_path = os.path.join(root, file_name)
        shift_id_helper(file_path)
