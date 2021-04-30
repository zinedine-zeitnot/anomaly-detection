import boto3

s3 = boto3.client('s3')


class InspectionInputSupplier:
    @classmethod
    def prepare_anomaly_inspection_input(
            cls,
            receivers_data_bucket: str,
            receiver_id_prefix: str = "receiver#",
    ) -> dict:
        '''
        Scans the receivers data bucket to retrieve the integrality of the receiver IDs to
        be processed.
        
        
        In [1]: InspectionInputSupplier.prepare_anomaly_inspection_input(
            receivers_data_bucket="receivers-data"
        )
        
        Out[1]: {
            "receiversDataBucket": "receivers-data",
            "receiversIds": [
                "receiver#00000001",
                "receiver#00000002",
                ...,
                "receiver#00000100"
            ]
        }
        
        '''
        result = s3.list_objects_v2(
            Bucket=receivers_data_bucket,
            Prefix=receiver_id_prefix,
            Delimiter='/',
        )

        raw_receivers = result['CommonPrefixes']

        while result['IsTruncated']:
            # Continue to request the next series of results
            # (this is for circumventing s3.list_objects_v2()'s size-limited response)
            
            continuation_token = result['NextContinuationToken']

            result = s3.list_objects_v2(
                Bucket=receivers_data_bucket,
                Prefix=receiver_id_prefix,
                Delimiter='/',
                ContinuationToken=continuation_token,
            )

            raw_receivers += result['CommonPrefixes']

        return {
            "receiversDataBucket": receivers_data_bucket,
            "receiversIds": [
                item['Prefix'].strip('/')
                for item in raw_receivers
            ]
        }