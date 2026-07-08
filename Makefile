runb:
	cd aiprac_data && ./.venv/bin/uvicorn main:app

resetdb:
	sudo -u postgres psql -c "DROP DATABASE IF EXISTS aiprac;"
	sudo -u postgres psql -c "CREATE DATABASE aiprac;"
	sudo -u postgres psql -d aiprac -c "ALTER DATABASE aiprac OWNER TO aiuser;"

setup:
	@echo "Creating Python virtual environment..."
	cd aiprac_data && uv sync
	@echo "Creating template .env files..."
	cp backendenv.example ./aiprac_data/.env
	@echo "Creating database..."
	sudo -u postgres psql -f ./dbsetup.sql
	@echo "Setup Complete"