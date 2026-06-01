# Shared Capability: 服務存活檢查 API Contract

## ADDED Requirements

### Requirement: Health check API contract

系統 SHALL 提供 `GET /api/health` 作為 frontend 檢查 backend 是否存活的 API contract。

#### Scenario: Backend 服務存活

- **GIVEN** backend API server 正常運作
- **WHEN** frontend 或使用者呼叫 `GET /api/health`
- **THEN** response status SHALL be `200`
- **AND** response body SHALL be JSON
- **AND** response body SHALL include `alive: true`
- **AND** response body SHALL include `status`
- **AND** response body SHALL include `service`
- **AND** response body SHALL include `checkedAt`

#### Scenario: Frontend local proxy 呼叫 health API

- **GIVEN** frontend dev server 正常運作
- **AND** backend API server 正常運作於 `http://127.0.0.1:3000`
- **WHEN** frontend 呼叫 `/api/health`
- **THEN** Vite dev proxy SHALL forward the request to backend
- **AND** frontend SHALL receive the same health check JSON response

