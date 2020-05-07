FROM python:3.7-alpine
LABEL MAINTAINER="Edward <https://t.me/TheEdward>"
# WORKDIR /app
COPY . /app
RUN	apk add tzdata && \
	apk add curl && \
	cp /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
	echo "Europe/Moscow" >  /etc/timezone && \
	pip install -r /app/requirements.txt && \
	chmod +x /app/main.py
CMD ["/app/main.py"]
