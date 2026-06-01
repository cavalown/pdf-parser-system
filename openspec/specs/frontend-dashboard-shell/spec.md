## Requirements

### Requirement: Collapsible sidebar

Frontend SHALL provide a left sidebar that can be toggled between expanded and collapsed states using a menu icon button in the top navbar.

#### Scenario: Menu icon position

- **GIVEN** 使用者開啟 frontend 首頁
- **WHEN** app shell renders
- **THEN** menu icon button SHALL appear inside the top navbar
- **AND** menu icon button SHALL appear immediately before `PDF Fac.`

#### Scenario: 收合 sidebar

- **GIVEN** 使用者位於首頁
- **WHEN** 使用者點擊 menu icon button
- **THEN** sidebar SHALL collapse
- **AND** navigation items SHALL show icons without visible text labels

#### Scenario: 展開 sidebar

- **GIVEN** sidebar 已收合
- **WHEN** 使用者再次點擊 menu icon button
- **THEN** sidebar SHALL expand
- **AND** navigation item text labels SHALL be visible

### Requirement: Collapsed sidebar item labels

When sidebar is collapsed, frontend SHALL show each navigation item's label on hover or keyboard focus.

#### Scenario: Hover collapsed nav item

- **GIVEN** sidebar 已收合
- **WHEN** 使用者 hover navigation icon
- **THEN** frontend SHALL display the navigation label near the icon

#### Scenario: Focus collapsed nav item

- **GIVEN** sidebar 已收合
- **WHEN** navigation item receives keyboard focus
- **THEN** frontend SHALL display the navigation label near the icon

### Requirement: Top navbar system home link

Frontend SHALL display the system name `PDF Fac.` in a top navbar aligned to the upper-left side of the application, and link it to the home page.

#### Scenario: 點擊系統名稱

- **GIVEN** 使用者看見 top navbar 左上方的 `PDF Fac.`
- **WHEN** 使用者點擊系統名稱
- **THEN** browser SHALL navigate to `/`

### Requirement: Sidebar navigation categories

Frontend SHALL display sidebar navigation categories for `PDF Analyze`, `PDF Modify`, and `Setting`.

#### Scenario: 顯示 sidebar 分類

- **GIVEN** 使用者開啟 frontend 首頁
- **WHEN** sidebar renders in expanded state
- **THEN** sidebar SHALL display `PDF Analyze`
- **AND** sidebar SHALL display `PDF Modify`
- **AND** sidebar SHALL display `Setting`

#### Scenario: 收合後顯示分類 labels

- **GIVEN** sidebar 已收合
- **WHEN** 使用者 hover 或 focus 任一 sidebar category icon
- **THEN** frontend SHALL display the corresponding category label from `PDF Analyze`, `PDF Modify`, or `Setting`

### Requirement: Red and black design system

Frontend SHALL use red and black as the base design system colors for the application shell and status dashboard.

#### Scenario: 顯示首頁

- **GIVEN** 使用者開啟 frontend 首頁
- **WHEN** the app shell renders
- **THEN** the visual design SHALL use black or near-black surfaces
- **AND** primary actions and active states SHALL use red accent color

### Requirement: Home page health status

Frontend home page SHALL call `/api/health` and render backend service status.

#### Scenario: Health API 回傳 alive

- **GIVEN** backend health API returns `alive: true`
- **WHEN** 首頁完成 health check request
- **THEN** frontend SHALL display an alive or online state
- **AND** frontend SHALL show service metadata from the response

#### Scenario: Health API 呼叫失敗

- **GIVEN** backend health API is unreachable or returns a non-2xx response
- **WHEN** 首頁 performs the health check request
- **THEN** frontend SHALL display an offline or error state
- **AND** frontend SHALL show an error message
