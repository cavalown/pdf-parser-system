## MODIFIED Requirements

### Requirement: Top navbar brand link

Frontend SHALL display the system name `PDF Fac.` in a top navbar aligned to the upper-left side of the application, and the brand text SHALL link to the home page `/`.

#### Scenario: 顯示 navbar 系統名稱

- **WHEN** 使用者開啟任一 frontend route
- **THEN** the top navbar SHALL display `PDF Fac.` on the upper-left side of the application

#### Scenario: 點擊 navbar 系統名稱回首頁

- **WHEN** 使用者點擊 top navbar 的 `PDF Fac.`
- **THEN** browser SHALL navigate to `/`
- **AND** frontend SHALL render the home page

### Requirement: Sidebar categories

Frontend SHALL display sidebar navigation categories `PDF Analyze`, `PDF Modify`, and `Setting`, and each category SHALL navigate to its corresponding frontend route.

#### Scenario: 顯示 expanded sidebar 分類

- **WHEN** sidebar renders in expanded state
- **THEN** sidebar SHALL display `PDF Analyze`
- **AND** sidebar SHALL display `PDF Modify`
- **AND** sidebar SHALL display `Setting`

#### Scenario: 點擊 sidebar 分類進入對應頁面

- **WHEN** 使用者點擊 sidebar 的 `PDF Analyze`
- **THEN** browser SHALL navigate to `/analyze`
- **WHEN** 使用者點擊 sidebar 的 `PDF Modify`
- **THEN** browser SHALL navigate to `/modify`
- **WHEN** 使用者點擊 sidebar 的 `Setting`
- **THEN** browser SHALL navigate to `/settings`

### Requirement: Existing home health status remains available

Frontend SHALL preserve the existing home page backend health check behavior on the `/` route while updating the navigation shell to use route navigation.

#### Scenario: 首頁仍顯示 health status

- **WHEN** 使用者開啟 frontend `/` route
- **THEN** frontend SHALL call `/api/health`
- **AND** frontend SHALL render backend service status from the health response or an error state when unavailable

### Requirement: Route-aware sidebar active state

Frontend SHALL mark the sidebar navigation category that matches the current frontend route as active.

#### Scenario: 顯示目前 route 的 active 分類

- **WHEN** 使用者位於 `/analyze`
- **THEN** sidebar SHALL mark `PDF Analyze` as active
- **WHEN** 使用者位於 `/modify`
- **THEN** sidebar SHALL mark `PDF Modify` as active
- **WHEN** 使用者位於 `/settings`
- **THEN** sidebar SHALL mark `Setting` as active
