import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import TestEmailPage from './pages/TestEmailPage'
import InboxPage from './pages/InboxPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/test" replace />} />
        <Route path="test" element={<TestEmailPage />} />
        <Route path="inbox" element={<InboxPage />} />
      </Route>
    </Routes>
  )
}

export default App
