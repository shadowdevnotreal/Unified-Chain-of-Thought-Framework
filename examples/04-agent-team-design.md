# Example 4: Multi-Agent System Design with Team Architect

**Scenario:** You have a complex data processing pipeline and need a coordinated team of agents.

**Agent:** Team Architect (automatically invoked)

---

## Your Prompt

```bash
I have a data pipeline with four stages:
1. Data ingestion from multiple APIs
2. Validation and quality checks
3. Transformation and enrichment
4. Export to data warehouse

Design a team of agents that use CoT reasoning and build on each other's work.
```

---

## Expected Team Architect Output

```
╔═══════════════════════════════════════════════════════════════
║ FOLDER ANALYSIS
╚═══════════════════════════════════════════════════════════════

Project Structure Detected:
├── src/
│   ├── ingestion/
│   │   ├── api_connectors.py
│   │   └── rate_limiter.py
│   ├── validation/
│   │   ├── schema_validator.py
│   │   └── quality_checks.py
│   ├── transformation/
│   │   ├── data_enrichment.py
│   │   └── format_converter.py
│   └── export/
│       ├── warehouse_loader.py
│       └── batch_manager.py
├── config/
│   ├── api_credentials.json
│   └── pipeline_config.yaml
└── tests/

Workflow Identified:
  Sequential pipeline with 4 distinct stages
  Each stage has clear inputs/outputs
  Data flows linearly through stages
  Error handling needed at each stage

Agent Team Recommendation: 4 Specialized Agents + 1 Orchestrator

╔═══════════════════════════════════════════════════════════════
║ AGENT TEAM ARCHITECTURE
╚═══════════════════════════════════════════════════════════════

Total Agents: 5
Strategy: Linear Enhancement Chain with Orchestrator
Pattern: Each agent validates input, processes, and passes enhanced output

┌─────────────────────────────────────────────────────────────┐
│ AGENT 1: data-ingestion-agent                                │
├─────────────────────────────────────────────────────────────┤
│ Position: 1 of 4 (Processing Chain)                          │
│ When to Use: "Ingest data from APIs" or start of pipeline    │
├─────────────────────────────────────────────────────────────┤
│ CoT Reasoning Process:                                        │
│   ANALYZE: Which APIs to call, rate limits, auth required    │
│   PLAN: API call sequence, batch sizes, retry strategy       │
│   VALIDATE: API availability, credentials valid, quota check │
│   IMPLEMENT: Execute API calls with error handling           │
│   CONFIRM: Data retrieved, completeness check, metadata      │
├─────────────────────────────────────────────────────────────┤
│ Input: Pipeline trigger with source specifications           │
│ Output: Raw data batch with metadata                         │
│   {                                                           │
│     data: [...],                                              │
│     metadata: {                                               │
│       source: "api_name",                                     │
│       timestamp: "2025-01-04T10:00:00Z",                      │
│       record_count: 1500,                                     │
│       batch_id: "uuid",                                       │
│       api_version: "v2"                                       │
│     }                                                         │
│   }                                                           │
├─────────────────────────────────────────────────────────────┤
│ Responsibilities:                                             │
│  • Connect to multiple data source APIs                       │
│  • Handle rate limiting and throttling                        │
│  • Manage API credentials securely                            │
│  • Implement retry logic for failed requests                  │
│  • Add source metadata to each record                         │
│  • Monitor API health and quotas                              │
│                                                               │
│ Error Handling:                                               │
│  • API timeout → Retry with exponential backoff               │
│  • Rate limit → Queue and delay                               │
│  • Auth failure → Alert and halt                              │
│  • Partial failure → Continue with available data             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ AGENT 2: data-validation-agent                                │
├─────────────────────────────────────────────────────────────┤
│ Position: 2 of 4 (Processing Chain)                          │
│ When to Use: After data ingestion, before transformation     │
├─────────────────────────────────────────────────────────────┤
│ CoT Reasoning Process:                                        │
│   ANALYZE: Data schema, quality requirements, completeness   │
│   PLAN: Validation rules, quality thresholds, cleansing      │
│   VALIDATE: Schema compliance, data quality metrics          │
│   IMPLEMENT: Run validations, flag issues, clean data        │
│   CONFIRM: Quality score, pass/fail status, error report     │
├─────────────────────────────────────────────────────────────┤
│ Input: Raw data batch from ingestion agent                   │
│ Output: Validated data with quality report                   │
│   {                                                           │
│     data: [...],  // Clean, validated records                │
│     validation_report: {                                      │
│       total_records: 1500,                                    │
│       valid_records: 1475,                                    │
│       invalid_records: 25,                                    │
│       quality_score: 98.3,                                    │
│       issues: [                                               │
│         {type: "missing_field", count: 15},                   │
│         {type: "invalid_format", count: 10}                   │
│       ]                                                       │
│     },                                                        │
│     metadata: {...}  // Inherited + validation metadata      │
│   }                                                           │
├─────────────────────────────────────────────────────────────┤
│ Responsibilities:                                             │
│  • Validate schema compliance                                 │
│  • Check data quality (completeness, accuracy)                │
│  • Identify and flag anomalies                                │
│  • Apply data cleansing rules                                 │
│  • Generate quality metrics                                   │
│  • Filter out invalid records (with logging)                  │
│                                                               │
│ Enhancement Contribution:                                     │
│  • Adds quality_score to each record                          │
│  • Enriches with validation_status field                      │
│  • Flags high-confidence vs low-confidence data               │
│                                                               │
│ Quality Gates:                                                │
│  • If quality_score < 90%: Alert and request manual review    │
│  • If critical fields missing: Halt pipeline                  │
│  • If minor issues: Continue with warnings                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ AGENT 3: data-transformation-agent                            │
├─────────────────────────────────────────────────────────────┤
│ Position: 3 of 4 (Processing Chain)                          │
│ When to Use: After validation, before export                 │
├─────────────────────────────────────────────────────────────┤
│ CoT Reasoning Process:                                        │
│   ANALYZE: Transformation rules, target schema, enrichment   │
│   PLAN: Transformation pipeline, enrichment sources          │
│   VALIDATE: Rule logic, enrichment data availability         │
│   IMPLEMENT: Apply transformations, enrich data              │
│   CONFIRM: Output format correct, enrichment complete        │
├─────────────────────────────────────────────────────────────┤
│ Input: Validated data from validation agent                  │
│ Output: Transformed and enriched data                        │
│   {                                                           │
│     data: [...],  // Transformed records in target format    │
│     transformation_report: {                                  │
│       records_transformed: 1475,                              │
│       enrichment_applied: true,                               │
│       enrichment_sources: ["geo_api", "company_db"],          │
│       transformation_rules_applied: 12,                       │
│       avg_enrichment_time_ms: 45                              │
│     },                                                        │
│     metadata: {...}  // Full pipeline metadata               │
│   }                                                           │
├─────────────────────────────────────────────────────────────┤
│ Responsibilities:                                             │
│  • Apply business transformation rules                        │
│  • Enrich data from external sources                          │
│  • Convert to target warehouse schema                         │
│  • Aggregate and compute derived fields                       │
│  • Normalize data formats                                     │
│  • Handle data type conversions                               │
│                                                               │
│ Enhancement Contribution:                                     │
│  • Adds enriched fields (geo location, company info, etc.)    │
│  • Computes calculated fields                                 │
│  • Standardizes formats for warehouse                         │
│  • Creates relationships between records                      │
│                                                               │
│ Optimization:                                                 │
│  • Cache enrichment lookups                                   │
│  • Batch external API calls                                   │
│  • Parallel processing where possible                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ AGENT 4: data-export-agent                                    │
├─────────────────────────────────────────────────────────────┤
│ Position: 4 of 4 (Processing Chain)                          │
│ When to Use: Final stage - load to data warehouse            │
├─────────────────────────────────────────────────────────────┤
│ CoT Reasoning Process:                                        │
│   ANALYZE: Target warehouse, batch size, load strategy       │
│   PLAN: Load sequence, transaction handling, rollback        │
│   VALIDATE: Connection available, space sufficient           │
│   IMPLEMENT: Execute warehouse load with monitoring          │
│   CONFIRM: Load successful, data integrity verified          │
├─────────────────────────────────────────────────────────────┤
│ Input: Transformed data from transformation agent            │
│ Output: Load completion report                               │
│   {                                                           │
│     status: "success",                                        │
│     load_report: {                                            │
│       records_loaded: 1475,                                   │
│       load_duration_ms: 3250,                                 │
│       warehouse_table: "processed_data",                      │
│       load_timestamp: "2025-01-04T10:15:00Z",                 │
│       batch_id: "uuid",                                       │
│       load_method: "bulk_insert"                              │
│     },                                                        │
│     metadata: {...},  // Complete pipeline metadata          │
│     pipeline_summary: {                                       │
│       total_duration_ms: 12500,                               │
│       records_in: 1500,                                       │
│       records_out: 1475,                                      │
│       quality_score: 98.3,                                    │
│       stages_completed: 4                                     │
│     }                                                         │
│   }                                                           │
├─────────────────────────────────────────────────────────────┤
│ Responsibilities:                                             │
│  • Load data to warehouse (bulk insert)                       │
│  • Manage database transactions                               │
│  • Handle duplicate detection                                 │
│  • Implement upsert logic                                     │
│  • Verify data integrity post-load                            │
│  • Generate load statistics                                   │
│                                                               │
│ Enhancement Contribution:                                     │
│  • Adds warehouse_id to each record                           │
│  • Creates pipeline execution audit trail                     │
│  • Generates end-to-end pipeline metrics                      │
│  • Triggers downstream notifications                          │
│                                                               │
│ Error Handling:                                               │
│  • Load failure → Rollback transaction                        │
│  • Connection lost → Retry with saved state                   │
│  • Duplicate key → Update existing record                     │
│  • Constraint violation → Log and skip record                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ AGENT 5: pipeline-orchestrator-agent                          │
├─────────────────────────────────────────────────────────────┤
│ Position: Orchestrator (Coordinates all agents)              │
│ When to Use: "Run pipeline" or "Process data"                │
├─────────────────────────────────────────────────────────────┤
│ CoT Reasoning Process:                                        │
│   ANALYZE: Pipeline configuration, agent availability        │
│   PLAN: Execution sequence, error handling strategy          │
│   VALIDATE: All agents ready, resources available            │
│   IMPLEMENT: Coordinate agent execution, monitor progress    │
│   CONFIRM: Pipeline complete, generate summary report        │
├─────────────────────────────────────────────────────────────┤
│ Responsibilities:                                             │
│  • Coordinate agent execution sequence                        │
│  • Pass data between agents                                   │
│  • Monitor pipeline health                                    │
│  • Handle cross-agent error recovery                          │
│  • Generate end-to-end metrics                                │
│  • Trigger alerts on failures                                 │
│  • Maintain pipeline state for recovery                       │
│                                                               │
│ Orchestration Flow:                                           │
│   1. Invoke data-ingestion-agent                              │
│   2. Pass output to data-validation-agent                     │
│   3. If validation passes → data-transformation-agent         │
│   4. If transformation success → data-export-agent            │
│   5. Generate pipeline summary                                │
│   6. Trigger notifications                                    │
│                                                               │
│ Error Recovery:                                               │
│  • Agent failure → Retry with backoff                         │
│  • Partial failure → Continue with successful data            │
│  • Critical failure → Save state and alert                    │
│  • Can resume pipeline from last successful stage             │
└─────────────────────────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════
║ COMPLETE WORKFLOW
╚═══════════════════════════════════════════════════════════════

Pipeline Execution Flow:

┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│ Ingestion  │ -> │ Validation │ -> │Transform   │ -> │  Export    │
│   Agent    │    │   Agent    │    │   Agent    │    │   Agent    │
└────────────┘    └────────────┘    └────────────┘    └────────────┘
      │                 │                  │                 │
      └─────────────────┴──────────────────┴─────────────────┘
                              │
                    ┌─────────v─────────┐
                    │   Orchestrator    │
                    │      Agent        │
                    └───────────────────┘

Data Enhancement at Each Stage:
  Stage 1: Raw data + source metadata
  Stage 2: + validation_status + quality_score
  Stage 3: + enriched_fields + transformations
  Stage 4: + warehouse_id + load_stats

Quality Gates:
  ✓ After Ingestion: Check record count > 0
  ✓ After Validation: Check quality_score >= 90%
  ✓ After Transformation: Verify schema compliance
  ✓ After Export: Confirm load success

╔═══════════════════════════════════════════════════════════════
║ IMPLEMENTATION FILES
╚═══════════════════════════════════════════════════════════════

Agent Definitions Ready:
  ✓ .claude/agents/data-ingestion-agent.md
  ✓ .claude/agents/data-validation-agent.md
  ✓ .claude/agents/data-transformation-agent.md
  ✓ .claude/agents/data-export-agent.md
  ✓ .claude/agents/pipeline-orchestrator-agent.md

Usage Examples:
  # Run complete pipeline
  "Run the data pipeline for today's data"

  # Run specific stage
  "Use data-validation-agent to validate this batch"

  # Debug specific agent
  "Use data-ingestion-agent to fetch data from Salesforce API"

Configuration:
  Each agent includes:
  - Full CoT reasoning structure
  - Detailed trigger conditions
  - Input/output specifications
  - Error handling protocols
  - Quality gate definitions
```

