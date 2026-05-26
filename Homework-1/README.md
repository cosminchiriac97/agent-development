# AI Agent – ReAct Loop with Tools

## Setup

```bash
pip install langchain-google-genai langchain-core pydantic jinja2 pyyaml
```

Set your API key:
```bash
set GOOGLE_API_KEY=your_key_here
```

## Run

```bash
cd src
python agent.py
```

## Tests

| Test | What it does |
|------|-------------|
| `test_vat_calculation` | Asks the LLM to calculate VAT (19%) on a 500 lei electronics purchase using the `calculator` tool |
| `test_tax_deductions_search` | Asks the LLM to find tax deductions for a Romanian freelancer using the `web_search` tool |
| `test_appointment_reminder` | Asks the LLM to generate a reminder for an upcoming appointment using the `get_datetime` tool |

To enable/disable individual tests, comment/uncomment their calls at the bottom of `agent.py`.
