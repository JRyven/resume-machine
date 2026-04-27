---
project_name: [PROJECT_NAME]
title: API Template
description: Copy-paste template for API endpoint documentation.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [api, template, documentation, endpoints]
---

# [API_NAME] API

**Path:** Documentation > API > [API_NAME] API

Base URL: `https://api.example.com/v1`

## Authentication

All requests require an API key in the `Authorization` header:

```
Authorization: Bearer [API_KEY]
```

Obtain your API key by [HOW_TO_GET_API_KEY]

## Errors

The API uses standard HTTP status codes. Error responses include:

```json
{
  "error": "[ERROR_CODE]",
  "message": "[HUMAN_READABLE_ERROR_MESSAGE]"
}
```

**Common Status Codes:**

- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (missing/invalid API key)
- `403` - Forbidden (permission denied)
- `404` - Not Found
- `500` - Internal Server Error

---

## GET /[RESOURCE]

Retrieve a list of [RESOURCE_PLURAL].

### Query Parameters

| Parameter | Type    | Required | Description                                                              |
| --------- | ------- | -------- | ------------------------------------------------------------------------ |
| `limit`   | integer | No       | Maximum number of results (default: `20`, max: `100`)                    |
| `offset`  | integer | No       | Number of results to skip for pagination (default: `0`)                  |
| `sort`    | string  | No       | Sort by field: `[FIELD_ONE]`, `[FIELD_TWO]`, `-[FIELD_ONE]` (descending) |

### Response

**Status:** 200 OK

```json
{
  "items": [
    {
      "id": "[RESOURCE_ID]",
      "[FIELD_ONE]": "[FIELD_VALUE]",
      "[FIELD_TWO]": "[FIELD_VALUE]"
    }
  ],
  "total": 150,
  "limit": 20,
  "offset": 0
}
```

### Example

```bash
curl -X GET "https://api.example.com/v1/[RESOURCE]?limit=10&sort=-created" \
  -H "Authorization: Bearer [API_KEY]"
```

---

## POST /[RESOURCE]

Create a new [RESOURCE_SINGULAR].

### Request Body

```json
{
  "[REQUIRED_FIELD]": "[FIELD_VALUE]",
  "[OPTIONAL_FIELD]": "[FIELD_VALUE]"
}
```

### Response

**Status:** 201 Created

```json
{
  "id": "[NEW_RESOURCE_ID]",
  "[FIELD_ONE]": "[FIELD_VALUE]",
  "[FIELD_TWO]": "[FIELD_VALUE]",
  "created": "[ISO_TIMESTAMP]"
}
```

### Example

```bash
curl -X POST "https://api.example.com/v1/[RESOURCE]" \
  -H "Authorization: Bearer [API_KEY]" \
  -H "Content-Type: application/json" \
  -d '{
    "[REQUIRED_FIELD]": "[VALUE]",
    "[OPTIONAL_FIELD]": "[VALUE]"
  }'
```

---

## GET /[RESOURCE]/[RESOURCE_ID]

Retrieve a specific [RESOURCE_SINGULAR] by ID.

### Path Parameters

| Parameter       | Type   | Description                                      |
| --------------- | ------ | ------------------------------------------------ |
| `[RESOURCE_ID]` | string | The unique identifier of the [RESOURCE_SINGULAR] |

### Response

**Status:** 200 OK

```json
{
  "id": "[RESOURCE_ID]",
  "[FIELD_ONE]": "[FIELD_VALUE]",
  "[FIELD_TWO]": "[FIELD_VALUE]",
  "created": "[ISO_TIMESTAMP]",
  "updated": "[ISO_TIMESTAMP]"
}
```

### Example

```bash
curl -X GET "https://api.example.com/v1/[RESOURCE]/[RESOURCE_ID]" \
  -H "Authorization: Bearer [API_KEY]"
```

---

## PUT /[RESOURCE]/[RESOURCE_ID]

Update a [RESOURCE_SINGULAR].

### Request Body

```json
{
  "[FIELD_ONE]": "[NEW_VALUE]",
  "[FIELD_TWO]": "[NEW_VALUE]"
}
```

Only include fields you want to update.

### Response

**Status:** 200 OK

```json
{
  "id": "[RESOURCE_ID]",
  "[FIELD_ONE]": "[UPDATED_VALUE]",
  "[FIELD_TWO]": "[UPDATED_VALUE]",
  "updated": "[ISO_TIMESTAMP]"
}
```

---

## DELETE /[RESOURCE]/[RESOURCE_ID]

Delete a [RESOURCE_SINGULAR].

### Response

**Status:** 204 No Content

---

## Rate Limiting

API requests are rate limited to `[REQUESTS_PER_UNIT]` requests per `[TIME_UNIT]`.

Headers indicate your current limit status:

- `X-RateLimit-Limit`: Total requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Unix timestamp when limit resets
