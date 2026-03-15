import { useState, useEffect } from 'react'
import axios from 'axios'
import { format } from 'date-fns'
import { X, Search, Filter } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1/agent'

export default function InboxPage() {
  const [emails, setEmails] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedEmailId, setSelectedEmailId] = useState(null)
  const [emailDetails, setEmailDetails] = useState(null)
  const [detailsLoading, setDetailsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [filterMode, setFilterMode] = useState('all') // 'all', 'human', 'auto'

  // Fetch all emails on mount
  useEffect(() => {
    const fetchInbox = async () => {
      try {
        const res = await axios.get(`${API_URL}/inbox`)
        setEmails(res.data.emails)
        setError(null)
      } catch (err) {
        console.error("Failed to fetch inbox", err)
        setError("Failed to load inbox data. Please check your connection.")
      } finally {
        setLoading(false)
      }
    }
    fetchInbox()
  }, [])

  // Fetch specific email details when row clicked
  const handleRowClick = async (id) => {
    setSelectedEmailId(id)
    setDetailsLoading(true)
    try {
      const res = await axios.get(`${API_URL}/email/${id}`)
      setEmailDetails(res.data)
    } catch (err) {
      console.error("Failed to fetch details", err)
    } finally {
      setDetailsLoading(false)
    }
  }

  const closePanel = () => {
    setSelectedEmailId(null)
    setEmailDetails(null)
  }

  const filteredEmails = emails.filter(email => {
    const matchesSearch = email.subject.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          email.customer_email.toLowerCase().includes(searchQuery.toLowerCase());
    
    if (filterMode === 'human' && !email.human_reviewed) return false;
    if (filterMode === 'auto' && email.human_reviewed) return false;
    
    return matchesSearch;
  });

  return (
    <div className="relative h-[calc(100vh-4rem)] flex flex-col">
      <div className="mb-6 flex items-center justify-between">
         <div>
          <h1 className="text-2xl font-bold text-gray-900">Inbox Monitoring</h1>
          <p className="text-gray-500 mt-1 text-sm">View all historical emails processed by the AI Agent.</p>
         </div>
         <div className="flex gap-2">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <input 
                type="text" 
                placeholder="Search emails..." 
                className="pl-9 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <select 
              value={filterMode}
              onChange={(e) => setFilterMode(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm text-gray-600 bg-white hover:bg-gray-50 outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Status</option>
              <option value="auto">Auto Replied</option>
              <option value="human">Human Review</option>
            </select>
         </div>
      </div>

      {/* Main Table Area */}
      <div className={`flex-1 overflow-hidden transition-all duration-300 flex border border-gray-200 rounded-xl bg-white shadow-sm ${selectedEmailId ? 'mr-96 lg:mr-[32rem]' : ''}`}>
        <div className="flex-1 overflow-auto">
          <table className="w-full text-left border-collapse">
            <thead className="bg-gray-50 sticky top-0 z-10 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Date</th>
                <th className="px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Customer</th>
                <th className="px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Subject</th>
                <th className="px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Intent</th>
                <th className="px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {loading ? (
                 <tr>
                   <td colSpan="5" className="px-6 py-8 text-center text-gray-500">
                     <div className="flex justify-center items-center gap-2">
                       <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                       Loading inbox data...
                     </div>
                   </td>
                 </tr>
              ) : error ? (
                 <tr>
                   <td colSpan="5" className="px-6 py-8 text-center text-red-500 bg-red-50">{error}</td>
                 </tr>
              ) : filteredEmails.length === 0 ? (
                 <tr>
                   <td colSpan="5" className="px-6 py-8 text-center text-gray-500">
                     {emails.length === 0 ? 'No emails processed yet. Go to Test Email to send one!' : 'No emails match your search/filter.'}
                   </td>
                 </tr>
              ) : (
                filteredEmails.map((email) => (
                  <tr 
                    key={email.id}
                    onClick={() => handleRowClick(email.id)}
                    className={`cursor-pointer transition-colors ${selectedEmailId === email.id ? 'bg-blue-50' : 'hover:bg-gray-50'}`}
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {format(new Date(email.timestamp), 'MMM d, h:mm a')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 border-r border-transparent">
                      {email.customer_email}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700 max-w-[200px] truncate">
                      {email.subject}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 capitalize">
                        {email.category}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                       <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${email.human_reviewed ? 'bg-amber-100 text-amber-800' : 'bg-green-100 text-green-800'}`}>
                         {email.human_reviewed ? 'Human Review' : 'Auto Replied'}
                       </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Side Slide-out Panel */}
      <div className={`fixed inset-y-0 right-0 w-96 lg:w-[32rem] bg-white border-l border-gray-200 shadow-2xl transform transition-transform duration-300 ease-in-out z-20 overflow-y-auto ${selectedEmailId ? 'translate-x-0' : 'translate-x-full'}`}>
        {selectedEmailId && (
          <div className="h-full flex flex-col">
            <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center bg-gray-50 sticky top-0 z-10">
              <h2 className="text-lg font-semibold text-gray-900">Email Details (ID: {selectedEmailId})</h2>
              <button onClick={closePanel} className="p-2 rounded-full hover:bg-gray-200 text-gray-500 transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="p-6 flex-1 space-y-8">
              {detailsLoading ? (
                <div className="flex justify-center py-12"><div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div></div>
              ) : emailDetails ? (
                <>
                  {/* Original Email */}
                  <section>
                    <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Original Request</h3>
                    <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 space-y-2">
                       <p className="text-sm"><span className="font-semibold text-gray-700">From:</span> {emailDetails.customer_email}</p>
                       <p className="text-sm"><span className="font-semibold text-gray-700">Subject:</span> {emailDetails.subject}</p>
                       <div className="mt-4 pt-4 border-t border-gray-200">
                         <p className="text-sm text-gray-800 whitespace-pre-wrap">{emailDetails.body}</p>
                       </div>
                    </div>
                  </section>

                   {/* Agent Context */}
                   <section>
                    <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">LangGraph Context</h3>
                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div className="bg-blue-50 p-3 rounded-lg border border-blue-100">
                         <p className="text-xs text-blue-600 font-semibold">Intent Classified</p>
                         <p className="text-sm font-medium text-gray-900 capitalize mt-1">{emailDetails.category}</p>
                      </div>
                      <div className={`p-3 rounded-lg border ${emailDetails.human_reviewed ? 'bg-amber-50 border-amber-100' : 'bg-green-50 border-green-100'}`}>
                         <p className={`text-xs font-semibold ${emailDetails.human_reviewed ? 'text-amber-600' : 'text-green-600'}`}>Routing Target</p>
                         <p className="text-sm font-medium text-gray-900 mt-1">{emailDetails.human_reviewed ? 'Human Escalation' : 'Automated Dispatch'}</p>
                      </div>
                    </div>
                    
                    <div className="bg-gray-900 p-4 rounded-lg border border-gray-800 mt-2">
                      <p className="text-xs text-gray-400 font-mono mb-2">// Retrieved FAISS Knowledge Base Documents</p>
                      <p className="text-xs text-gray-300 font-mono whitespace-pre-wrap leading-relaxed">{emailDetails.kb_info || 'No documents matched.'}</p>
                    </div>
                  </section>

                  {/* Final Output */}
                  <section>
                    <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Final Generated Draft</h3>
                    <div className="bg-white p-4 rounded-lg border-2 border-green-200 shadow-sm text-sm text-gray-800 whitespace-pre-wrap">
                      {emailDetails.final_reply}
                    </div>
                  </section>
                </>
              ) : (
                <div className="text-center text-gray-500">Failed to load email data.</div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
