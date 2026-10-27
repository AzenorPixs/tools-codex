# Design

## Context

PLLM consumes `tfl.json` for provider candidates and currently validates Medium
and measures every paid OpenRouter candidate. TFL currently excludes
OpenRouter models without Medium before publishing its paid catalog. The
current state and performance memory use schema 2 and six priorities.

## Goals / Non-Goals

**Goals:**

- Keep paid OpenRouter admission data driven from the complete TFL model list.
- Revalidate mode5 context and base prices against current OpenRouter metadata
  and the current BCE rate without sending a generation request.
- Route free OpenRouter candidates through the existing streaming benchmark
  and Medium validation path.
- Preserve the current Go behaviors and move DeepSeek’s existing behavior to 7.

**Non-Goals:**

- Changing the 0.20 EUR/M ceiling, context threshold, free performance limits,
  account privacy settings, provider credentials, installation or scheduling.
- Refreshing the published TFL catalog with live provider calls as part of this
  source change.

## Decisions

1. **Keep paid and free OpenRouter admission separate.** TFL retains all paid
   entries passing context, price, modality and LM filters even without an
   effort declaration. TFL continues to require Medium and successful free
   performance qualification for free entries. This keeps mode5 metadata only
   and prevents mode6 from consuming unqualified free candidates.
2. **Recheck mode5’s live constraints before selection.** After the required
   positive credit check, PLLM reads the current model catalog and BCE rate,
   revalidates context and native prices, then sorts eligible paid candidates
   by current EUR average with stable TFL tie order. It records unavailable
   performance as null and `not_required`; it never calls generation.
3. **Use seven-policy schema 3.** Schema 1/2 migrations retain compatible Go
   history, reset the old measured OpenRouter mode5, create a new free OpenRouter
   mode6 and move DeepSeek history/memory to mode7. Prior selection is cleared.
   Mode5 performance memory is discarded because the mode no longer benchmarks.
4. **Preserve the historical OpenRouter secret.** Modes5/6 use the existing
   `policy=mode3/provider=openrouter` reference. Mode6 treats its category as
   free and skips credits; mode5 checks credits. No credential is moved or
   created.

## Risks / Trade-offs

- **Mode5 does not prove that account guardrails allow generation.** It is a
  metadata eligibility policy by request. Provider privacy and access rules may
  still reject later use; mode5 reports no performance or route qualification.
- **A stale TFL file can omit newly eligible paid models.** A subsequent TFL
  collection is needed to refresh the source catalog; this change does not
  regenerate provider data.
- **Old schema data could imply a stale selected model.** Migration clears
  selection and marks historical rows unvisited until the new invocation
  evaluates them.

## Migration Plan

1. Update OpenSpec requirements and the TFL/PLLM implementations.
2. Migrate generated PLLM state and performance memory to schema 3 without
   carrying old mode5 performance results.
3. Synchronize autonomous and embedded skills, command wrappers, documentation,
   package version and all six plugin manifests.
4. Validate offline and archive this change. A later authorized TFL run refreshes
   the model catalog; no profile installation or remote publication is part of
   this SCM change.
