FROM jrottenberg/ffmpeg:4-ubuntu

RUN apt-get -yqq update && \
    apt-get install -yq --no-install-recommends python3.9 python3-pip && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    pip3 install --verbose esdk-obs-python flask --no-cache-dir

WORKDIR /

COPY --chown=1003:1003 ./ /

EXPOSE 8000

ENTRYPOINT  ["python3"]
CMD         ["/index.py"]