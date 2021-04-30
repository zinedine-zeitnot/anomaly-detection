## What's this repo for?

This repository hosts the infrastructure and logic behind the anomaly detection pipeline described in the following companion blog post: [Automating the discovery of anomalies in reception data with AWS Step Functions](https://bit.ly/2Rcv6Zw).


## Project structure

- `data/` folder: contains two samples of receiver data (one healthy, one not) used for populating the receivers' data bucket.
- `functions/` folder: contains the source code of the AWS Lambda functions used in this project.
- `utils/` folder: contains the code to populate the receivers' data bucket with a handful of receiver data to begin with.
- `workflows/` folder: contains the definition of the two AWS Step Functions state machines used in this project.
- `template.yaml` file: [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) template defining the infrastructure of our application.

## Deploying the application stack to AWS

_ECR prerequisite_: You'll need to have previously set up an [ECR](https://aws.amazon.com/ecr/) repository to host the Docker image used as deployment package of the **dissectData** Lambda function. For that matter, you'll need the following tools installed on your machine:
- The [AWS CLI](https://aws.amazon.com/cli/) to create your ECR repo from the command line and log you in
- [Docker](https://docs.docker.com/get-docker/), so you can log in to your ECR repo before pushing the Docker image

Once you've got both, creation and authentication are achieved via a couple of shell commands:
```bash
$ aws ecr create-repository --repository-name <your-ecr-repo-name, e.g. anomaly-detection-app-repository> --image-tag-mutability IMMUTABLE --image-scanning-configuration scanOnPush=true

$ aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account id>.dkr.ecr.<region>.amazonaws.com
```

We redirect the curious reader towards the following blog post for additional context about the use of a Docker image as an alternative way to package AWS Lambda functions: [Using container image support for AWS Lambda with AWS SAM](https://aws.amazon.com/blogs/compute/using-container-image-support-for-aws-lambda-with-aws-sam/).

(end of ECR prerequisite.)

Once you have your ECR repo up and running, you'll need the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) to build and deploy the application stack.

Then, from the project root (location of the `template.yaml` file), simply run: 
```bash
$ sam build --use-container && sam deploy --guided
```

After the build completes, you'll be prompted to enter a series of stack parameters like so:
```
Stack Name: <Stack name of your choosing, e.g. AnomalyDetectionApp>
AWS Region: <Your favorite AWS region>
Parameter ReceiversDataBucket: <Your bucket name> 
Parameter AnomalyNotificationTopicName: <Your anomaly topic name> 
Parameter PrincipalAnomalySubscriberEmail: <your.email@example.com> 
Image Repository for DissectData: <your-account-id>.dkr.ecr.<your-aws-region>.amazonaws.com/<your-ecr-repo-name>
```

And, after a few minutes (and if all did well): hooray, your stack's ready for some anomaly diagnosing!

(well... *almost*. The only missing piece is setting up some data to analyze, of course. But fair enough: create a S3 bucket for hosting the receivers data and launch the seeding script `populate_receivers_data_bucket.py`. Also, don't forget to check your mailbox and confirm your subscription to the anomaly topic beforehand or you won't be alerted!)
