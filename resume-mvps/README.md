# Resume MVPs — Yubraj Chaulagain

Synthetic portfolio demonstrations aligned with the supplied resume. No employer or customer data is included.

## Customer Service RAG Agent
`apps/voice-agent` demonstrates grounded customer context, a visibly simulated call lifecycle, time-zone-aware availability, persisted bookings, and slot-contention rejection. It makes no calls or messages.

## Media ETL Pipeline
`apps/media-etl` runs a deterministic 500-row synthetic normalization job with invalid-row quarantine, casing normalization, exact duplicate handling, count reconciliation, source-row lineage, and CSV export. `services/media_etl` provides the matching Python clean-room pipeline.

## Verify
```bash
npm install
npm test
npm run build
python -m pytest services/media_etl/tests
```

Provider adapters and the n8n workflow contain credential references only. They are not evidence of a live Vapi or Google Sheets test.

Yubraj Chaulagain · [GitHub](https://github.com/nceeg01) · [LinkedIn](https://linkedin.com/in/yubrajchaulagain03)
