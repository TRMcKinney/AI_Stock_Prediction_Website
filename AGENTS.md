Repository Setup
================

Install backend dependencies with:

```
pip install -r backend/requirements.txt
```

Install frontend dependencies with:

```
npm install
```

Run tests from the repository root using:

```
pytest
```

The following environment variables must be provided, either in a `.env` file or through your environment configuration:

- `ALPHA_VANTAGE_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_KEY`

