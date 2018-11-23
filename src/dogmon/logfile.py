import re
import subprocess


def read(path, data):
    """
    Fill a queue asynchronously with the output from tail -F
    """
    # Gets subprocess' output line by line as soon as the subprocess
    # flushes its stdout buffer
    # Use -F and not -f to track the actual name of the file, not the
    # file descriptor (to deal with log rotation)
    with subprocess.Popen(['tail', '-F', path],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL,
                          bufsize=1,
                          universal_newlines=True) as proc:
        for line in proc.stdout:
            data.log_lines_put(line)


def parse_line(line):
    """
    Parse a log line to extract IP, path, status and length
    """
    # The common logfile format is as follows:
    # remotehost rfc931 authuser [date] "request" status bytes
    regex = re.compile(r'^(?P<ip>.*?) (?P<remote_log_name>.*?) '
                       r'(?P<userid>.*?) \[(?P<date>.*?)(?= ) '
                       r'(?P<timezone>.*?)\] \"(?P<request_method>.*?) '
                       r'(?P<path>.*?)(?P<request_version> HTTP/.*)?\" '
                       r'(?P<status>.*?) (?P<length>.*?)$')

    match = regex.match(line.rstrip('\n'))
    if match is not None:
        return (match.group('ip'), match.group('path'),
                match.group('status'), match.group('length'))
