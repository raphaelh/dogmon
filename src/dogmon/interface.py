import curses
import logging
import math


def format_bytes(count):
    """
    Format bytes in human-readable format
    """
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB']:
        if abs(count) < 1024.0:
            return f"{count:3.1f} {unit}"
        count /= 1024.0
    return f"{count:.1f} YiB"


def refresh_window_stats(max_screen_lines, max_screen_columns, data):
    max_stats_lines = math.ceil(max_screen_lines / 2) - 2
    left_column_start = 2
    right_column_start = math.ceil(max_screen_columns / 2) + 1

    window_stats = curses.newwin(max_stats_lines + 2,
                                 max_screen_columns,
                                 0,
                                 0)
    window_stats.erase()
    window_stats.box()

    window_stats.addstr(1, left_column_start,
                        f"Total requests: {data.total_requests()}")
    window_stats.addstr(2, left_column_start,
                        f"Unique visitors: {data.unique_visitors()}")
    window_stats.addstr(3, left_column_start,
                        f"Bytes served: {format_bytes(data.bytes_served())}")

    start_line = 5
    window_stats.addstr(start_line, left_column_start,
                        "Top sections sorted by hits:",
                        curses.A_UNDERLINE)

    top_sections = data.top_sections()
    lines_displayed = min(len(top_sections),
                          max_stats_lines - start_line)

    # width used before : 1 vertical border + 1 space
    #                     + 4 chars for hits + 1 space
    # after : 1 space
    # total = 8
    name_trunc_width = math.ceil(max_screen_columns / 2) - 8
    for line in range(lines_displayed):
        name, hits = top_sections[line]
        window_stats.addstr(start_line + line + 1, 2,
                            f"{hits:>4} {name[:name_trunc_width]}")

    window_stats.addstr(start_line, right_column_start,
                        "Top not found URLs sorted by hits:",
                        curses.A_UNDERLINE)

    top_not_found = data.top_not_found()
    lines_displayed = min(len(top_not_found),
                          max_stats_lines - start_line)

    # width used before : 1 space + 4 chars for hits + 1 space
    # after : 1 space + 1 vertical border
    # total = 8
    name_trunc_width = math.floor(max_screen_columns / 2) - 8
    for line in range(lines_displayed):
        name, hits = top_not_found[line]
        window_stats.addstr(start_line + line + 1, right_column_start,
                            f"{hits:>4} {name[:name_trunc_width]}")

    window_stats.refresh()


def refresh_window_alerts(max_screen_lines, max_screen_columns, data):
    max_alerts_lines = math.floor(max_screen_lines / 2) - 2
    left_column_start = 2

    window_alerts = curses.newwin(
                             max_alerts_lines + 2,
                             max_screen_columns,
                             max_screen_lines - max_alerts_lines - 2,
                             0)
    window_alerts.erase()
    window_alerts.box()

    lines_displayed = min(len(data.alerts), max_alerts_lines)
    logging.debug(f"{lines_displayed} alerts to display out of "
                  f"{len(data.alerts)}: {[a[0] for a in data.alerts]}")

    for line in range(lines_displayed):
        hits_average, alert_time = data.alerts[-lines_displayed + line]

        if hits_average == data.ALERT_RECOVERED:
            window_alerts.addstr(line + 1, left_column_start,
                                 f"High traffic alert recovered at "
                                 f"{alert_time:%H:%M:%S}")
        else:
            window_alerts.addstr(line + 1, left_column_start,
                                 f"High traffic generated an alert - "
                                 f"hits = {hits_average}, "
                                 f"triggered at {alert_time:%H:%M:%S}")

    window_alerts.refresh()


def refresh(stdscr, data):
    max_screen_lines, max_screen_columns = stdscr.getmaxyx()
    refresh_window_stats(max_screen_lines, max_screen_columns, data)
    refresh_window_alerts(max_screen_lines, max_screen_columns, data)


def init(stdscr):
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)

    stdscr.nodelay(1)
    stdscr.clear()
    stdscr.refresh()
