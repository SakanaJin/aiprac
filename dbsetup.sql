DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'aiuser') THEN
    CREATE USER aiuser WITH ENCRYPTED PASSWORD 'password';
  END IF;
END
$$;

SELECT 'CREATE DATABASE aiprac OWNER aiuser'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'aiprac')\gexec

ALTER DATABASE aiprac OWNER TO aiuser;

\c aiprac

GRANT ALL ON SCHEMA public TO aiuser;