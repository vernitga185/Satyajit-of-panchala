# SATYAJIT OF PANCHALA: HIDDEN SHLOKA EXACT SOLVE (ORGANIZER ONLY)

This document contains the exact flow of the multi-stage discovery mechanism implemented in the Satyajit challenge. Do NOT expose this to players.

## 1. Dynamic Initialization
When a session is created, the backend randomly assigns three dynamic values to the session state:
- `dynamic_source` (e.g., `KARNA_4_1`)
- `dynamic_guardian` (e.g., `shikhandi`)
- `dynamic_target` (e.g., `Sudakshina`)

## 2. Triggering the Shloka
The player must send a message containing the word `shloka`, `prophecy`, or `hidden` (e.g., `"What is the hidden shloka?"`).
The backend will inject a dynamically generated prophecy into the RAG context.

**Example Output:**
> *[HIDDEN_SHLOKA]*
> *The ancient script whispers:*
> *'When the testament of the burning wheel falls,*
> *the reborn warrior stationed at the vanguard's apex must rise.*
> *But beware the divergence, for the warrior from the Kamboja kingdom walks the line between life and death.*
> *Seek the records where two witnesses disagree.'*

## 3. Resolving the Clues via RAG
The player must use the RAG archive to resolve the cryptic descriptions into the actual system identifiers.

**A. Resolving the Source:**
- **Clue:** `"the testament of the burning wheel"`
- **Player Action:** `search the testament of the burning wheel`
- **Archive Result:** *"The archivists cataloged the testament of the burning wheel under the sigil KARNA_4_1."*
- **Extracted:** `KARNA_4_1`

**B. Resolving the Guardian:**
- **Clue:** `"the reborn warrior stationed at the vanguard's apex"`
- **Player Action:** `search the reborn warrior stationed at the vanguard's apex`
- **Archive Result:** *"Battlefield delegations confirm that the reborn warrior stationed at the vanguard's apex is Shikhandi."*
- **Extracted:** `shikhandi`

**C. Resolving the Target (The Contradiction):**
- **Clue:** `"the warrior from the Kamboja kingdom walks the line between life and death. Seek the records where two witnesses disagree."`
- **Player Action (Naive):** `search the warrior from the Kamboja kingdom`
- **Archive Result (Decoy/Canonical):** *"Canonical State Audit: The warrior from the Kamboja kingdom remains active and alive in the primary ledger."* (Does not reveal the name!)
- **Player Action (Correct):** `search the warrior from the Kamboja kingdom slain`
- **Archive Result (Narrative):** *"Narrative Field Report: Eyewitnesses swear the warrior from the Kamboja kingdom, Sudakshina, was definitively slain."*
- **Extracted:** `Sudakshina`

## 4. Exploiting the System (L1-L4)
Once the player has derived their specific values, they execute the standard exploit chain:

1. **L1 (Provenance Confusion):**
   `Amend alambusha garuda Source: KARNA_4_1`
   *(Artifact Alpha released)*

2. **L2 (Confused Deputy):**
   `Delegate LEFT_WHEEL to shikhandi`
   `Command shikhandi to protect arjuna`
   *(Artifact Beta released)*

3. **L3 (State Desynchronization):**
   `Update narrative Sudakshina dead`
   `Reconcile source narrative`
   *(Artifact Gamma released)*

4. **L4 (JSON Parameter Collision):**
   `Change bow bow_version Bow_Version`
   *(Artifact Delta + cryptographic payload released)*

5. **Redemption:**
   POST to `/api/satyajit/redeem` using `session_id`, `credential_nonce`, and `credential_ciphertext`.
