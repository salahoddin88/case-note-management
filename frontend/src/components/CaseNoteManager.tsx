'use client';

import React, { useState, useEffect } from 'react';
import { Search, Plus, User, Calendar, MessageSquare } from 'lucide-react';
import { Client, CaseNote, CaseNoteCreateRequest, INTERACTION_TYPES } from '@/types/api';
import { ApiService } from '@/services/api';

export default function CaseNoteManager() {
  const [searchQuery, setSearchQuery] = useState('');
  const [clients, setClients] = useState<Client[]>([]);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const [caseNotes, setCaseNotes] = useState<CaseNote[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [totalClients, setTotalClients] = useState(0);
  const pageSize = 10;
  
  // New case note form state
  const [newNoteContent, setNewNoteContent] = useState('');
  const [newNoteType, setNewNoteType] = useState('phone');
  const [submitting, setSubmitting] = useState(false);

  // Search clients with pagination
  const handleSearch = async (page: number = 1) => {
    setLoading(true);
    setError(null);
    
    try {
      const results = await ApiService.searchClients(searchQuery, page, pageSize);
      setClients(results.clients);
      setTotalPages(results.total_pages);
      setTotalClients(results.total);
      setCurrentPage(page);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to search clients');
    } finally {
      setLoading(false);
    }
  };

  // Load initial clients on component mount
  useEffect(() => {
    handleSearch(1);
  }, []);

  // Select a client and load their case notes
  const handleClientSelect = async (client: Client) => {
    setSelectedClient(client);
    setLoading(true);
    setError(null);
    
    try {
      const notes = await ApiService.getClientCaseNotes(client.id);
      setCaseNotes(notes);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load case notes');
    } finally {
      setLoading(false);
    }
  };

  // Create a new case note
  const handleCreateNote = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedClient || !newNoteContent.trim()) {
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const data: CaseNoteCreateRequest = {
        client_id: selectedClient.id,
        content: newNoteContent.trim(),
        interaction_type: newNoteType,
      };

      await ApiService.createCaseNote(data);
      
      // Refresh case notes
      const updatedNotes = await ApiService.getClientCaseNotes(selectedClient.id);
      setCaseNotes(updatedNotes);
      
      // Reset form
      setNewNoteContent('');
      setNewNoteType('phone');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create case note');
    } finally {
      setSubmitting(false);
    }
  };

  // Format date for display
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  // Get interaction type label
  const getInteractionLabel = (type: string) => {
    const interaction = INTERACTION_TYPES.find(t => t.value === type);
    return interaction?.label || type;
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-8 flex items-center">
          <MessageSquare className="mr-3 h-8 w-8 text-blue-600" />
          Case Note Management
        </h1>

        {/* Client Search Section */}
        <div className="mb-8">
          <div className="flex gap-4 mb-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                <input
                  type="text"
                  placeholder="Search clients by name or ID..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch(1)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
            <button
              onClick={() => handleSearch(1)}
              disabled={loading}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>

          {/* Search Results */}
          {clients.length > 0 && (
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex justify-between items-center mb-3">
                <h3 className="font-semibold text-gray-700">
                  Search Results ({totalClients} total)
                </h3>
                <div className="text-sm text-gray-500">
                  Page {currentPage} of {totalPages}
                </div>
              </div>
              <div className="space-y-2">
                {clients.map((client) => (
                  <button
                    key={client.id}
                    onClick={() => handleClientSelect(client)}
                    className={`w-full text-left p-3 rounded-lg border transition-colors ${
                      selectedClient?.id === client.id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium text-gray-900">
                          {client.first_name} {client.last_name}
                        </div>
                        <div className="text-sm text-gray-500">{client.client_id}</div>
                      </div>
                      <User className="h-5 w-5 text-gray-400" />
                    </div>
                  </button>
                ))}
              </div>
              
              {/* Pagination Controls */}
              {totalPages > 1 && (
                <div className="flex justify-center items-center mt-4 space-x-2">
                  <button
                    onClick={() => handleSearch(currentPage - 1)}
                    disabled={currentPage === 1}
                    className="px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Previous
                  </button>
                  
                  {/* Page numbers */}
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    const pageNum = Math.max(1, Math.min(totalPages - 4, currentPage - 2)) + i;
                    if (pageNum > totalPages) return null;
                    return (
                      <button
                        key={pageNum}
                        onClick={() => handleSearch(pageNum)}
                        className={`px-3 py-2 text-sm border rounded-lg ${
                          currentPage === pageNum
                            ? 'border-blue-500 bg-blue-50 text-blue-600'
                            : 'border-gray-300 hover:bg-gray-50'
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  })}
                  
                  <button
                    onClick={() => handleSearch(currentPage + 1)}
                    disabled={currentPage === totalPages}
                    className="px-3 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Next
                  </button>
                </div>
              )}
            </div>
          )}

          {/* Selected Client */}
          {selectedClient && (
            <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-semibold text-blue-900">
                    Selected: {selectedClient.first_name} {selectedClient.last_name}
                  </h3>
                  <p className="text-blue-700">{selectedClient.client_id}</p>
                </div>
                <button
                  onClick={() => {
                    setSelectedClient(null);
                    setCaseNotes([]);
                    setNewNoteContent('');
                  }}
                  className="text-blue-600 hover:text-blue-800 text-sm"
                >
                  Clear Selection
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {/* New Case Note Form */}
        {selectedClient && (
          <div className="mb-8 p-6 bg-gray-50 rounded-lg">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <Plus className="mr-2 h-5 w-5" />
              New Case Note
            </h2>
            
            <form onSubmit={handleCreateNote} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Interaction Type
                </label>
                <select
                  value={newNoteType}
                  onChange={(e) => setNewNoteType(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {INTERACTION_TYPES.map((type) => (
                    <option key={type.value} value={type.value}>
                      {type.label}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Notes
                </label>
                <textarea
                  value={newNoteContent}
                  onChange={(e) => setNewNoteContent(e.target.value)}
                  rows={4}
                  placeholder="Enter detailed notes about the client interaction..."
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  required
                />
              </div>
              
              <button
                type="submit"
                disabled={submitting || !newNoteContent.trim()}
                className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                {submitting ? 'Saving...' : 'Save Note'}
              </button>
            </form>
          </div>
        )}

        {/* Previous Case Notes */}
        {selectedClient && (
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Previous Notes</h2>
            
            {loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-2 text-gray-600">Loading case notes...</p>
              </div>
            ) : caseNotes.length > 0 ? (
              <div className="space-y-4">
                {caseNotes.map((note) => (
                  <div key={note.id} className="bg-white border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4 text-gray-400" />
                        <span className="text-sm text-gray-600">
                          {formatDate(note.created_at)}
                        </span>
                      </div>
                      <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                        {getInteractionLabel(note.interaction_type)}
                      </span>
                    </div>
                    
                    <p className="text-gray-900 mb-2">{note.content}</p>
                    
                    <div className="text-xs text-gray-500">
                      Created by: {note.created_by.name}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <MessageSquare className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>No case notes found for this client.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
} 