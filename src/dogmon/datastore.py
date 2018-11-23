import datetime
import queue
import logging


class DataStore:
    SAMPLING_PERIOD = 10
    TIME_WINDOW = 120
    HISTORY_SIZE = int(TIME_WINDOW / SAMPLING_PERIOD)

    ALERT_RECOVERED = -1

    def __init__(self, log_lines=None, hits=None, hits_history=None,
                 stats=None, alerts=None):
        if log_lines is None:
            self.log_lines_init()
        else:
            self.__log_lines = log_lines

        if hits is None:
            self.hits_init()
        else:
            self.__hits = hits

        if hits_history is None:
            self.hits_history_init()
        else:
            self.__hits_history = hits_history

        if stats is None:
            self.stats_init()
        else:
            self.__stats = stats

        if alerts is None:
            self.alerts_init()
        else:
            self.alerts = alerts

    def log_lines_init(self):
        self.__log_lines = queue.Queue()

    def hits_init(self):
        self.__hits = 0

    def hits_history_init(self):
        self.__hits_history = [0] * self.HISTORY_SIZE

    def stats_init(self):
        self.__stats = {'visitors': {},
                        'paths': {},
                        'status_codes': {},
                        'not_found': {},
                        'bytes_served': 0}

    def alerts_init(self):
        self.alerts = []

    def alerts_reset(self):
        self.alerts_init()

    def hits_reset(self):
        self.hits_init()

    def stats_reset(self):
        self.stats_init()

    def hits_increment(self):
        self.__hits += 1

    def hits_history_update(self):
        # emulate a fixed-size FIFO queue, when a new
        # value is inserted it pushes the oldest one out
        self.__hits_history.append(self.__hits)
        self.__hits_history = self.__hits_history[-self.HISTORY_SIZE:]
        logging.debug(f"hits_history = {self.__hits_history}")

    def hits_average(self):
        return sum(self.__hits_history) // self.TIME_WINDOW

    def hits_history_get(self):
        return self.__hits_history

    def stats_update(self, ip, path, status, length):
        if ip in self.__stats['visitors']:
            self.__stats['visitors'][ip] += 1
        else:
            self.__stats['visitors'][ip] = 1

        if path in self.__stats['paths']:
            self.__stats['paths'][path] += 1
        else:
            self.__stats['paths'][path] = 1

        if status in self.__stats['status_codes']:
            self.__stats['status_codes'][status] += 1
        else:
            self.__stats['status_codes'][status] = 1

        if status == '404':
            if path in self.__stats['not_found']:
                self.__stats['not_found'][path] += 1
            else:
                self.__stats['not_found'][path] = 1

        try:
            self.__stats['bytes_served'] += int(length)
        except ValueError:
            # when length is not provided in the log and is "-" instead
            pass

    def alerts_empty(self):
        return (not self.alerts)

    def alert_triggered(self):
        return (not self.alerts_empty()
                and self.alerts[-1][0] != self.ALERT_RECOVERED)

    def alert_recovered(self):
        return (not self.alerts_empty()
                and self.alerts[-1][0] == self.ALERT_RECOVERED)

    def alert_trigger(self):
        logging.debug(
            f"alert_trigger: hits_average = {self.hits_average()}")
        self.alerts.append([self.hits_average(),
                            datetime.datetime.now()])

    def alert_recover(self):
        logging.debug(
            f"alert_trigger: hits_average = {self.hits_average()}")
        self.alerts.append([-1,
                            datetime.datetime.now()])

    def alerts_update(self, threshold):
        if self.hits_average() > threshold:
            if self.alerts_empty() or self.alert_recovered():
                self.alert_trigger()
        else:
            if self.alert_triggered():
                self.alert_recover()

    def log_lines_put(self, line):
        self.__log_lines.put(line.rstrip())

    def log_lines(self):
        # get_nowait is a reliable way to read a stream
        # without blocking regardless of operating system
        while True:
            try:
                yield self.__log_lines.get_nowait()
            except queue.Empty:
                return

    def top_sections(self):
        sections = {}

        for path in self.__stats['paths']:
            # if the path doesn't contain a '/' after the 1st char
            # then it's not a section
            if '/' in path[1:]:
                section = path[1:].split('/')[0]
                if section in sections:
                    sections[section] += self.__stats['paths'][path]
                else:
                    sections[section] = self.__stats['paths'][path]

        return sorted(sections.items(), key=lambda kv: kv[1],
                      reverse=True)

    def top_not_found(self):
        return sorted(self.__stats['not_found'].items(),
                      key=lambda kv: kv[1], reverse=True)

    def total_requests(self):
        return sum(self.__stats['paths'].values())

    def unique_visitors(self):
        return len(self.__stats['visitors'])

    def bytes_served(self):
        return self.__stats['bytes_served']
