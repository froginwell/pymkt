FROM python:3.6
RUN pip --no-cache-dir install gevent && \
    pip --no-cache-dir install gunicorn
COPY pymkt /tmp/src/pymkt
COPY setup.py /tmp/src/setup.py
RUN cd /tmp/src && python setup.py install
