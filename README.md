# Otto Margin Desk

Contest build for the Nous Research x NVIDIA x Stripe **Hermes Agent Accelerated Business Hackathon**.

Otto Margin Desk is an autonomous business-intelligence micro-operation for restaurant and supply-chain margin leaders. It scouts public margin signals, synthesizes them through a Hermes MoA council, packages the result as a paid executive brief, records revenue/spend in a treasury ledger, and prepares delivery to a buyer.

## Demo loop

1. `fetch_market_data.py` pulls public economic data from FRED.
2. `run_moa_brief.py` invokes Hermes MoA (`otto`) to produce the paid brief.
3. `run_business_ops.py` simulates/executes the Stripe test-mode business loop and writes a treasury ledger.
4. `render_site.py` renders the public landing page/demo dashboard.
5. `run_full_cycle.py` executes the full cycle end-to-end.

## Verified MoA role setup

- Reference 1: `openai-codex:gpt-5.5`
- Reference 2: `ollama-launch:glm-5.2:cloud`
- Aggregator: `openai-codex:gpt-5.5`

## Safety

Public-data only. No CFA/private data. No live spending without explicit approval. If `STRIPE_SECRET_KEY` is missing or not test-mode, the demo uses a local signed Stripe-style test event and marks it honestly in the UI.
