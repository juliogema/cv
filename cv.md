# Julio Gema

**Software Engineer**

Indonesia · juliogema.personal@gmail.com · github.com/juliogema · linkedin.com/in/juliogema

## Summary

Software engineer who builds and operates cloud services in Go for a game-backend platform, with additional experience in Java and .NET Core. Recent work covers usage-based billing and metering, concurrency controls, audit logging, and data migrations, using MongoDB, Redis, Kafka, AWS and Kubernetes. Writes tech specs and defends design decisions in review. Ships changes with code review and security review, and uses AI coding agents (Claude Code) as part of a documented, repeatable workflow.

## Skills

- **Languages:** Go, Java, C# (.NET Core), Python, SQL, Bash
- **Data and messaging:** MongoDB, Redis, Kafka (event streaming), AWS Athena
- **Cloud and infrastructure:** AWS, Kubernetes, Helm, Kustomize, Flux, Docker, secrets management (AWS Parameter Store, ExternalSecrets)
- **Backend practices:** REST and gRPC APIs, OpenAPI/Swagger, feature flags, data migrations, idempotent job design, rate limiting, audit logging, observability and log analysis
- **Engineering process:** technical specifications, design reviews, code review, security review, CI/CD, Git, Bitbucket, GitHub, Jira, Confluence
- **AI-assisted engineering:** Claude Code, custom agent skills and hooks, LLM-assisted code and security review

## Experience

### Software Engineer, AccelByte

July 2021 to Present · Remote

Cloud platform for online game backends (identity, multiplayer servers, billing).

**Billing and metering**

- Designed and built a subscription-history component in Go and MongoDB that synchronizes subscriptions to an external billing platform from the service's own data. Delivered with a tech spec, a data migration script and a pull request, after settling 19 design questions in review.
- Implemented a usage-reporting pipeline to an external usage-based billing platform for several product lines. Daily usage events are built from AWS Athena query results, and the integration runs behind a feature flag so it can be rolled out independently.
- Redesigned how a metered infrastructure resource is billed, from a fixed price to daily usage events, relying on documented vendor behaviour instead of undocumented behaviour. Settled 20 design decisions in review, then implemented the change and fixed the valid review findings.
- Built a read-only Python tool that compares monthly bills between two billing platforms item by item and guarantees it sends no write requests. On a closed month it matched plan and usage items to the cent and surfaced the few real differences for follow-up.
- Fixed a high-severity review finding in which two scheduled jobs doubled data-warehouse scans. Concurrent identical queries now share one execution (Go singleflight), covered by a unit test. This avoided a cache that would have served stale rows and kept the two jobs independent.
- Diagnosed an integration failure from worker logs (a rejected API key) and traced how rotated secrets reach running Kubernetes pods.

**Customer notifications**

- Built scheduled email notifications using an hourly worker job, a 24-hour send window, and a claim-before-send record in MongoDB to prevent duplicate emails. Added the SendGrid template, the configuration change, a database index migration and QA test steps.

**Access control and identity**

- Added a configurable concurrency limit for a subset of tenants, separate from the existing global limit. Wrote a spec with 20 edge cases, then implemented a rolling 24-hour count of distinct rejected users in a Redis sorted set, and documented a HyperLogLog alternative with its memory and accuracy trade-offs.
- Implemented audit logging for an admin configuration API across 9 endpoints through the event-streaming SDK, following the platform's existing naming and client-IP conventions. Tests cover each endpoint, user and client tokens, and failure paths, and a deliberately removed audit call is caught by the tests.
- Updated the identity service to handle new error codes from a downstream service across six login flows.
- Fixed a status endpoint that reported zero for a namespace that does not exist, by adding a cached existence check that returns 404 and fails open if the lookup service is unreachable.

**Configuration and data migration**

- Found and fixed the root cause of a bug in which null numeric limits became 0 during selective configuration export and import. Added explicit defaults that match the owning service's behaviour.

**Engineering practice**

- Runs a code review and a security review on larger changes before opening the pull request, checks each finding against the code, and fixes the valid ones. Skips findings that conflict with a recorded design decision and says why.
- Keeps a structured daily engineering log with decisions, state and next steps, written so another engineer or an AI agent can pick the work up without extra context.
- Writes specs and design docs in Confluence and answers review comments in rounds. One spec had 15 inline comments in the first round, each checked against the code before the spec was updated.

## Education

Bachelor Degree of Applied Science in Informatics Engineering, Surabaya State Polytechnic, 2021
