## 1. Frontend Setup

- [ ] 1.1 Add `react-router-dom` to frontend dependencies.
- [ ] 1.2 Update frontend routing entry so `App` renders a browser router with layout routes.

## 2. Frontend Structure

- [ ] 2.1 Create an app shell component that owns top navbar, sidebar, collapsed sidebar state, and main content layout.
- [ ] 2.2 Create focused navbar and sidebar components using the existing red/black visual pattern.
- [ ] 2.3 Create page components for `HomePage`, `PdfAnalyzePage`, `PdfModifyPage`, and `SettingPage`.
- [ ] 2.4 Move the existing `/api/health` request state and health status UI into `HomePage`.

## 3. Frontend Navigation

- [ ] 3.1 Configure `/`, `/analyze`, `/modify`, and `/settings` routes to render inside the app shell.
- [ ] 3.2 Change sidebar items from hash anchors to route links.
- [ ] 3.3 Add route-aware active styling for `PDF Analyze`, `PDF Modify`, and `Setting`.
- [ ] 3.4 Preserve sidebar expanded/collapsed behavior and collapsed hover/focus labels.
- [ ] 3.5 Ensure the `PDF Fac.` navbar brand link navigates to `/` and renders the home page.

## 4. Frontend Page Content

- [ ] 4.1 Ensure `/` renders only the home health status content as its primary page content.
- [ ] 4.2 Add clear basic empty states for `PDF Analyze`, `PDF Modify`, and `Setting` without implementing their final workflows.
- [ ] 4.3 Remove the previous homepage placeholder sections for `PDF Analyze`, `PDF Modify`, and `Setting`.

## 5. Validation

- [ ] 5.1 Run frontend lint.
- [ ] 5.2 Run frontend build.
- [ ] 5.3 Manually verify browser navigation for `/`, `/analyze`, `/modify`, and `/settings`.
- [ ] 5.4 Manually verify sidebar collapse/expand, active item styling, and collapsed hover/focus labels.
- [ ] 5.5 Manually verify `/` still calls `/api/health` and renders alive/offline/error states.
