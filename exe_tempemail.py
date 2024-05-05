import sys
from typing import Tuple

from dist.app import GalxeApp, cli_args_work_type


def kick_starter():
    (is_vpn, w) = cli_args_work_type(3)
    c = GalxeApp()
    c.port_vpn = 7890 if is_vpn is True else 0
    c.misc_mode = True
    c.start_from_index = 0
    c.init_all_keyfiles()
    c.worker_type = w
    c.loop_major()


if __name__ == '__main__':
    kick_starter()
