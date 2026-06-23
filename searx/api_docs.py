# SPDX-License-Identifier: AGPL-3.0-or-later
"""
API Documentation and OpenAPI/Swagger Support for SearXNG
"""

from typing import Dict, List, Any


OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "SearXNG API",
        "description": "Privacy-focused metasearch engine API",
        "version": "1.0.0",
        "contact": {
            "name": "SearXNG",
            "url": "https://searxng.org",
            "email": "contact@searxng.org"
        },
        "license": {
            "name": "AGPL-3.0-or-later",
            "url": "https://www.gnu.org/licenses/agpl-3.0.html"
        }
    },
    "servers": [
        {
            "url": "https://api.searxng.org",
            "description": "Production server"
        }
    ],
    "paths": {
        "/search": {
            "get": {
                "summary": "Search",
                "description": "Perform a search query",
                "operationId": "search",
                "parameters": [
                    {
                        "name": "q",
                        "in": "query",
                        "description": "Search query",
                        "required": True,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "format",
                        "in": "query",
                        "description": "Response format (html, json, csv, rss)",
                        "schema": {
                            "type": "string",
                            "enum": ["html", "json", "csv", "rss"],
                            "default": "html"
                        }
                    },
                    {
                        "name": "categories",
                        "in": "query",
                        "description": "Search categories (comma-separated)",
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "language",
                        "in": "query",
                        "description": "Search language",
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "pageno",
                        "in": "query",
                        "description": "Page number",
                        "schema": {"type": "integer", "default": 1}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful search",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "results": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "title": {"type": "string"},
                                                    "url": {"type": "string"},
                                                    "content": {"type": "string"},
                                                    "engine": {"type": "string"}
                                                }
                                            }
                                        },
                                        "query": {"type": "string"},
                                        "number_of_results": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Bad request"},
                    "429": {"description": "Rate limit exceeded"},
                    "500": {"description": "Server error"}
                }
            }
        },
        "/health": {
            "get": {
                "summary": "Health Check",
                "description": "Check service health status",
                "operationId": "health",
                "responses": {
                    "200": {
                        "description": "Service is healthy",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string"},
                                        "timestamp": {"type": "string"},
                                        "uptime": {"type": "number"}
                                    }
                                }
                            }
                        }
                    },
                    "503": {"description": "Service unavailable"}
                }
            }
        },
        "/metrics": {
            "get": {
                "summary": "Metrics",
                "description": "Get performance metrics",
                "operationId": "metrics",
                "responses": {
                    "200": {
                        "description": "Metrics data",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "requests": {"type": "integer"},
                                        "error_rate": {"type": "string"},
                                        "avg_response_time": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "SearchResult": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Result title"
                    },
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "description": "Result URL"
                    },
                    "content": {
                        "type": "string",
                        "description": "Result snippet"
                    },
                    "engine": {
                        "type": "string",
                        "description": "Search engine source"
                    },
                    "score": {
                        "type": "number",
                        "description": "Result relevance score"
                    }
                },
                "required": ["title", "url", "engine"]
            },
            "SearchResponse": {
                "type": "object",
                "properties": {
                    "results": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/SearchResult"}
                    },
                    "query": {
                        "type": "string",
                        "description": "Original search query"
                    },
                    "number_of_results": {
                        "type": "integer",
                        "description": "Total number of results"
                    },
                    "response_time": {
                        "type": "number",
                        "description": "Response time in seconds"
                    }
                }
            }
        },
        "securitySchemes": {
            "apiKey": {
                "type": "apiKey",
                "in": "header",
                "name": "X-API-Key"
            }
        }
    },
    "security": [
        {"apiKey": []}
    ]
}


def get_openapi_spec() -> Dict[str, Any]:
    """Get OpenAPI specification."""
    return OPENAPI_SPEC


def get_api_documentation() -> str:
    """Get API documentation in Markdown format."""
    return """
# SearXNG API Documentation

## Overview
SearXNG provides a privacy-focused metasearch API that aggregates results from multiple search engines.

## Authentication
API requests can optionally include an API key via the `X-API-Key` header.

## Endpoints

### Search
**GET /search**

Perform a search query.

#### Parameters
- `q` (required): Search query string
- `format` (optional): Response format (html, json, csv, rss). Default: html
- `categories` (optional): Comma-separated list of categories
- `language` (optional): Search language code
- `pageno` (optional): Page number. Default: 1

#### Example Request
```
GET /search?q=python&format=json&pageno=1
```

#### Example Response
```json
{
  "results": [
    {
      "title": "Python.org",
      "url": "https://www.python.org",
      "content": "Official Python website",
      "engine": "google",
      "score": 0.95
    }
  ],
  "query": "python",
  "number_of_results": 1000000,
  "response_time": 0.234
}
```

### Health Check
**GET /health**

Check service health status.

#### Example Response
```json
{
  "status": "UP",
  "timestamp": "2026-06-23T11:00:00Z",
  "uptime": 86400
}
```

### Metrics
**GET /metrics**

Get performance metrics.

#### Example Response
```json
{
  "requests_last_hour": 1234,
  "error_rate": "0.12%",
  "avg_response_time_ms": "234.56",
  "p95_response_time_ms": "456.78",
  "p99_response_time_ms": "789.01"
}
```

## Rate Limiting
- 60 requests per minute per IP
- 1000 requests per hour per IP
- Burst limit: 10 requests

Rate limit information is included in response headers:
- `X-RateLimit-Limit`: Request limit
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Reset time (Unix timestamp)

## Response Formats

### JSON
Returns results as JSON object.

### CSV
Returns results as CSV file.

### RSS
Returns results as RSS feed.

### HTML
Returns results as HTML page (default).

## Error Handling

### 400 Bad Request
Invalid parameters or malformed request.

### 429 Too Many Requests
Rate limit exceeded.

### 500 Internal Server Error
Server error occurred.

## Best Practices

1. **Use appropriate format**: Choose JSON for API integration, HTML for web browsers
2. **Respect rate limits**: Implement exponential backoff for retries
3. **Cache results**: Use caching to reduce API calls
4. **Handle errors**: Implement proper error handling for all responses
5. **User-Agent**: Include a descriptive User-Agent header

## Examples

### Python
```python
import requests

response = requests.get('https://api.searxng.org/search', params={
    'q': 'python programming',
    'format': 'json'
})

results = response.json()
for result in results['results']:
    print(f"{result['title']}: {result['url']}")
```

### JavaScript
```javascript
fetch('https://api.searxng.org/search?q=javascript&format=json')
  .then(response => response.json())
  .then(data => {
    data.results.forEach(result => {
      console.log(`${result.title}: ${result.url}`);
    });
  });
```

### cURL
```bash
curl 'https://api.searxng.org/search?q=curl&format=json'
```

## Support
For issues and questions, visit https://github.com/searxng/searxng
"""


def get_api_endpoints() -> List[Dict[str, str]]:
    """Get list of API endpoints."""
    return [
        {
            "method": "GET",
            "path": "/search",
            "description": "Perform a search query"
        },
        {
            "method": "GET",
            "path": "/health",
            "description": "Check service health"
        },
        {
            "method": "GET",
            "path": "/metrics",
            "description": "Get performance metrics"
        },
        {
            "method": "GET",
            "path": "/api/docs",
            "description": "Get API documentation"
        }
    ]

