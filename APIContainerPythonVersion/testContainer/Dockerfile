#This dockerfile builds a container image with python and rednose installed so we can test
# another built container.
# it it is designed to be launched and linked to the running container to preform the tests
# source code is not embedded in the image - it is attached

FROM alpine
MAINTAINER Robert Metcalf

COPY ./requirements.txt /test_requirements.txt
COPY ./main_app_requirements.txt /main_app_requirements.txt


RUN apk add --no-cache bash python3 curl python3-dev build-base linux-headers pcre-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    pip3 install --upgrade pip && \
    pip3 install -r /main_app_requirements.txt && \
    pip3 install -r /test_requirements.txt

##Before building cp ../src/requirements.txt ./main_app_requirements.txt
##docker build . -t metcarob/genericpythonapitester:latest
##docker run --network pythontestingnetwork --mount type=bind,source=$(pwd),target=/ext_volume metcarob/genericpythonapitester:latest nosetests --rednose /ext_volume

##docker run --network pythontestingnetwork --mount type=bind,source=$(pwd),target=/ext_volume metcarob/genericpythonapitester:latest curl virtualpresencepicture:8098/apidocs/
