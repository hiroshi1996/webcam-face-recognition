# Base python package
FROM python:3.8.10-slim-buster

# open-cv error fix
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Working directory and user
RUN useradd -ms /bin/bash myuser
USER myuser
WORKDIR /home/myuser

# Copy the dependencies
COPY --chown=myuser:myuser requirements.txt requirements.txt

# Add env path
ENV PATH="/home/myuser/.local/bin:${PATH}"

# Upgrade pip
RUN pip3 install --upgrade pip

# Install the dependencies
RUN pip3 install --user -r requirements.txt



# Copy the files
COPY --chown=myuser:myuser . .

# Executable commands
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
