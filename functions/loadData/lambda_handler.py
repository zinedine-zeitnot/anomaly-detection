from data_loader import DataLoader


def handler(event, _):
    data = DataLoader.load_data(
        receiver_id=event["receiverId"],
        receivers_data_bucket=event["receiversDataBucket"],
    )
    
    return data
