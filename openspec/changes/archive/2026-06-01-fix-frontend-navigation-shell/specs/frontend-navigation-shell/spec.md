## ADDED Requirements

### Requirement: Top navbar brand link

Frontend SHALL display the system name `PDF Fac.` in a top navbar aligned to the upper-left side of the application, and the brand text SHALL link to the home page `/`.

#### Scenario: 顯示 navbar 系統名稱

- **WHEN** 使用者開啟 frontend 首頁
- **THEN** the top navbar SHALL display `PDF Fac.` on the upper-left side of the application

#### Scenario: 點擊 navbar 系統名稱回首頁

- **WHEN** 使用者點擊 top navbar 的 `PDF Fac.`
- **THEN** browser SHALL navigate to `/`

### Requirement: Sidebar toggle placement

Frontend SHALL place the sidebar menu icon below the system name area and align it to the right edge of the sidebar.

#### Scenario: 顯示 menu icon 位置

- **WHEN** 使用者開啟 frontend 首頁
- **THEN** the sidebar menu icon SHALL appear below the top navbar system name area
- **AND** the sidebar menu icon SHALL align to the right edge of the sidebar

### Requirement: Sidebar categories

Frontend SHALL display sidebar navigation categories `PDF Analyze`, `PDF Modify`, and `Setting`.

#### Scenario: 顯示 expanded sidebar 分類

- **WHEN** sidebar renders in expanded state
- **THEN** sidebar SHALL display `PDF Analyze`
- **AND** sidebar SHALL display `PDF Modify`
- **AND** sidebar SHALL display `Setting`

### Requirement: Collapsible sidebar behavior

Frontend SHALL allow users to toggle the sidebar between expanded and collapsed states with the menu icon button.

#### Scenario: 收合 sidebar

- **WHEN** 使用者點擊 menu icon button while sidebar is expanded
- **THEN** sidebar SHALL collapse
- **AND** sidebar category text labels SHALL no longer be visibly rendered in the sidebar rail
- **AND** sidebar category icons SHALL remain visible

#### Scenario: 展開 sidebar

- **WHEN** 使用者點擊 menu icon button while sidebar is collapsed
- **THEN** sidebar SHALL expand
- **AND** sidebar category text labels SHALL be visible

### Requirement: Collapsed sidebar labels

When sidebar is collapsed, frontend SHALL show the corresponding category label when a category icon receives hover or keyboard focus.

#### Scenario: Hover collapsed category icon

- **WHEN** 使用者 hover a collapsed sidebar category icon
- **THEN** frontend SHALL display the corresponding category label

#### Scenario: Focus collapsed category icon

- **WHEN** a collapsed sidebar category icon receives keyboard focus
- **THEN** frontend SHALL display the corresponding category label

### Requirement: Existing home health status remains available

Frontend SHALL preserve the existing home page backend health check behavior while updating the navigation shell.

#### Scenario: 首頁仍顯示 health status

- **WHEN** 使用者開啟 frontend 首頁
- **THEN** frontend SHALL call `/api/health`
- **AND** frontend SHALL render backend service status from the health response or an error state when unavailable
