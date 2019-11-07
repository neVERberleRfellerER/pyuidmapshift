#!/usr/bin/env python

import argparse
import os

def shift_id(path, source, destination, shift_uids, shift_gids):
    st = os.lstat(path)

    old_uid = st.st_uid
    uid_offset = old_uid - source
    new_uid = destination + uid_offset if shift_uids else -1

    old_gid = st.st_gid
    gid_offset = old_gid - source
    new_gid = destination + gid_offset if shift_gids else -1

    os.lchown(path, new_uid, new_gid)

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
