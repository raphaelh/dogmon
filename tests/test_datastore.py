import queue

from dogmon.datastore import DataStore
from dogmon import interface
from dogmon import logfile


def test_data():
    list_log_lines = \
           ['65.55.213.74 - - [17/May/2015:15:05:45 +0000] "GET /blog/tags/open%20source HTTP/1.1" 200 19423',
            '65.55.213.74 - - [17/May/2015:15:05:36 +0000] "GET /tag/geekery/CEE-logging-for-profit.html HTTP/1.1" 200 13358',
            '65.55.213.74 - - [17/May/2015:15:05:34 +0000] "GET /blog/tags/wine HTTP/1.1" 200 10021',
            '65.55.213.74 - - [17/May/2015:15:05:57 +0000] "GET /tag/geekery/tf2-wine-linux-performance-tuning.html HTTP/1.1" 200 10021',
            '65.55.213.74 - - [17/May/2015:15:05:15 +0000] "GET /blog/tags/rants HTTP/1.1" 200 39692',
            '65.55.213.74 - - [17/May/2015:15:05:21 +0000] "GET /blog/tags/X11 HTTP/1.1" 200 32742',
            '68.180.224.225 - - [17/May/2015:15:05:19 +0000] "GET /blog/tags/ipcp HTTP/1.1" 404 9983',
            '65.55.213.74 - - [17/May/2015:15:05:20 +0000] "GET /blog/tags/open%20source HTTP/1.1" 200 11113',
            '65.55.213.73 - - [17/May/2015:15:05:57 +0000] "GET /blog/tags/ipcp HTTP/1.1" 404 9514',
            '65.55.213.73 - - [17/May/2015:15:05:40 +0000] "GET /blog/tags/sysadmin HTTP/1.1" 404 40797'
           ]

    queue_log_lines = queue.Queue()
    for line in list_log_lines:
        queue_log_lines.put(line)

    data = DataStore(log_lines = queue_log_lines)
    for log_line in data.log_lines():
        stats = logfile.parse_line(log_line)
        if stats:
            data.stats_update(*stats)
            data.hits_increment()

    assert(data.total_requests() == 10)
    assert(data.unique_visitors() == 3)
    assert(data.bytes_served() == 196664)
    assert(data.top_sections() == [('blog', 8), ('tag', 2)])
    assert(data.top_not_found() == [('/blog/tags/ipcp', 2),
                                    ('/blog/tags/sysadmin', 1)])