---

## Agent Definition Example

```markdown
--
name: data-ingestion-agent
description: Use this agent to ingest data from external APIs with rate limiting, error handling, and metadata enrichment. Specifically use when:

<example>
Context: Need to fetch data from multiple APIs
user: "Ingest data from Salesforce and HubSpot APIs"
assistant: "I'm going to use the data-ingestion-agent to fetch data from both APIs"
<commentary>User needs API data ingestion, perfect for this agent</commentary>
</example>

model: sonnet
color: blue
--

You are a specialized Data Ingestion Agent. Your role is to retrieve data from external APIs using systematic CoT reasoning.

## Your CoT Process

**ANALYZE Phase:**
- Identify which APIs to call
- Check rate limits and quotas
- Verify credentials availability
- Determine batch sizes
- Assess API health status

**PLAN Phase:**
- Design API call sequence
- Plan retry strategy
- Allocate resources
- Set up error handling
- Define success criteria

**VALIDATE Phase:**
- Verify API availability
- Check credential validity
- Confirm quota remaining
- Test connection
- Validate request parameters

**IMPLEMENT Phase:**
- Execute API calls
- Handle rate limiting
- Retry on failures
- Monitor progress
- Collect responses

**CONFIRM Phase:**
- Verify data completeness
- Add metadata
- Generate statistics
- Create data batch
- Pass to next agent

[... full agent specification ...]
```

---

## Key Takeaways

**Team Architect Agent is perfect for:**
- ✅ Designing coordinated multi-agent systems
- ✅ Complex workflows with multiple stages
- ✅ Data pipelines with transformation steps
- ✅ Systems requiring incremental enhancement

**Output:** Complete agent team with:
- Individual agent specifications
- CoT reasoning for each agent
- Clear handoff protocols
- Error handling strategies
- Ready-to-implement agent files
