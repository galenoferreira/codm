FROM opendronemap/odm:gpu  as build
#para subir um container novo, basta rodar push-docker.sh 

RUN pip3 install  awscli


COPY entry.sh /

ENTRYPOINT [ "/entry.sh" ]

