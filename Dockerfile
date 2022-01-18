FROM python:3.7-buster
WORKDIR /app

# Install pyppeteer depedencies
RUN apt-get update
RUN apt-get install gconf-service -y
RUN apt-get install libasound2 -y
RUN apt-get install libatk1.0-0 -y
RUN apt-get install libatk-bridge2.0-0 -y
RUN apt-get install libc6 -y
RUN apt-get install libcairo2 -y
RUN apt-get install libcups2 -y
RUN apt-get install libdbus-1-3 -y
RUN apt-get install libexpat1 -y
RUN apt-get install libfontconfig1 -y
RUN apt-get install libgcc1 -y
RUN apt-get install libgconf-2-4 -y
RUN apt-get install libgdk-pixbuf2.0-0 -y
RUN apt-get install libglib2.0-0 -y
RUN apt-get install libgtk-3-0 -y
RUN apt-get install libnspr4 -y
RUN apt-get install libpango-1.0-0 -y
RUN apt-get install libpangocairo-1.0-0 -y
RUN apt-get install libstdc++6 -y
RUN apt-get install libx11-6 -y
RUN apt-get install libx11-xcb1 -y
RUN apt-get install libxcb1 -y
RUN apt-get install libxcomposite1 -y
RUN apt-get install libxcursor1 -y
RUN apt-get install libxdamage1 -y
RUN apt-get install libxext6 -y
RUN apt-get install libxfixes3 -y
RUN apt-get install libxi6 -y
RUN apt-get install libxrandr2 -y
RUN apt-get install libxrender1 -y
RUN apt-get install libxss1 -y
RUN apt-get install libxtst6 -y
RUN apt-get install ca-certificates -y
RUN apt-get install fonts-liberation -y
RUN apt-get install libappindicator1 -y
RUN apt-get install libnss3 -y
RUN apt-get install lsb-release -y
RUN apt-get install xdg-utils -y
RUN apt-get install wget -y
RUN apt-get install libcairo-gobject2 -y
RUN apt-get install libxinerama1 -y
RUN apt-get install libgtk2.0-0 -y
RUN apt-get install libpangoft2-1.0-0 -y
RUN apt-get install libthai0 -y
RUN apt-get install libpixman-1-0 -y
RUN apt-get install libxcb-render0 -y
RUN apt-get install libharfbuzz0b -y
RUN apt-get install libdatrie1 -y
RUN apt-get install libgraphite2-3 -y
RUN apt-get install libgbm1 -y

# Install other dependencies
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
ENTRYPOINT ["python"]
CMD ["main.py"]
