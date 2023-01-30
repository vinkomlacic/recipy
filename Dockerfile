# image and basic system set up
FROM python:3.9-slim
LABEL authors="Vinko Mlacic <vinkomlacic@outlook.com>"
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# args
# directories must end with a slash
ARG PROJECT_DIR=/opt/recipy/

# system packages
RUN apt-get update
RUN apt-get install git -y
RUN apt-get install gcc -y
RUN apt-get install pip -y
RUN pip install uwsgi

# SSH stuff
#ADD docker/docker.key /root/.ssh/id_rsa
#RUN ssh-keyscan gitlab.com >> /root/.ssh/known_hosts
#RUN chmod 600 /root/.ssh/id_rsa
#RUN touch /root/.ssh/known_hosts

# create the user
RUN addgroup recipy --gid 2001
RUN adduser recipy --disabled-password --gecos "Recipy" --home /home/recipy --gid 2001 --uid 2001

# copy checklist source
COPY . $PROJECT_DIR

# give ownership to the default user
RUN chown -R recipy:recipy $PROJECT_DIR

# install the requirements
RUN pip install --no-cache-dir --upgrade -r $PROJECT_DIR/requirements.txt

# we store the credentials and repository url in the pip.conf
COPY pip.conf /root/.pip/pip.conf
RUN chmod 0600 /root/.pip/pip.conf

# set the environment and run the container
USER recipy
WORKDIR $PROJECT_DIR
ENV PYTHONPATH=$PYTHONPATH:$PROJECT_DIR

# Start the server
CMD ["uwsgi", "--ini", "uwsgi.ini"]
