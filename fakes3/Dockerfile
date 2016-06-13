FROM ruby:2.1.4
MAINTAINER Steven Jack <stevenmajack@gmail.com>

RUN mkdir -p /var/data/fake-s3 /usr/src/app
WORKDIR /usr/src/app

RUN git clone https://github.com/mark2997/fake-s3.git
WORKDIR /usr/src/app/fake-s3
RUN gem build fakes3.gemspec
RUN gem install fakes3-0.1.5.2.gem

EXPOSE 4569

ENTRYPOINT ["fakes3", "--root" ,"/var/data/fake-s3", "-p", "4569"]

