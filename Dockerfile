FROM python:3.8-alpine

# set the working directory in the container
WORKDIR /

# install dependencies / make sure time zone is correct
RUN ln -sf /usr/share/zoneinfo/America/New_York /etc/timezone && \
    ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime && \
    pip3 install mega.py && pip3 install schedule

# copy the content of the local directory to the working directory
COPY main.py /

ENTRYPOINT ["python", "-u"]

# command to run on container start
CMD [ "main.py" ]
