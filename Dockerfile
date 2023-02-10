FROM python:3.8-slim

# set the working directory in the container
WORKDIR /

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

# install dependencies / make sure time zone is correct
RUN ln -sf /usr/share/zoneinfo/America/New_York /etc/timezone && \
    ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime && \
    pip install mega.py && pip install schedule

# copy the content of the local directory to the working directory
COPY main.py /

ENTRYPOINT ["python", "-u"]

# command to run on container start
CMD [ "main.py" ]
