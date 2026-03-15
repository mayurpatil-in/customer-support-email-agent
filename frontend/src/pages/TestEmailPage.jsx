import { useState } from 'react'
import axios from 'axios'
import { Send, Loader2, CheckCircle2, AlertCircle, Bot } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1/agent'

export default function TestEmailPage() {
  const [formData, setFormData] = useState({
    customer_email: '',
    subject: '',
    body: ''
  })
  
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post(`${API_URL}/process-email`, formData)
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while connecting to the agent.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Test Email Simulation</h1>
        <p className="text-gray-500 mt-2">Send a mock email through the LangGraph AI Support Agent pipeline.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* INPUT FORM */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Customer Email</label>
              <input 
                type="email" 
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
                placeholder="customer@example.com"
                value={formData.customer_email}
                onChange={(e) => setFormData({...formData, customer_email: e.target.value})}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Subject</label>
              <input 
                type="text"
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
                placeholder="Help with my order"
                value={formData.subject}
                onChange={(e) => setFormData({...formData, subject: e.target.value})}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Message Body</label>
              <textarea 
                required
                rows={6}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors resize-none"
                placeholder="I received a defective item..."
                value={formData.body}
                onChange={(e) => setFormData({...formData, body: e.target.value})}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 px-4 rounded-lg flex items-center justify-center transition-colors disabled:opacity-70"
            >
              {loading ? (
                <><Loader2 className="w-5 h-5 mr-2 animate-spin" /> Processing AI Pipeline...</>
              ) : (
                <><Send className="w-5 h-5 mr-2" /> Process Email</>
              )}
            </button>
          </form>

          {error && (
            <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg flex items-start border border-red-100">
              <AlertCircle className="w-5 h-5 mr-2 flex-shrink-0 mt-0.5" />
              <p className="text-sm">{error}</p>
            </div>
          )}
        </div>

        {/* RESULTS PANEL */}
        <div className="bg-gray-50 p-6 rounded-xl border border-gray-200 h-full flex flex-col">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            Agent Output
            {result && <CheckCircle2 className="w-5 h-5 ml-2 text-green-500" />}
          </h2>
          
          {!result && !loading && (
            <div className="flex-1 flex flex-col items-center justify-center text-gray-400">
              <Bot className="w-12 h-12 mb-3 text-gray-300" />
              <p>Submit an email to view the AI reasoning.</p>
            </div>
          )}

          {loading && (
            <div className="flex-1 flex flex-col items-center justify-center text-gray-400 space-y-4">
               <div className="flex space-x-2">
                 <div className="w-3 h-3 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                 <div className="w-3 h-3 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                 <div className="w-3 h-3 bg-blue-400 rounded-full animate-bounce"></div>
               </div>
               <p className="text-sm font-medium text-blue-600">Running LangGraph Nodes...</p>
            </div>
          )}

          {result && (
            <div className="space-y-6 flex-1 overflow-auto">
              {/* Badges */}
              <div className="flex flex-wrap gap-2">
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  Intent: {result.category}
                </span>
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${result.human_reviewed ? 'bg-amber-100 text-amber-800' : 'bg-green-100 text-green-800'}`}>
                  {result.human_reviewed ? 'Human Escalated' : 'Auto Resolved'}
                </span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                  Confidence: {(result.confidence_score * 100).toFixed(0)}%
                </span>
              </div>

              {/* Draft Output */}
              <div>
                <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Final AI Draft</h3>
                <div className="bg-white p-4 rounded-lg border border-gray-200 text-sm text-gray-700 whitespace-pre-wrap">
                  {result.final_reply}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
