import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import DashboardLayout from './layouts/DashboardLayout'
import DashboardPage from './pages/Dashboard'
import InboxPage from './pages/Inbox'
import ThreadPage from './pages/Thread'
import AnalyticsPage from './pages/Analytics'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={<DashboardLayout><DashboardPage /></DashboardLayout>} />
      <Route path="/inbox" element={<DashboardLayout><InboxPage /></DashboardLayout>} />
      <Route path="/analytics" element={<DashboardLayout><AnalyticsPage /></DashboardLayout>} />
      <Route path="/thread/:email" element={<DashboardLayout><ThreadPage /></DashboardLayout>} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}

export default App
