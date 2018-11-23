import queue

from dogmon.datastore import DataStore
from dogmon import interface
from dogmon import logfile


def test_utf8():
    list_log_lines = \
           ['65.55.213.74 - - [17/May/2015:15:05:45 +0000] "GET /blog/tags/찦차를 타고 온 펲시맨과 쑛다리 똠방각하 HTTP/1.1" 404 19423',
            '65.55.213.74 - - [17/May/2015:15:05:36 +0000] "GET /tag/geekery/울란바토르 HTTP/1.1" 404 13358',
            '65.55.213.74 - - [17/May/2015:15:05:34 +0000] "GET /blog/tags/ test  HTTP/1.1" 404 10021',
            '65.55.213.74 - - [17/May/2015:15:05:57 +0000] "GET /tag/geekery/表ポあA鷗ŒéＢ逍Üßªąñ丂㐀 HTTP/1.1" 404 10021',
            '65.55.213.74 - - [17/May/2015:15:05:15 +0000] "GET /blog/tags/ʇunpᴉpᴉɔuᴉ HTTP/1.1" 404 39692',
            '65.55.213.74 - - [17/May/2015:15:05:21 +0000] "GET /blog/tags/🏳0🌈️ HTTP/1.1" 404 32742',
            '68.180.224.225 - - [17/May/2015:15:05:19 +0000] "GET /blog/tags/Ṱ̺̺̕o͞ ̷i̲̬͇̪͙n̝̗͕v̟̜̘̦͟o̶̙̰̠kè͚̮̺̪̹̱̤ ̖t̝͕̳̣̻̪͞h̼͓̲̦̳̘̲e͇̣̰̦̬͎ ̢̼̻̱̘h͚͎͙̜̣̲ͅi̦̲̣̰̤v̻͍e̺̭̳̪̰-m̢iͅn̖̺̞̲̯̰d HTTP/1.1" 404 9983',
            '65.55.213.74 - - [17/May/2015:15:05:20 +0000] "GET /blog/tags/❤️ 💔 💌 💕 💞 💓 💗 💖 💘 💝 💟 💜 💛 💚 💙 HTTP/1.1" 404 11113',
            '65.55.213.73 - - [17/May/2015:15:05:57 +0000] "GET /tag/geekery/🇺🇸🇷🇺🇸 🇦🇫🇦🇲🇸 HTTP/1.1" 404 9514',
            '65.55.213.73 - - [17/May/2015:15:05:40 +0000] "GET /blog/tags/التَّطْبِيقَاتُ الْحاسُوبِيَّةُ HTTP/1.1" 404 40797'
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

    assert(data.top_not_found() ==
           [('/blog/tags/찦차를 타고 온 펲시맨과 쑛다리 똠방각하', 1),
            ('/tag/geekery/울란바토르', 1),
            ('/blog/tags/\u2029test\u2029', 1),
            ('/tag/geekery/表ポあA鷗ŒéＢ逍Üßªąñ丂㐀', 1),
            ('/blog/tags/ʇunpᴉpᴉɔuᴉ', 1),
            ('/blog/tags/🏳0🌈️', 1),
            ('/blog/tags/Ṱ̺̺̕o͞ ̷i̲̬͇̪͙n̝̗͕v̟̜̘̦͟o̶̙̰̠kè͚̮̺̪̹̱̤ ̖t̝͕̳̣̻̪͞h̼͓̲̦̳̘̲e͇̣̰̦̬͎ ̢̼̻̱̘h͚͎͙̜̣̲ͅi̦̲̣̰̤v̻͍e̺̭̳̪̰-m̢iͅn̖̺̞̲̯̰d', 1),
            ('/blog/tags/❤️ 💔 💌 💕 💞 💓 💗 💖 💘 💝 💟 💜 💛 💚 💙', 1),
            ('/tag/geekery/🇺🇸🇷🇺🇸 🇦🇫🇦🇲🇸', 1),
            ('/blog/tags/التَّطْبِيقَاتُ الْحاسُوبِيَّةُ', 1)])
