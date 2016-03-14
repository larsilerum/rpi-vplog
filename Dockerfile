FROM larsilerum/pythonwithgpio
MAINTAINER Lars Larsson <lars.martin.larsson@gmail.com>
RUN apt-get update
RUN apt-get install python-lxml
COPY *.py /vplog/
WORKDIR /vplog
CMD python vploginflux.py
