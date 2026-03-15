import { Outlet, NavLink } from 'react-router-dom'
import { Mail, Inbox, Bot } from 'lucide-react'

export default function Layout() {
  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-gray-200">
          <Bot className="w-6 h-6 text-blue-600 mr-2" />
          <span className="text-lg font-bold text-gray-900">Support AI Agent</span>
        </div>
        
        <nav className="flex-1 py-4">
          <ul className="space-y-1">
            <li>
              <NavLink
                to="/test"
                className={({ isActive }) =>
                  `flex items-center px-6 py-3 text-sm font-medium ${
                    isActive 
                      ? 'bg-blue-50 text-blue-700 border-r-4 border-blue-700' 
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`
                }
              >
                <Mail className="w-5 h-5 mr-3" />
                Test Email
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/inbox"
                className={({ isActive }) =>
                  `flex items-center px-6 py-3 text-sm font-medium ${
                    isActive 
                      ? 'bg-blue-50 text-blue-700 border-r-4 border-blue-700' 
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`
                }
              >
                <Inbox className="w-5 h-5 mr-3" />
                Inbox Monitoring
              </NavLink>
            </li>
          </ul>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8 max-w-7xl mx-auto">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
