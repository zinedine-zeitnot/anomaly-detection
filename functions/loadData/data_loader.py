import s3fs
import pandas


class DataLoader:
    @classmethod
    def load_data(
            cls,
            receiver_id: str,
            receivers_data_bucket: str,
    ) -> list:
        '''
        Retrieve the last 40 days of a receiver's S3-hosted data as a list.
        
        
        In[1] : DataLoader.load_data(
            receiver_id="receiver#00000001",
            receivers_data_bucket="receivers-data",
        )
        
        Out[1]: [31, 30, 29, ..., 10, 11, 10]
        
        '''
        last_40_days_data_series = (
            pandas
            .read_csv(
                f"s3://{receivers_data_bucket}/{receiver_id}/data.csv",
                header=None,
                index_col=0, 
                squeeze=True,
            )
            .tail(40)
        )

        return last_40_days_data_series.values.tolist()
