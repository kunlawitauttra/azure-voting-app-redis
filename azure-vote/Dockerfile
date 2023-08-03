# Use the Python 3.6 image with uWSGI and Nginx
FROM tiangolo/uwsgi-nginx-flask:python3.6

# Set the working directory
WORKDIR /app

# Copy the application files to the container
COPY app.py /app
COPY templates /app/templates
COPY static /app/static
COPY config_file.cfg /app

# Install pymssql to connect to Azure SQL Database
RUN pip install pymssql

# Expose ports
EXPOSE 80

# Set environment variables
ENV PORT 80
ENV PATH ${PATH}:/home/site/wwwroot

# Supervisor will call into /opt/startup/init_container.sh
# Also see: http://blog.trifork.com/2014/03/11/using-supervisor-with-docker-to-manage-processes-supporting-image-inheritance/
CMD ["python", "app.py"]
