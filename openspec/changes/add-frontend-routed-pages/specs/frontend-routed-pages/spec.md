## ADDED Requirements

### Requirement: Route-based page shell

Frontend SHALL provide route-based pages inside the application shell.

#### Scenario: 顯示首頁 route

- **WHEN** 使用者開啟 `/`
- **THEN** frontend SHALL render the app shell
- **AND** frontend SHALL render the home page content inside the main content area

#### Scenario: 顯示 PDF Analyze route

- **WHEN** 使用者開啟 `/analyze`
- **THEN** frontend SHALL render the app shell
- **AND** frontend SHALL render a `PDF Analyze` page inside the main content area

#### Scenario: 顯示 PDF Modify route

- **WHEN** 使用者開啟 `/modify`
- **THEN** frontend SHALL render the app shell
- **AND** frontend SHALL render a `PDF Modify` page inside the main content area

#### Scenario: 顯示 Setting route

- **WHEN** 使用者開啟 `/settings`
- **THEN** frontend SHALL render the app shell
- **AND** frontend SHALL render a `Setting` page inside the main content area

### Requirement: Sidebar route navigation

Frontend SHALL use sidebar navigation items to navigate between route-based pages.

#### Scenario: 點擊 PDF Analyze navigation

- **WHEN** 使用者點擊 sidebar 的 `PDF Analyze`
- **THEN** browser SHALL navigate to `/analyze`
- **AND** frontend SHALL render the `PDF Analyze` page

#### Scenario: 點擊 PDF Modify navigation

- **WHEN** 使用者點擊 sidebar 的 `PDF Modify`
- **THEN** browser SHALL navigate to `/modify`
- **AND** frontend SHALL render the `PDF Modify` page

#### Scenario: 點擊 Setting navigation

- **WHEN** 使用者點擊 sidebar 的 `Setting`
- **THEN** browser SHALL navigate to `/settings`
- **AND** frontend SHALL render the `Setting` page

### Requirement: Route-aware active navigation

Frontend SHALL visually mark the sidebar item that corresponds to the current route.

#### Scenario: PDF Analyze active state

- **WHEN** 使用者位於 `/analyze`
- **THEN** sidebar SHALL mark `PDF Analyze` as the active navigation item

#### Scenario: PDF Modify active state

- **WHEN** 使用者位於 `/modify`
- **THEN** sidebar SHALL mark `PDF Modify` as the active navigation item

#### Scenario: Setting active state

- **WHEN** 使用者位於 `/settings`
- **THEN** sidebar SHALL mark `Setting` as the active navigation item

#### Scenario: Home active state

- **WHEN** 使用者位於 `/`
- **THEN** sidebar SHALL mark the home page navigation item as active when a home navigation item is present

### Requirement: Home page health status

The `/` home page SHALL call `/api/health` and render backend service status.

#### Scenario: 首頁載入 health status

- **WHEN** 使用者開啟 `/`
- **THEN** frontend SHALL call `/api/health`
- **AND** frontend SHALL render backend service status from the health response or an error state when unavailable

#### Scenario: 其他頁面不顯示首頁 health panel

- **WHEN** 使用者開啟 `/analyze`
- **THEN** frontend SHALL render the `PDF Analyze` page
- **AND** frontend SHALL NOT render the home page health status panel as the main page content
