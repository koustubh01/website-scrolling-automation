FROM umihico/aws-lambda-selenium-python:latest as build-image

COPY website2.py .

COPY requirements3.txt .

RUN pip install \
        awslambdaric

# Install FFmpeg
RUN yum install sudo -y
RUN sudo yum install libwayland-client
RUN sudo yum install wget -y
RUN sudo yum install tar -y
RUN sudo yum install xz -y


RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
RUN sudo tar xf ffmpeg-release-amd64-static.tar.xz


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements3.txt

COPY website5.py .

CMD ["website5.handler"]