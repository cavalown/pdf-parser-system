## ADDED Requirements

### Requirement: Dark red navbar background

Frontend SHALL render the top navbar with a dark red background color.

#### Scenario: 顯示暗紅色 navbar

- **WHEN** 使用者開啟 frontend 首頁
- **THEN** the top navbar SHALL use a dark red background color

### Requirement: Navbar menu toggle placement

Frontend SHALL display the sidebar menu icon inside the top navbar, immediately to the left of the `PDF Fac.` brand link.

#### Scenario: 顯示 navbar menu icon

- **WHEN** 使用者開啟 frontend 首頁
- **THEN** menu icon SHALL appear in the top navbar
- **AND** menu icon SHALL appear immediately before `PDF Fac.`

### Requirement: Navbar menu toggle controls sidebar

The navbar menu icon SHALL toggle the sidebar between expanded and collapsed states.

#### Scenario: 收合 sidebar

- **WHEN** sidebar is expanded
- **AND** 使用者點擊 navbar menu icon
- **THEN** sidebar SHALL collapse
- **AND** sidebar category icons SHALL remain visible

#### Scenario: 展開 sidebar

- **WHEN** sidebar is collapsed
- **AND** 使用者點擊 navbar menu icon
- **THEN** sidebar SHALL expand
- **AND** sidebar category labels SHALL be visible

### Requirement: Brand link remains home navigation

Frontend SHALL keep `PDF Fac.` as a top navbar brand link that navigates to `/`.

#### Scenario: 點擊品牌名稱

- **WHEN** 使用者點擊 top navbar 的 `PDF Fac.`
- **THEN** browser SHALL navigate to `/`

### Requirement: Sidebar remains navigation-only

Sidebar SHALL display the navigation categories `PDF Analyze`, `PDF Modify`, and `Setting` without containing a separate menu toggle control row.

#### Scenario: 顯示 sidebar 分類

- **WHEN** sidebar renders
- **THEN** sidebar SHALL display `PDF Analyze`
- **AND** sidebar SHALL display `PDF Modify`
- **AND** sidebar SHALL display `Setting`
- **AND** sidebar SHALL NOT display a separate menu toggle control row
