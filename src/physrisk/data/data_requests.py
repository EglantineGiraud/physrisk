from typing import List
from collections import defaultdict

class EventDataRequest:
    def __init__(self, event_type: type, longitude: float, latitude: float, **kwargs):
        self.event_type = event_type
        self.longitude = longitude
        self.latitude = latitude
        self.key = '_'.join(str(k) + ":" + str(v) for k, v in sorted(kwargs.items()))
        #self.key = sorted(kwargs.items())
        self.props = dict(**kwargs)

class ReturnPeriodEvDataResp:
    def __init__(self, return_periods, intensities):
        self.return_periods = return_periods
        self.intensities = intensities

def process_requests(requests : List[EventDataRequest], data_sources):
    prop_groups = defaultdict(list)
    for request in requests:
        prop_groups[request.key].append(request)
    
    responses = {}
    for key in prop_groups.keys():
        request_group = prop_groups[key]
        props = request_group[0].props
        event_type = request_group[0].event_type
        longitudes = [req.longitude for req in request_group]
        latitudes = [req.latitude for req in request_group]
        ret_period, intensities = data_sources[event_type](longitudes, latitudes, **props)
        
        for i, req in enumerate(request_group):
            responses[req] = ReturnPeriodEvDataResp(ret_period, intensities[i, :])
    
    return responses
