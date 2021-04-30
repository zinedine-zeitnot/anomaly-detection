FROM public.ecr.aws/lambda/python:3.7

COPY lambda_handler.py data_dissector.py requirements.txt ./

RUN python3.7 -m pip install -r requirements.txt -t .

CMD ["lambda_handler.handler"]
