export DATABASE_URL="postgres://postgres:postgres@localhost:5432/testdb"
export AUTH0_DOMAIN="franknguyenvd.au.auth0.com"
export AUTH0_CLIENT_ID="oonR1Vxx6bPjJakLOwWqHixQJ5cisSjG"
export AUTH0_IDENTIFIER="auth"
export AUTH0_ALGORITHM="RS256"
gunicorn app:app