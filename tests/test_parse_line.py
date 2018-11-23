from dogmon import logfile

def test_parse_line():
    line_valid = '65.55.213.74 - - [17/May/2015:15:05:45 +0000] "GET /blog/tags/logging HTTP/1.1" 200 19423'
    assert(logfile.parse_line(line_valid) == ('65.55.213.74', '/blog/tags/logging', '200', '19423'))
    
    line_invalid = '65.55.213.74 - - [17/May/2015:15:05:45 +0000] "GET /blog/tags/logging HTTP/1.1" 200'
    assert(logfile.parse_line(line_invalid) == None)
