FROM alpine:3.6

 RUN apk add --update \
 python3 \
 py3-pip \
 curl \
 which \
 bash
 RUN curl -sSL https://sdk.cloud.google.com | bash
 ENV PATH $PATH:/root/google-cloud-sdk/bin
 COPY . ./
 RUN pip install --upgrade pip
 RUN pip install --no-cache-dir -r requirements.txt
 ENTRYPOINT [ "python3" ]
 CMD ["main.py"]
 EXPOSE 8080:8080
