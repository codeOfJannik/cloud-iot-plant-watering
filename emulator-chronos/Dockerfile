FROM ruby:2.6-alpine

RUN apk add --no-cache --update build-base linux-headers git tzdata

RUN mkdir /emulator
WORKDIR /emulator

COPY Gemfile /emulator/Gemfile
COPY Gemfile.lock /emulator/Gemfile.lock
RUN bundle install

EXPOSE 9292

COPY . /emulator

CMD sh -c "puma -b tcp://0.0.0.0:9292"
