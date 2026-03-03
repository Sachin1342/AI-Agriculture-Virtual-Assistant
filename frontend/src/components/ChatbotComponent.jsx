import React, { useEffect, useRef, useState } from 'react';
import { FiSend, FiUpload, FiX } from 'react-icons/fi';
import { chatbotAPI } from '../api/client';

const ChatbotComponent = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: "Hello! I'm your AI agricultural assistant. How can I help you today?",
      timestamp: new Date(),
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [showImageUpload, setShowImageUpload] = useState(false);
  const [error, setError] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || loading) return;
    setError('');

    const text = inputMessage;
    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await chatbotAPI.sendMessage(text, sessionId);
      setSessionId(response.data.session_id || sessionId);

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'bot',
          text: response.data.chatbot_response,
          confidence: response.data.confidence,
          timestamp: new Date(),
        },
      ]);
    } catch (err) {
      setError(err.message);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 2,
          sender: 'bot',
          text: 'Sorry, I encountered an error. Please try again.',
          timestamp: new Date(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setError('');
    setLoading(true);

    try {
      const response = await chatbotAPI.detectDisease(file);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          sender: 'bot',
          text: `Disease: ${response.data.disease}\nConfidence: ${response.data.confidence_percentage}\n\nTreatments:\n${(response.data.treatments || []).join('\n')}`,
          data: response.data,
          timestamp: new Date(),
        },
      ]);
      setShowImageUpload(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      event.target.value = '';
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-green-50 to-blue-50">
      <div className="bg-green-600 text-white p-6 shadow-lg">
        <h1 className="text-3xl font-bold">🌾 Crop Assistant AI</h1>
        <p className="text-green-100">Your intelligent agricultural companion</p>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${msg.sender === 'user' ? 'bg-blue-500 text-white rounded-br-none' : 'bg-white text-gray-800 rounded-bl-none border border-gray-200'}`}>
              <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
              {msg.confidence ? (
                <p className="text-xs mt-1 opacity-75">Confidence: {(msg.confidence * 100).toFixed(0)}%</p>
              ) : null}
            </div>
          </div>
        ))}
        {loading ? <p className="text-sm text-gray-500">Processing...</p> : null}
        {error ? <p className="text-sm text-red-600">{error}</p> : null}
        <div ref={messagesEndRef} />
      </div>

      {showImageUpload ? (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4 shadow-xl">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-800">Upload Leaf Image</h2>
              <button onClick={() => setShowImageUpload(false)} className="text-gray-500 hover:text-gray-700">
                <FiX size={20} />
              </button>
            </div>
            <div className="border-2 border-dashed border-green-300 rounded-lg p-6 text-center">
              <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" id="image-upload" />
              <label htmlFor="image-upload" className="cursor-pointer flex flex-col items-center space-y-2">
                <FiUpload size={32} className="text-green-600" />
                <span className="text-sm text-gray-600">Click to upload</span>
              </label>
            </div>
          </div>
        </div>
      ) : null}

      <div className="bg-white border-t border-gray-200 p-6">
        <div className="flex gap-3">
          <button onClick={() => setShowImageUpload(true)} className="bg-green-600 hover:bg-green-700 text-white rounded-lg p-3" title="Upload disease detection image">
            <FiUpload size={20} />
          </button>
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask about diseases, water levels, crop recommendations..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-green-600"
          />
          <button onClick={handleSendMessage} disabled={loading || !inputMessage.trim()} className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white rounded-lg p-3">
            <FiSend size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatbotComponent;
