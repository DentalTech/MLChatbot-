FROM alpine:latest
RUN apk add --no-cache py-pip 
RUN pip3 install --upgrade pip
WORKDIR ./demo/
COPY . .
RUN pip3 --no-cache-dir install -r requirements.txt                                                                            
EXPOSE 5002
ENTRYPOINT  ["python3"]
CMD ["__init__.py","--host", "0.0.0.0"]