FROM node:6.10.1

RUN mkdir /src;  
WORKDIR /src  
# COPY ../../src/package.json /usr/src/app/
# RUN npm install && npm cache clean
# COPY ../../src/ /usr/src/app

# CMD [ "npm", "start" ]