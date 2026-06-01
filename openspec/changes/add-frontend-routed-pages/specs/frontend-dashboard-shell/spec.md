## MODIFIED Requirements

### Requirement: Home page health status

Frontend home page at `/` SHALL call `/api/health` and render backend service status as the home page's primary content.

#### Scenario: Health API 回傳 alive

- **GIVEN** backend health API returns `alive: true`
- **WHEN** 首頁 `/` 完成 health check request
- **THEN** frontend SHALL display an alive or online state
- **AND** frontend SHALL show service metadata from the response

#### Scenario: Health API 呼叫失敗

- **GIVEN** backend health API is unreachable or returns a non-2xx response
- **WHEN** 首頁 `/` performs the health check request
- **THEN** frontend SHALL display an offline or error state
- **AND** frontend SHALL show an error message

#### Scenario: 首頁不承載其他 sidebar 頁面內容

- **WHEN** 使用者開啟首頁 `/`
- **THEN** frontend SHALL render the home health status content
- **AND** frontend SHALL NOT render `PDF Analyze`, `PDF Modify`, or `Setting` page content as part of the home page main content
