from inspection_input_supplier import InspectionInputSupplier


def handler(event, _):
    anomaly_inspection_input = InspectionInputSupplier.prepare_anomaly_inspection_input(
        receivers_data_bucket=event["receiversDataBucket"]
    )
    
    return anomaly_inspection_input
