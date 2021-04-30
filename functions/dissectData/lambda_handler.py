from data_dissector import DataDissector


def handler(event, _):
    switchpoint_trio = DataDissector.dissect_data(data=event['data'])
    
    return {
        "switchpoint": switchpoint_trio.switchpoint,
        "preSwitchAverage": switchpoint_trio.pre_switch_average,
        "postSwitchAverage": switchpoint_trio.post_switch_average,
    } 
