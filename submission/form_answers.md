# Submission form draft

## Project name
Otto Margin Desk

## One-line summary
An autonomous margin-intelligence micro-business that uses Hermes MoA to create, sell, account for, and deliver paid restaurant margin briefs.

## What it does
Otto Margin Desk scouts public economic and social-market signals relevant to restaurant margin, synthesizes them through a Hermes MoA council, packages the result as a paid daily brief, records a checkout event, debits model/search/hosting costs under safety limits, reinvests into the next scouting cycle, and prepares delivery for the buyer.

## Why it is useful
Restaurant margin leaders do not need more dashboards; they need concise, decision-ready margin signals. Otto turns scattered public data into a paid executive brief with specific procurement/pricing actions.

## Why it is viable
The demo uses durable primitives: Hermes Agent, MoA, public data pulls, Stripe-style test checkout events, a treasury ledger, static publishing, and prepared gateway delivery. The architecture can swap in real Stripe test/live keys and scheduled cron without changing the business loop.

## How it uses MoA
The corrected council uses GPT-5.5 as Reference 1, GLM 5.2 Cloud as Reference 2, and GPT-5.5 as Aggregator. The references review different signal interpretations; the aggregator resolves contradictions and writes the final customer-facing paid brief.

## Safety controls
No proprietary data. No live spend without human approval. Per-cycle spend caps. If a live Stripe key is detected, object creation is blocked. If no test key is present, the demo uses a signed local Stripe-style test event and labels it honestly.

## Repository / demo URL
https://kcemate.github.io/otto-margin-desk/

## X post URL
[paste final X post URL]
