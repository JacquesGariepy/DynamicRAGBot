import React, { useState, useEffect } from 'react';
import { getDocuments, addDocument, deleteDocument } from '../services/documentService';

function DocumentManagement() {
    const [documents, setDocuments] = useState([]);
    const [newDocument, setNewDocument] = useState({ content: '', metadata: '' });

    useEffect(() => {
        fetchDocuments();
    }, []);

    const fetchDocuments = async () => {
        try {
            const fetchedDocuments = await getDocuments();
            setDocuments(fetchedDocuments);
        } catch (error) {
            console.error('Error fetching documents:', error);
        }
    };

    const handleAddDocument = async () => {
        try {
            const metadata = JSON.parse(newDocument.metadata);
            await addDocument(newDocument.content, metadata);
            setNewDocument({ content: '', metadata: '' });
            fetchDocuments();
        } catch (error) {
            console.error('Error adding document:', error);
        }
    };

    const handleDeleteDocument = async (documentId) => {
        try {
            await deleteDocument(documentId);
            fetchDocuments();
        } catch (error) {
            console.error('Error deleting document:', error);
        }
    };

    return (
        <div>
            <h1>Document Management</h1>
            <div>
                <textarea
                    value={newDocument.content}
                    onChange={(e) => setNewDocument({ ...newDocument, content: e.target.value })}
                    placeholder="Document Content"
                />
                <textarea
                    value={newDocument.metadata}
                    onChange={(e) => setNewDocument({ ...newDocument, metadata: e.target.value })}
                    placeholder="Document Metadata (JSON)"
                />
                <button onClick={handleAddDocument}>Add Document</button>
            </div>
            <ul>
                {documents.map(doc => (
                    <li key={doc.id}>
                        {doc.content.substring(0, 50)}...
                        <button onClick={() => handleDeleteDocument(doc.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default DocumentManagement;