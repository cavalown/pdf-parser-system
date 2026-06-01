# Backend Capability: 服務存活 Endpoint

## ADDED Requirements

### Requirement: Health endpoint

Backend SHALL expose a NestJS controller route for `GET /api/health` that returns service liveness metadata.

#### Scenario: 呼叫 health endpoint

- **GIVEN** NestJS application has global prefix `api`
- **WHEN** a client sends `GET /api/health`
- **THEN** `AppController` SHALL handle the request
- **AND** `AppService` SHALL return a response containing `alive`, `status`, `service`, and `checkedAt`

### Requirement: Health response timestamp

Backend SHALL include the health check evaluation time in `checkedAt` using ISO 8601 format.

#### Scenario: 取得檢查時間

- **GIVEN** backend API server 正常運作
- **WHEN** a client sends `GET /api/health`
- **THEN** response body `checkedAt` SHALL be an ISO 8601 timestamp string representing the request handling time

