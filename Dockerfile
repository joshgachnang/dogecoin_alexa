# Copyright 2014 Josh Gachnang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM debian:latest
MAINTAINER josh@servercobra.com

RUN apt-get update && \
    apt-get install -y build-essential python python-dev python-setuptools python-pip && \
    pip install uwsgi

# Install pip requirements first (cache them when our code changes)
ADD requirements.txt /home/docker/code/
RUN pip install -r /home/docker/code/requirements.txt

# Install our code
ADD . /home/docker/code/

WORKDIR /home/docker/code
EXPOSE 8000

CMD ["/usr/local/bin/uwsgi", "--socket", "0.0.0.0:8000", "-w", "doge:app"]
