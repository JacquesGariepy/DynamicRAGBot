import React, { useState, useEffect, useRef } from 'react';
import { sendChatMessage } from '../services/chatbotService';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isOpen, setIsOpen] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    const handleSendMessage = async () => {
        if (inputMessage.trim() === '') return;

        const newMessages = [...messages, { text: inputMessage, sender: 'user' }];
        setMessages(newMessages);
        setInputMessage('');

        try {
            const response = await sendChatMessage(inputMessage);
            setMessages([...newMessages, { text: response, sender: 'bot' }]);
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages([...newMessages, { text: 'Sorry, I encountered an error. Please try again.', sender: 'bot' }]);
        }
    };

    return (
        <div className={`chatbot ${isOpen ? 'open' : ''}`}>
            <button className="chatbot-toggle" onClick={() => setIsOpen(!isOpen)}>
                {isOpen ? 'Close Chat' : 'Open Chat'}
            </button>
            {isOpen && (
                <div className="chatbot-container">
                    <div className="chatbot-messages">
                        {messages.map((message, index) => (
                            <div key={index} className={`message ${message.sender}`}>
                                {message.text}
                            </div>
                        ))}
                        <div ref={messagesEndRef} />
                    </div>
                    <div className="chatbot-input">
                        <input
                            type="text"
                            value={inputMessage}
                            onChange={(e) => setInputMessage(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                            placeholder="Type your message here..."
                        />
                        <button onClick={handleSendMessage}>Send</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Chatbot;