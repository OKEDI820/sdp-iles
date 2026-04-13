import Navbar from './Navbar'
import Sidebar from './Sidebar'

export default function AppLayout({ children }) {
  return (
    <div className="app-shell">
      <Navbar />
      <div className="main-shell">
        <Sidebar />
        <main className="content">{children}</main>
      </div>
    </div>
  )
}
