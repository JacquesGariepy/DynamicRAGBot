import React, { useState } from 'react';
import { queryRAG } from '../services/ragService';

function RAGInterface() {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await queryRAG(question);
            setAnswer(response);
        } catch (error) {
            console.error('Error querying RAG:', error);
            setAnswer('An error occurred while processing your question.');
        }
    };

    return (
        <div>
            <h1>RAG Interface</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask a question"
                />
                <button type="submit">Submit</button>
            </form>
            {answer && (
                <div>
                    <h2>Answer:</h2>
                    <p>{answer}</p>
                </div>
            )}
        </div>
    );
}

export default RAGInterface;