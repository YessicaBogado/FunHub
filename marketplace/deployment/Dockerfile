# docker build -t functionhub .

# TODO: repeat CMD line also in OpenShift deployment
# TODO: otherwise, start 'nginx' and 'mon.sh' manually after deployment

FROM nginx:stable-alpine

COPY app /usr/share/nginx/html
# COPY generator /opt/generator/
# COPY custom/gen.sh custom/mon.sh /opt/generator/

RUN rm -rf /opt/functions
# RUN mkdir /opt/functions-local

RUN touch /usr/share/nginx/html/api/sensors/functions
RUN chmod 775 /usr/lib/nginx /var/log/nginx /run /usr/share/nginx/html/api/sensors
RUN chmod 666 /var/log/nginx/* /usr/share/nginx/html/api/sensors/functions
RUN sed -i -e "s/80/10080/" /etc/nginx/conf.d/default.conf

EXPOSE 10080

WORKDIR /opt

ENV PYTHONPATH=/usr/lib/python3/dist-packages

CMD ["sh", "-c", "nginx && tail -f /dev/null"]
