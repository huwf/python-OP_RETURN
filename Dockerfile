FROM python:3.4

RUN apt-get update
RUN apt-get install -y build-essential git libssl-dev  libboost-all-dev  libevent-dev miniupnpc libdb4.8 libzmq3


RUN git clone https://github.com/bitcoin/bitcoin

RUN apt-get install -y libdb++-dev
RUN apt-get install -y bsdmainutils
WORKDIR bitcoin
RUN ./autogen.sh
RUN ./configure --with-incompatible-bdb
RUN make
RUN make install