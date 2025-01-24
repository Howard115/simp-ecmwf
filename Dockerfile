FROM ubuntu:24.04

# Install required packages including wget, sudo, and gnupg
RUN apt update && apt install -y cron python3 wget sudo gnupg python3-pip python3-venv

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Download and add Google's signing key
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
# Add Google Chrome repository
RUN sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# Update package list
RUN sudo apt-get update
# Install Chrome
RUN sudo apt-get install -y google-chrome-stable

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

#run it every 6 hours
COPY scrapy.py /app/scrapy.py 

COPY app.py /app/app.py
RUN python3 /app/app.py


COPY crontab /etc/cron.d/crontab
RUN chmod 644 /etc/cron.d/crontab

EXPOSE 8501

CMD ["streamlit", "run", "/app/app.py"]

