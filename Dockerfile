FROM php:8.2-apache

# Install ekstensi PDO SQLite yang dibutuhkan sistem repositori
RUN apt-get update && apt-get install -y libsqlite3-dev \
    && docker-php-ext-install pdo_sqlite

# Aktifkan mod_rewrite Apache
RUN a2enmod rewrite

# Set working directory
WORKDIR /var/www/html

# Salin file proyek ke dalam container
COPY . /var/www/html

# Pastikan Apache bisa menulis ke folder server (untuk database SQLite)
RUN chown -R www-data:www-data /var/www/html/
