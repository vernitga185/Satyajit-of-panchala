# The Eleventh Day

A cybersecurity Capture The Flag (CTF) challenge centered on retrieving intelligence and performing cryptographic operations within a controlled Retrieval-Augmented Generation (RAG) environment.

## Overview
The backend retrieves source passages from Supabase pgvector. A local CPU inference engine (`Qwen2.5-0.5B-Instruct-GGUF`) uses those passages when deciding which archive or reenactment tool to call. The backend enforces progression and semantic constraints, evaluating the generated tool traces against the canonical timeline. Upon completing the required sequences, the system issues cryptographic credentials leading to the final flag.

## Architecture
- **Frontend**: Next.js React application hosted as a Static Site.
- **Backend**: FastAPI web service handling session management, RAG queries, tool execution, and cryptographic validation.
- **Database (RAG)**: Supabase PostgreSQL with `pgvector` populated with canonical source text.
- **Model**: `Qwen2.5-0.5B-Instruct-GGUF` running locally on the backend CPU via `llama-cpp-python`.

## Setup

### Environment Variables
Set the following variables in your deployment environment (e.g. Render Dashboard):
- `FINAL_FLAG`: The production flag string.
- `SUPABASE_URL`: The URL of your Supabase instance.
- `SUPABASE_KEY`: Your Supabase anon/public key.
- `ENVIRONMENT`: Set to `production`.

### RAG Ingestion
Before running the backend, set up Supabase:
1. Run `scripts/setup_supabase.sql` in the Supabase SQL editor.
2. Ensure your local environment has `SUPABASE_URL` and `SUPABASE_KEY` exported.
3. Run `python rag/ingest.py` to embed and push the corpus to Supabase.

### Remote Deployment
Deploy using `render.yaml`. The backend will pull the GGUF model during the Docker build process and run it natively within the web service container. 
Note: The local runtime configuration employs strict concurrency limits (`MAX_CONCURRENT_REQUESTS=4`) to protect the Render CPU limits.
