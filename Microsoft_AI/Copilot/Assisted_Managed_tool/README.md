# Copilot Assisted Order Management Tool

## Overview

The Copilot Assisted Order Management Tool is an AI-powered solution on Microsoft Power Platform that streamlines order processing with a Canvas App and a Copilot Studio bot connected to Dataverse. It reduces manual work with guided workflows and conversational actions for create, read, update, and delete operations on orders.

## Architecture

[See Architecture](./docs/architecture.en.svg)

## Repository Structure

```
.
├─ docs/
│  └─ architecture.svg
├─ orders.xlsx                  # Optional sample data
├─ solutions/
│  └─ New_app_manamegent_tool_v2/
│     ├─ botcomponent_connectionreferenceset/
│     ├─ botcomponent_dvtablesearchset/
│     ├─ botcomponent_workflowset/
│     ├─ botcomponents/
│     ├─ bots/
│     ├─ canvasapps/
│     ├─ dvtablesearchentities/
│     ├─ dvtablesearchs/
│     ├─ entities/
│     ├─ modernflows/
│     └─ publishers/
├─ README.md
└─ README.es.md
```

### Solution Contents (summary)

- botcomponents/bots: Copilot Studio topics and assets for the agent `schema_Agent_order_management__06eaaaf3`.
- botcomponent_connectionreferenceset: Connection references for Dataverse CRUD actions (Create/Get/List/Update/Delete).
- botcomponent_dvtablesearchset: DVT table search configuration (e.g., new order discovery topic).
- botcomponent_workflowset: Workflow/action `create_new_order_flow_v2` used by the bot.
- canvasapps: Canvas app artifacts for order management UI.
- entities, dvtablesearchentities, dvtablesearchs, modernflows, publishers: Dataverse tables, search entities, flows, and publisher metadata.

## Features

- Intelligent order processing with Copilot-guided actions
- Automated workflow for order lifecycle management
- Natural-language interface (Copilot Studio)
- Real-time status tracking in Dataverse

## Prerequisites

- Power Platform environment with Dataverse
- Power Platform CLI (pac)
- Appropriate licenses for Power Apps/Dataverse/Copilot Studio

## Get Started (pack and import)

This repository contains the unpacked solution under `solutions/New_app_manamegent_tool_v2`. To deploy it to an environment, pack it into a solution .zip and then import.

1) Install or verify pac CLI
```cmd
pac --version
```

2) Authenticate to your environment
```cmd
pac auth create --url https://<your-env>.crm.dynamics.com --name DEV
pac auth select --name DEV
```

3) Pack the solution from source
```cmd
:: Unmanaged (editable in target)
pac solution pack --zipfile out\New_app_manamegent_tool_v2_unmanaged.zip --folder solutions\New_app_manamegent_tool_v2 --packagetype Unmanaged

:: Managed (locked for Prod)
pac solution pack --zipfile out\New_app_manamegent_tool_v2_managed.zip --folder solutions\New_app_manamegent_tool_v2 --packagetype Managed
```

4) Import the solution
```cmd
:: Choose one of the produced zip files
pac solution import --path out\New_app_manamegent_tool_v2_unmanaged.zip --publish-changes
```

5) Resolve connection references and share the app/bot as needed via Maker Portal.

## Data seeding (optional)

- Use `orders.xlsx` to seed initial data via Dataverse import (Maker Portal > Data > Tables > Import).

## Operations and ALM

- Export managed solution for Test/Prod
```cmd
pac solution export --name <SolutionUniqueName> --managed true --path out\Solution_Managed.zip
```
- Run solution checker
```cmd
pac solution checker run --solution-name <SolutionDisplayName>
```

## Troubleshooting

- Connection references unresolved: assign to valid Dataverse connections after import.
- Bot topics not triggering: review intents and topics in Copilot Studio, and verify actions point to the right tables.
- Dataverse permission errors: ensure appropriate security roles on order tables.

## Documentation

- Architecture (original): ./docs/architecture.svg
- Architecture (English): ./docs/architecture.en.svg
- Spanish guide: ./README.es.md
- Power Platform docs: https://learn.microsoft.com/power-platform/
- Microsoft 365 Developer Program (FAQ): https://learn.microsoft.com/en-us/office/developer-program/microsoft-365-developer-program-faq
- Copilot Studio requirements/licensing: https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing-subscriptions

## Version History

- 2025-09-19: Added summary and steps for `solutions/New_app_manamegent_tool_v2`; linked architecture diagram; cleaned sections.

---

Last Updated: 2025-09-19