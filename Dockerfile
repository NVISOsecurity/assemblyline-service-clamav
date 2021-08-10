FROM cccs/assemblyline-v4-service-base:stable

ENV SERVICE_PATH clamav.ClamAV

USER root

RUN apt update
RUN apt install -y clamav clamav-freshclam
RUN freshclam

USER assemblyline

WORKDIR /opt/al_service
COPY . .

ARG version=4.0.0.dev1
USER root
RUN sed -i -e "s/\$SERVICE_TAG/$version/g" service_manifest.yml

USER assemblyline
