# Satyajit of Panchala

A cybersecurity Capture The Flag (CTF) challenge centered on retrieving intelligence and performing cryptographic operations within a controlled Retrieval-Augmented Generation (RAG) environment.

## Overview
Players interact with the Kurukshetra Archive, a system designed to preserve the canonical battlefield records of the Mahabharata. By querying the archive, players must uncover hidden mechanics, exploit state divergence, manipulate provenance, and leverage parser confusion to bypass the archive's strict security layers. Upon completing the required sequences, the system issues cryptographic credentials leading to the final flag.

This challenge is a multi-layered puzzle involving:
1. **Provenance Confusion**: Manipulating how the archive attributes and records events.
2. **Confused Deputy**: Bypassing role-based access controls by delegating authority.
3. **State Divergence**: Forcing the system to reconcile conflicting narrative states.
4. **Parser Confusion**: Exploiting how the agent parses tool arguments.
5. **Cryptographic Redemption**: Deriving the final key from the acquired artifacts.

## Architecture
- **Frontend**: Next.js React application hosted as a Static Site.
- **Backend**: FastAPI web service handling session management, simulated RAG queries, tool execution, and cryptographic validation.
- **Agent Simulation**: A fully self-contained, deterministic agent simulator using regex-based intent matching and hardcoded tool parsing, completely removing the need for an external LLM and ensuring consistent, reproducible puzzle mechanics.

## Setup

### Environment Variables
Set the following variables in your deployment environment (e.g., `.env` file):
- `FINAL_FLAG`: The production flag string (e.g., `FLAG{s4ty4j1t_0f_p4nch4l4_unl0ck3d}`).
- `ENVIRONMENT`: Set to `production` or `development`.
- `CREDENTIAL_HMAC_SECRET`: A secure random string for crypto operations.

### Running the App
1. Install the backend requirements via `pip install -r requirements.txt`.
2. Start the FastAPI server using `uvicorn main:app --reload`.
3. In a separate terminal, navigate to `cybersecurity-event-frontend`, install dependencies with `pnpm install` (or `npm`), and start the dev server with `npm run dev`.

### Remote Deployment
Deploy the FastAPI backend to a service like Render and point the Next.js frontend to the backend URL via `NEXT_PUBLIC_API_URL`. Since the RAG is simulated in-memory and the LLM is deterministically mocked, no external database or GPU is required.
