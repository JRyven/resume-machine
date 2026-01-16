---
project_name: [PROJECT_NAME]
title: API Specification
description: Rules for creating API documentation with endpoints, parameters, and examples.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [api, specification, documentation, endpoints, reference]
---

# API Specification

**Path:** Documentation > Writing Documentation > API Specification

API documentation describes HTTP endpoints, request/response formats, authentication, and error codes.

## Purpose

API documentation:

- Defines available endpoints and methods
- Specifies request and response formats
- Documents authentication and authorization
- Explains error codes and handling
- Provides integration examples

## Mandatory Sections

### YAML Front Matter

```yaml
---
project_name: [PROJECT_NAME]
title: [API_NAME] API Documentation
description: [BRIEF_API_DESCRIPTION]
api_version: [VERSION]
base_url: [BASE_URL_PLACEHOLDER]
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [api, [API_NAME], documentation, endpoints]
---
```

### Breadcrumb Navigation

```markdown
**Path:** Documentation > API > [API_NAME] API
```

### Authentication

Describe how to authenticate:

```markdown
## Authentication

All requests require an API key in the `Authorization` header:
```

Authorization: Bearer [API_KEY]

```

```

## Endpoint Documentation Format

### Endpoint Heading

```markdown
## [HTTP_METHOD] /[ENDPOINT_PATH]

[One-sentence description of endpoint purpose]
```

### Path Parameters

```markdown
### Path Parameters

| Parameter | Type   | Description   |
| --------- | ------ | ------------- |
| `[PARAM]` | string | [DESCRIPTION] |
| `[PARAM]` | number | [DESCRIPTION] |
```

### Query Parameters

```markdown
### Query Parameters

| Parameter | Type    | Required | Description                          |
| --------- | ------- | -------- | ------------------------------------ |
| `[PARAM]` | string  | No       | [DESCRIPTION] (default: `[DEFAULT]`) |
| `[PARAM]` | boolean | No       | [DESCRIPTION] (default: `[DEFAULT]`) |
```

### Request Body

````markdown
### Request Body

```json
{
  "[FIELD]": "[DESCRIPTION_AND_TYPE]",
  "[FIELD]": "[DESCRIPTION_AND_TYPE]"
}
```
````

````

### Response

```markdown
### Response

**Status:** 200 OK

```json
{
  "[FIELD]": "[RESPONSE_VALUE]",
  "[FIELD]": "[RESPONSE_VALUE]"
}
````

### Example

```bash
curl -X [METHOD] "[BASE_URL]/[ENDPOINT]" \
  -H "Authorization: Bearer [API_KEY]" \
  -H "Content-Type: application/json" \
  -d '{
    "[FIELD]": "[VALUE]"
  }'
```

````

### Error Responses

```markdown
**Error Response (400 Bad Request)**

```json
{
  "error": "INVALID_REQUEST",
  "message": "Missing required field: [FIELD_NAME]"
}
````

````

## Error Codes Section

```markdown
## Error Codes

| Code | Meaning | Typical Cause |
|------|---------|---------------|
| 400 | Bad Request | Invalid parameters or missing required fields |
| 401 | Unauthorized | Invalid or missing API key |
| 403 | Forbidden | API key lacks required permissions |
| 404 | Not Found | Resource does not exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Unexpected server error |
````

## Example

```markdown
# REST API Documentation

Base URL: `https://api.example.com/v1`

## Authentication

All requests require an API key:
```

Authorization: Bearer [API_KEY]

````

## POST /users

Create a new user account.

### Request Body

```json
{
  "email": "user@example.com",
  "name": "[USER_NAME]",
  "password": "[PASSWORD_HASH]"
}
````

### Response

**Status:** 201 Created

```json
{
  "id": "[USER_ID]",
  "email": "user@example.com",
  "name": "[USER_NAME]",
  "created_at": "[ISO_TIMESTAMP]"
}
```

### Example

```bash
curl -X POST "https://api.example.com/v1/users" \
  -H "Authorization: Bearer [API_KEY]" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "[USER_NAME]",
    "password": "[PASSWORD_HASH]"
  }'
```

## GET /users/[USER_ID]

Retrieve a user by ID.

### Path Parameters

| Parameter   | Type   | Description            |
| ----------- | ------ | ---------------------- |
| `[USER_ID]` | string | Unique user identifier |

### Response

**Status:** 200 OK

```json
{
  "id": "[USER_ID]",
  "email": "user@example.com",
  "name": "[USER_NAME]"
}
```

```

## Size Guidelines

- Total: 400-1000 words
- YAML: ~50 words
- Breadcrumb: 5 words
- Authentication: 30-50 words
- Per Endpoint: 100-200 words
- Error Codes: 50-100 words
```
