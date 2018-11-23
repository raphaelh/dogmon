import queue

from dogmon.datastore import DataStore
from dogmon import interface
from dogmon import logfile

 
def test_alerting():
    THRESHOLD = 10

    # no alerts, below threshold, should not trigger an alert
    data = DataStore(hits_history=[59, 122, 125, 95, 127, 124, 110, 102, 106, 124, 110, 109])
    data.alerts_update(THRESHOLD)
    assert(data.hits_average() <= THRESHOLD)
    assert(data.alerts_empty())
    
    # no alerts, above threshold, should trigger an alert
    data._DataStore__hits = 124
    data.hits_history_update()
    data.alerts_update(THRESHOLD)
    assert(data._DataStore__hits_history == [122, 125, 95, 127, 124, 110, 102, 106, 124, 110, 109, 124])
    assert(sum(data.hits_history_get()) // DataStore.TIME_WINDOW > THRESHOLD)
    assert(data.hits_average() > THRESHOLD)
    assert(len(data.alerts) == 1)
    assert(data.alert_triggered())

    # alert triggered, above threshold, should not trigger another alert
    data._DataStore__hits = 82
    data.hits_history_update()
    data.alerts_update(THRESHOLD)
    assert(data._DataStore__hits_history == [125, 95, 127, 124, 110, 102, 106, 124, 110, 109, 124, 82])
    assert(data.hits_average() > THRESHOLD)
    assert(len(data.alerts) == 1)
    
    # alert triggered, below threshold, should recover the alert
    data._DataStore__hits = 92
    data.hits_history_update()
    data.alerts_update(THRESHOLD)
    assert(data._DataStore__hits_history == [95, 127, 124, 110, 102, 106, 124, 110, 109, 124, 82, 92])
    assert(data.hits_average() <= THRESHOLD)
    assert(len(data.alerts) == 2)
    assert(data.alert_recovered())
    
    # alert recovered, below threshold, should not recover alert again
    data._DataStore__hits = 108
    data.hits_history_update()
    data.alerts_update(THRESHOLD)
    assert(data._DataStore__hits_history == [127, 124, 110, 102, 106, 124, 110, 109, 124, 82, 92, 108])
    assert(data.hits_average() <= THRESHOLD)
    assert(len(data.alerts) == 2)
    
    # alert recovered, above threshold, should trigger an alert
    data._DataStore__hits = 132
    data.hits_history_update()
    data.alerts_update(THRESHOLD)
    assert(data._DataStore__hits_history == [124, 110, 102, 106, 124, 110, 109, 124, 82, 92, 108, 132])
    assert(data.hits_average() > THRESHOLD)
    assert(len(data.alerts) == 3)
    assert(data.alert_triggered())


def test_hits_history_update():
    data = DataStore(hits_history=[59, 122, 125, 95, 127, 124, 110, 102, 106, 124, 110, 109])
    data._DataStore__hits = 124
    data.hits_history_update()
    assert(data.hits_history_get() == [122, 125, 95, 127, 124, 110, 102, 106, 124, 110, 109, 124])
   
