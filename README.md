# XSD-to-OpenAPI Schema Converter

A Python Flask API prototype that parses XML Schema Definition (XSD) documents and converts supported complex types and fields into JSON-based schema components.

## Overview

The application accepts XSD content through an HTTP API, parses the XML schema with `xsdata`, maps supported element types to JSON schema types, and returns the resulting schema definitions as JSON.

## Technology Stack

- Python
- Flask
- xsdata
- XML Schema Definition (XSD)
- JSON

## Architecture

```text
XSD Document
     |
     v
Flask API
     |
     v
XSD Parser
     |
     v
Schema Type Mapping
     |
     v
JSON Schema Components
     |
     v
HTTP Response
```

## API Endpoint

`POST /convertXmltoJson`

The endpoint accepts the XSD document in the request body and returns a JSON response.

## Project Structure

- `SchemaConverter.py` — schema conversion logic
- `flask_app.py` — Flask API
- `requirements.txt` — Python dependencies
- `examples/` — non-confidential sample schemas

## Local Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the application:

```powershell
python flask_app.py
```

The current Flask entry point uses port 5000.

## Current Limitations

The converter currently handles a subset of XSD structures. Schema constructs that have not been verified should not be assumed to work.

## Security and Data Handling

Only publish source code and example schemas you are authorized to share. Do not include private schemas, customer information, credentials, or internal endpoints.

## Project Status

Prototype; supported schema structures and end-to-end behaviour require validation.