from anomaly_metrics_enricher import AnomalyMetricsEnricher


def handler(event, _):
    anomaly_metrics = AnomalyMetricsEnricher.add_extra_anomaly_metrics(
        switchpoint_trio=event['switchpointTrio']
    )
    
    return anomaly_metrics
