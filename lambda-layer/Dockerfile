# base lambda image
FROM public.ecr.aws/sam/build-python3.9

#
# versions
#

ARG KUBECTL_VERSION=1.21.0 
ARG HELM_VERSION=3.9.2

USER root
RUN mkdir -p /opt
WORKDIR /tmp

#
# tools
#

RUN yum update -y \
    && yum install -y zip unzip wget tar gzip

#
# aws cli
#

RUN python -m pip install awscli -t /opt/awscli

# organize for self-contained usage
RUN mv /opt/awscli/bin/aws /opt/awscli

# cleanup
RUN rm -rf \
    /opt/awscli/pip* \
    /opt/awscli/setuptools* \
    /opt/awscli/awscli/examples

#
# kubectl
#

RUN mkdir -p /opt/kubectl
RUN cd /opt/kubectl && curl -LO "https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl"
RUN chmod +x /opt/kubectl/kubectl

#
# helm
#

RUN mkdir -p /tmp/helm && wget -qO- https://get.helm.sh/helm-v${HELM_VERSION}-linux-amd64.tar.gz | tar -xvz -C /tmp/helm
RUN mkdir -p /opt/helm && cp /tmp/helm/linux-amd64/helm /opt/helm/helm

#
# create the bundle
#

RUN cd /opt \
    && zip --symlinks -r ../layer.zip * \
    && echo "/layer.zip is ready" \
    && ls -alh /layer.zip;

WORKDIR /
