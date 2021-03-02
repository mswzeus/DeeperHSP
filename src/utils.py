# Written by Seonwoo Min, Seoul National University (mswzeus@gmail.com)

import os
import sys
import random
import datetime
import numpy as np

import torch


def Print(string, output, newline=False, timestamp=True):
    """ print to stdout and a file (if given) """
    if timestamp:
        time = datetime.datetime.now()
        line = '\t'.join([str(time.strftime('%m-%d %H:%M:%S')), string])
    else:
        time = None
        line = string

    print(line, file=sys.stderr)
    if newline: print("", file=sys.stderr)

    if not output == sys.stdout:
        print(line, file=output)
        if newline: print("", file=output)

    output.flush()
    return time


def set_seeds(seed):
    """ set random seeds """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def check_args(args):
    """ sanity check for arguments """
    if "checkpoint" in args and args["checkpoint"] is not None and not os.path.exists(args["checkpoint"]):
        sys.exit("checkpoint [%s] does not exists" % (args["checkpoint"]))
    if "data_path" in args and (args["data_path"] is None or not os.path.exists(args["data_path"] + "/FASTA/")):
        sys.exit("data_path [%s] does not have a FASTA directory" % (args["data_path"]))


def set_output(args, string):
    """ set output configurations """
    output, save_prefix = sys.stdout, None
    if args["output_path"] is not None:
        save_prefix = args["output_path"]
        if not os.path.exists(save_prefix):
            os.makedirs(save_prefix, exist_ok=True)
        output = open(args["output_path"] + "/" + string + ".txt", "a")

    return output, save_prefix
