FROM wbgrs/php:7.2-python

WORKDIR /script

ADD main.py /script/
ADD sheets.py /script/
ADD parser /script/parser
ADD Pipfile /script/
ADD Pipfile.lock /script/

RUN ls /script/

RUN pipenv install

RUN wget https://get.symfony.com/cli/installer -O - | bash && mv /root/.symfony/bin/symfony /usr/local/bin/symfony

CMD [ "pipenv", "run", "python", "./main.py" ]
