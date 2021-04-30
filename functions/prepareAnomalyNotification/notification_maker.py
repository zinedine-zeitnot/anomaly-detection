class NotificationMaker:
    @classmethod
    def prepare_anomaly_notification(cls, parallelization_output: list) -> str:
        faulty_receivers = [item for item in parallelization_output if item != {}]
        
        notification_message = (
            f"Anomalies detected for the following list of receivers: "
            f"(empty if none found) {faulty_receivers}."
        )
        
        return notification_message
