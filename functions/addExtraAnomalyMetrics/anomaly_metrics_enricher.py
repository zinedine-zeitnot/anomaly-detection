class AnomalyMetricsEnricher:
    @classmethod
    def add_extra_anomaly_metrics(cls, switchpoint_trio: dict) -> dict:
        anomaly_metrics = switchpoint_trio

        anomaly_metrics['preSwitchAverageOverPostSwitchAverage'] = (
            anomaly_metrics['preSwitchAverage'] / anomaly_metrics['postSwitchAverage']
        )

        return anomaly_metrics
