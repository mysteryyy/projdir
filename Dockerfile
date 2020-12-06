
FROM python:3.7
LABEL maintainer="yishusahil@gmail.com"


RUN apt-get update
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update && apt-get -y install google-chrome-stable --no-install-recommends
ENV CHROMEDRIVER_VERSION 87.0.4280.88
ENV ALLURE_VERSION 2.13.3

RUN wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN rm chromedriver_linux64.zip

RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod 0755 /usr/bin/chromedriver

RUN python3 -m pip  install selenium
RUN python3 -m pip install nsepy
RUN python3 -m pip install kiteconnect
RUN python3 -m pip install -U python-dotenv 



COPY trading /usr/share/app

WORKDIR /usr/share/app


ENTRYPOINT ["python","/usr/share/app/get_request_token.py"]
