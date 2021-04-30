from notification_maker import NotificationMaker


def handler(event, _):
    notification_message = NotificationMaker.prepare_anomaly_notification(
        parallelization_output=event
    )
    
    return {"notificationMessage": notification_message}
