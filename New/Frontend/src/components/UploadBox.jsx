import React, { useState, useRef } from 'react';
import { uploadPDF, listDocuments } from '../services/api';
import { Upload, FileText, CheckCircle, XCircle, Loader, Trash2 } from 'lucide-react';

const UploadBox = ({ onUploadSuccess, documents, setDocuments }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    
    if (!file.name.endsWith('.pdf')) {
      setError('Please upload a PDF file');
      return;
    }
    
    setUploading(true);
    setUploadProgress(0);
    setError(null);
    setUploadStatus(null);
    
    try {
      const result = await uploadPDF(file, (progress) => {
        setUploadProgress(progress);
      });
      
      setUploadStatus('success');
      setUploadProgress(100);
      
      // Refresh document list
      const docs = await listDocuments();
      setDocuments(docs.documents);
      
      if (onUploadSuccess) {
        onUploadSuccess(result);
      }
      
      // Clear file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      
      // Clear status after 3 seconds
      setTimeout(() => {
        setUploadStatus(null);
        setUploadProgress(0);
      }, 3000);
      
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.response?.data?.detail || 'Upload failed');
      setUploadStatus('error');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
        <Upload className="w-5 h-5 text-blue-600" />
        Upload Documents
      </h2>
      
      <div className="space-y-4">
        {/* Upload Area */}
        <div
          className={`border-2 border-dashed rounded-lg p-6 text-center transition-all
            ${uploading ? 'border-blue-400 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50'}`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
            disabled={uploading}
            className="hidden"
            id="pdf-upload"
          />
          <label
            htmlFor="pdf-upload"
            className="cursor-pointer block"
          >
            <Upload className="w-12 h-12 text-gray-400 mx-auto mb-3" />
            <p className="text-gray-600 mb-2">
              {uploading ? 'Uploading...' : 'Click to upload or drag and drop'}
            </p>
            <p className="text-sm text-gray-500">PDF files only (Max 10MB)</p>
          </label>
        </div>
        
        {/* Progress Bar */}
        {uploading && (
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-gray-600">
              <span>Uploading...</span>
              <span>{uploadProgress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          </div>
        )}
        
        {/* Status Message */}
        {uploadStatus === 'success' && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-3 flex items-center gap-2 text-green-700">
            <CheckCircle className="w-5 h-5" />
            <span>PDF uploaded and indexed successfully!</span>
          </div>
        )}
        
        {uploadStatus === 'error' && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 flex items-center gap-2 text-red-700">
            <XCircle className="w-5 h-5" />
            <span>{error}</span>
          </div>
        )}
        
        {/* Document List */}
        {documents && documents.length > 0 && (
          <div className="border-t border-gray-200 pt-4">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Indexed Documents</h3>
            <div className="space-y-2">
              {documents.map((doc, idx) => (
                <DocumentItem key={idx} document={doc} setDocuments={setDocuments} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const DocumentItem = ({ document, setDocuments }) => {
  const [deleting, setDeleting] = useState(false);
  
  const handleDelete = async () => {
    if (!confirm(`Delete "${document}"?`)) return;
    
    setDeleting(true);
    try {
      await deleteDocument(document);
      const docs = await listDocuments();
      setDocuments(docs.documents);
    } catch (err) {
      console.error('Delete error:', err);
      alert('Failed to delete document');
    } finally {
      setDeleting(false);
    }
  };
  
  return (
    <div className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
      <div className="flex items-center gap-2">
        <FileText className="w-4 h-4 text-gray-500" />
        <span className="text-sm text-gray-700">{document}</span>
      </div>
      <button
        onClick={handleDelete}
        disabled={deleting}
        className="text-red-600 hover:text-red-700 transition-colors"
      >
        <Trash2 className="w-4 h-4" />
      </button>
    </div>
  );
};

export default UploadBox;