import boto3

s3 = boto3.client('s3')


RECEIVERS_DATA_BUCKET = "receivers"
RECEIVERS_LIST = ["receiver#" + f"{i}".zfill(8) for i in range(1, 101)]
ABNORMAL_RECEIVER = RECEIVERS_LIST[0]


def upload_receiver_data_to_s3(receiver_id: str, data_type: str) -> None:
    with open(f"data/{data_type}-data.csv", "rb") as data:
        print(f"Uploading {data_type} data for {receiver_id}...")

        s3.upload_fileobj(
            Fileobj=data,
            Bucket=RECEIVERS_DATA_BUCKET,
            Key=f"{receiver_id}/data.csv",
        )


if __name__ == "__main__":
    upload_receiver_data_to_s3(receiver_id=ABNORMAL_RECEIVER, data_type="abnormal")

    for receiver_id in RECEIVERS_LIST[1:]:
        upload_receiver_data_to_s3(receiver_id=receiver_id, data_type="normal")
