FROM mysql:8.0

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=stocks
ENV MYSQL_USER=stockuser
ENV MYSQL_PASSWORD=stockpass

# Copy init SQL script into container
COPY init.sql /docker-entrypoint-initdb.d/
