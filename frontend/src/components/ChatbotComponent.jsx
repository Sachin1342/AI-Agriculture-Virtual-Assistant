import React, { useState, useEffect, useRef } from 'react';
import { chatbotAPI } from '../api/client';
import { FiSend, FiUpload, FiX } from 'react-icons/fi';

const ChatbotComponent = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: 'Hello! I\'m your AI agricultural assistant. How can I help you today?',
      timestamp: new Date(),
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [showImageUpload, setShowImageUpload] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      sender: 'user',
      text: inputMessage,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await chatbotAPI.sendMessage(inputMessage);
      const botMessage = {
        id: messages.length + 2,
        sender: 'bot',
        text: response.data.chatbot_response,
        intent: response.data.intent,
        confidence: response.data.confidence,
        action: response.data.action,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: messages.length + 2,
        sender: 'bot',
        text: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploadedFile(file);
    setLoading(true);

    try {
      const response = await chatbotAPI.detectDisease(file);
      
      const botMessage = {
        id: messages.length + 1,
        sender: 'bot',
        text: `Disease Detected: ${response.data.disease}\nConfidence: ${response.data.confidence_percentage}\n\nTreatments:\n${response.data.treatments.join('\n')}`,
        type: 'disease_detection',
        data: response.data,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
      setShowImageUpload(false);
    } catch (error) {
      const errorMessage = {
        id: messages.length + 1,
        sender: 'bot',
        text: 'Failed to detect disease. Please try another image.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-green-50 to-blue-50">
      {/* Header */}
      <div className="bg-green-600 text-white p-6 shadow-lg">
        <h1 className="text-3xl font-bold">🌾 Crop Assistant AI</h1>
        <p className="text-green-100">Your intelligent agricultural companion</p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
                msg.sender === 'user'
                  ? 'bg-blue-500 text-white rounded-br-none'
                  : 'bg-white text-gray-800 rounded-bl-none border border-gray-200'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
              {msg.data && (
                <div className="mt-2 text-xs opacity-75">
                  <p>Disease: {msg.data.disease}</p>
                  <p>Confidence: {msg.data.confidence_percentage}</p>
                </div>
              )}
              {msg.confidence && (
                <p className="text-xs mt-1 opacity-75">
                  Confidence: {(msg.confidence * 100).toFixed(0)}%
                </p>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white text-gray-800 px-4 py-3 rounded-lg border border-gray-200">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-green-600 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-green-600 rounded-full animate-bounce delay-100" />
                <div className="w-2 h-2 bg-green-600 rounded-full animate-bounce delay-200" />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Image Upload Modal */}
      {showImageUpload && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4 shadow-xl">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-800">Upload Leaf Image</h2>
              <button
                onClick={() => setShowImageUpload(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                <FiX size={20} />
              </button>
            </div>
            
            <div className="border-2 border-dashed border-green-300 rounded-lg p-6 text-center">
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="hidden"
                id="image-upload"
              />
              <label
                htmlFor="image-upload"
                className="cursor-pointer flex flex-col items-center space-y-2"
              >
                <FiUpload size={32} className="text-green-600" />
                <span className="text-sm text-gray-600">
                  Click to upload or drag and drop
                </span>
                <span className="text-xs text-gray-400">PNG, JPG up to 10MB</span>
              </label>
            </div>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 p-6">
        <div className="flex gap-3">
          <button
            onClick={() => setShowImageUpload(true)}
            className="flex-shrink-0 bg-green-600 hover:bg-green-700 text-white rounded-lg p-3 transition"
            title="Upload disease detection image"
          >
            <FiUpload size={20} />
          </button>
          
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask about diseases, water levels, crop recommendations..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-green-600"
          />
          
          <button
            onClick={handleSendMessage}
            disabled={loading || !inputMessage.trim()}
            className="flex-shrink-0 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white rounded-lg p-3 transition"
          >
            <FiSend size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatbotComponent;
