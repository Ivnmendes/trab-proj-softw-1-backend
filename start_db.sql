CREATE DATABASE farmacia_db;
CREATE USER farmacia_user WITH PASSWORD 'sua_senha_segura';

ALTER ROLE farmacia_user SET client_encoding TO 'utf8';
ALTER ROLE farmacia_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE farmacia_user SET timezone TO 'America/Sao_Paulo';

GRANT ALL PRIVILEGES ON DATABASE farmacia_db TO farmacia_user;

\c farmacia_db
GRANT ALL ON SCHEMA public TO farmacia_user;