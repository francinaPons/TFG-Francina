FROM python:3.7-alpine
RUN apk --update add --no-cache \
    lapack-dev \
    python3-dev gcc \
    freetype-dev \
    jpeg-dev zlib-dev libjpeg \
    gfortran musl-dev \
    ffmpeg

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

RUN apk add make automake gcc g++ subversion python3-dev
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:80", "app:app", "--timeout 20000"]
