# Gmail Clone Backend Project
## Overview
A robust Gmail clone backend implementation built with Django, featuring real-time capabilities, advanced search, and automated mail management.

## Features
### Mail Management
- ✉️ Complete email CRUD operations
- 📁 Smart categorization (inbox, sent, starred, spam, trash)
- 🔍 Full-text search powered by Elasticsearch
- 🗑️ Automatic cleanup of 30-day-old deleted emails

### Authentication & Security
- 🔐 JWT-based authentication
- 🔒 WebSocket security with token authentication
- 👥 Role-based access control
- 🎯 Custom spam rules and filters configuration


## Tech Stack
### Core Technologies
- Framework : Django & Django REST Framework
- Authentication : Simple JWT
- Documentation : Swagger/OpenAPI
### Storage & Caching
- Database : PostgreSQL
- Cache & Messaging : Redis
- Search Engine : Elasticsearch
### Task Processing
- Async Tasks : Celery
- Scheduled Tasks : Celery Beat
### Infrastructure
- Containerization : Docker & Docker Compose
- Web Server : Nginx
- Services :
  - Web Application
  - Celery Worker
  - Celery Beat
  - PostgreSQL Database
  - Redis Cache
  - Elasticsearch Engine
  - Nginx Proxy
## API Endpoints
**Mail Operations**
- `GET /mail/get/v1/inbox/` - List inbox emails
- `GET /mail/get/v1/star/` - List starred emails
- `GET /mail/get/v1/delete/` - List deleted emails
- `GET /mail/get/v1/spam/` - List spam emails
- `GET /mail/get/v1/sent/` - List sent emails
- `GET /mail/get/v1/mail/{id}/` - Get specific email
- `POST /mail/create/v1/` - Create new email
- `PATCH /mail/update/v1/star/` - Star/unstar email
- `PATCH /mail/update/v1/read/` - Mark email as read
- `GET /mail/search/v1/` - Search emails

### Development Setup
1. Clone the repository
2. Run `docker-compose up`
3. Access the API at `http://localhost/`
4. API documentation available at `http://localhost/__docs__/v1/`
### Testing
- Comprehensive test suite for all API endpoints
- Test coverage for mail operations, search, and authentication
- Automated testing with proper test isolation