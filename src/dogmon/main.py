#!/usr/bin/env python3

import argparse
import curses
import logging
import threading
import time

from dogmon.datastore import DataStore
from dogmon import interface
from dogmon import logfile


def sleep_until(seconds, start_time):
    time.sleep(float(seconds) - ((time.time() - start_time)
               % float(seconds)))


def main_loop(stdscr, args):
    data = DataStore()

    thread_read_file = threading.Thread(target=logfile.read,
                                        args=(args.file, data))
    thread_read_file.daemon = True
    thread_read_file.start()

    interface.init(stdscr)

    start_time = time.time()

    try:
        while True:
            for log_line in data.log_lines():
                stats = logfile.parse_line(log_line)
                if stats:
                    data.stats_update(*stats)
                    data.hits_increment()

            data.hits_history_update()
            data.alerts_update(args.threshold)

            interface.refresh(stdscr, data)

            data.stats_reset()
            data.hits_reset()

            # sleep until data.SAMPLING_PERIOD seconds
            sleep_until(data.SAMPLING_PERIOD, start_time)
            logging.debug(
                f"Called every {data.SAMPLING_PERIOD} seconds")

    except KeyboardInterrupt:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d",
                        "--debug",
                        action='store_true',
                        help="print debug messages to dogmon.log")
    parser.add_argument("-f",
                        "--file",
                        default="/tmp/access.log",
                        help="set log file to monitor")
    parser.add_argument("-t",
                        "--threshold",
                        default=10,
                        type=int,
                        help="set high traffic threshold \
                              (requests per second)")
    args = parser.parse_args()

    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(filename="dogmon.log",
                        level=log_level,
                        format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%H:%M:%S")

    curses.wrapper(main_loop, args)


if __name__ == '__main__':
    main()
