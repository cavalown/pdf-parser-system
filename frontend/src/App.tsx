import { useCallback, useEffect, useState } from 'react'
import './App.css'

type HealthStatus = {
  alive: boolean
  status: string
  service: string
  checkedAt: string
}

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [health, setHealth] = useState<HealthStatus | null>(null)
  const [isChecking, setIsChecking] = useState(true)
  const [healthError, setHealthError] = useState('')

  const fetchHealth = useCallback(async () => {
    const response = await fetch('/api/health')

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`)
    }

    return response.json() as Promise<HealthStatus>
  }, [])

  const checkHealth = useCallback(async () => {
    setIsChecking(true)
    setHealthError('')

    try {
      setHealth(await fetchHealth())
    } catch (error) {
      setHealth(null)
      setHealthError(error instanceof Error ? error.message : 'Unknown error')
    } finally {
      setIsChecking(false)
    }
  }, [fetchHealth])

  useEffect(() => {
    let isActive = true

    fetchHealth()
      .then((nextHealth) => {
        if (isActive) {
          setHealth(nextHealth)
        }
      })
      .catch((error: unknown) => {
        if (isActive) {
          setHealth(null)
          setHealthError(error instanceof Error ? error.message : 'Unknown error')
        }
      })
      .finally(() => {
        if (isActive) {
          setIsChecking(false)
        }
      })

    return () => {
      isActive = false
    }
  }, [fetchHealth])

  const healthState = health?.alive ? 'online' : 'offline'

  return (
    <div className={`app-shell ${sidebarOpen ? 'sidebar-open' : 'sidebar-collapsed'}`}>
      <header className="top-navbar">
        <div className="navbar-left">
          <button
            type="button"
            className="icon-button menu-toggle"
            aria-label={sidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
            aria-expanded={sidebarOpen}
            onClick={() => setSidebarOpen((isOpen) => !isOpen)}
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
          <a className="brand-link" href="/" aria-label="PDF Fac. home">
            PDF Fac.
          </a>
        </div>
      </header>

      <aside className="sidebar" aria-label="Primary navigation">
        <nav className="nav-list">
          <a className="nav-item active" href="#service" aria-label="PDF Analyze" data-label="PDF Analyze">
            <span className="nav-icon" aria-hidden="true">
              A
            </span>
            <span className="nav-text">PDF Analyze</span>
          </a>
          <a className="nav-item" href="#documents" aria-label="PDF Modify" data-label="PDF Modify">
            <span className="nav-icon" aria-hidden="true">
              M
            </span>
            <span className="nav-text">PDF Modify</span>
          </a>
          <a className="nav-item" href="#settings" aria-label="Setting" data-label="Setting">
            <span className="nav-icon" aria-hidden="true">
              S
            </span>
            <span className="nav-text">Setting</span>
          </a>
        </nav>
      </aside>

      <main className="main-content">
        <header className="page-header">
          <div>
            <p className="eyebrow">Dashboard</p>
            <h1>PDF Fac.</h1>
            <p className="header-copy">首頁會即時檢查後端服務是否仍然存活。</p>
          </div>
          <button type="button" className="refresh-button" onClick={() => void checkHealth()} disabled={isChecking}>
            {isChecking ? '檢查中' : '重新檢查'}
          </button>
        </header>

        <section className="status-panel" id="service" aria-live="polite">
          <div className="status-heading">
            <span className={`status-dot ${healthState}`}></span>
            <div>
              <h2>後端連線狀態</h2>
              <p>{health?.service ?? 'pdf-parser-system-api'}</p>
            </div>
          </div>

          <div className="status-value">
            {isChecking ? 'Checking' : health?.alive ? 'Alive' : 'Offline'}
          </div>

          <dl className="status-grid">
            <div>
              <dt>API</dt>
              <dd>/api/health</dd>
            </div>
            <div>
              <dt>Status</dt>
              <dd>{health?.status ?? (healthError ? 'error' : '-')}</dd>
            </div>
            <div>
              <dt>Checked At</dt>
              <dd>{health?.checkedAt ? new Date(health.checkedAt).toLocaleString() : '-'}</dd>
            </div>
          </dl>

          {healthError && <p className="error-message">連線失敗：{healthError}</p>}
        </section>

        <section className="work-area" id="documents">
          <div>
            <h2>文件處理工作區</h2>
            <p>側邊欄可收合；只剩 icon 時，滑過項目會顯示功能名稱。</p>
          </div>
          <div className="placeholder-grid" aria-hidden="true">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </section>

        <section className="settings-anchor" id="settings" aria-label="Settings"></section>
      </main>
    </div>
  )
}

export default App
