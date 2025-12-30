import React, { useState, useRef, useEffect } from 'react';
import { Send, Menu, X, MessageSquare, Clock, CheckCircle2, FileText } from 'lucide-react';

const FlowmindAssistant = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [chatHistory] = useState([
    { id: '1', title: 'CSV Validation Process', timestamp: '2024-12-29 14:30', preview: 'How to validate CSV files...' },
    { id: '2', title: 'Database Migration Steps', timestamp: '2024-12-28 10:15', preview: 'Steps for migrating database...' },
    { id: '3', title: 'API Integration Testing', timestamp: '2024-12-27 16:45', preview: 'Testing API endpoints...' }
  ]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: input,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const botResponse = {
        id: Date.now() + 1,
        type: 'assistant',
        content: {
          procedure: [
            {
              step: 1,
              title: 'Data Collection',
              description: 'Gather all necessary input data and system requirements',
              expectedResult: 'Complete dataset with all required fields populated'
            },
            {
              step: 2,
              title: 'Validation Checks',
              description: 'Run automated validation rules on collected data',
              expectedResult: 'All validation rules pass with zero critical errors'
            },
            {
              step: 3,
              title: 'System Integration',
              description: 'Integrate validated data into the target system',
              expectedResult: 'Successful data integration with confirmation logs'
            }
          ],
          summary: 'Computer system validation process completed successfully'
        },
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadHistorySession = (sessionId) => {
    setShowHistory(false);
  };

  const StructuredResponse = ({ content }) => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {content.procedure && content.procedure.map((step) => (
        <div key={step.step} style={{
          backgroundColor: '#ffffff',
          border: '1px solid #e5e7eb',
          borderRadius: '8px',
          padding: '16px',
          boxShadow: '0 1px 2px 0 rgba(0,0,0,0.05)'
        }}>
          <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
            <div style={{
              width: '32px',
              height: '32px',
              backgroundColor: '#3b82f6',
              color: 'white',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 'bold',
              flexShrink: 0
            }}>
              {step.step}
            </div>
            <div style={{ flex: 1 }}>
              <h4 style={{ fontWeight: '600', color: '#111827', marginBottom: '4px' }}>
                {step.title}
              </h4>
              <p style={{ color: '#4b5563', fontSize: '14px', marginBottom: '8px' }}>
                {step.description}
              </p>
              <div style={{
                display: 'flex',
                gap: '8px',
                backgroundColor: '#f0fdf4',
                border: '1px solid #86efac',
                borderRadius: '4px',
                padding: '8px',
                alignItems: 'flex-start'
              }}>
                <CheckCircle2 style={{
                  width: '16px',
                  height: '16px',
                  color: '#16a34a',
                  marginTop: '2px',
                  flexShrink: 0
                }} />
                <p style={{ fontSize: '14px', color: '#166534' }}>
                  <span style={{ fontWeight: '600' }}>Expected Result:</span> {step.expectedResult}
                </p>
              </div>
            </div>
          </div>
        </div>
      ))}
      {content.summary && (
        <div style={{
          backgroundColor: '#eff6ff',
          border: '1px solid #bfdbfe',
          borderRadius: '8px',
          padding: '12px'
        }}>
          <p style={{ fontSize: '14px', color: '#1e40af', fontWeight: '500' }}>
            {content.summary}
          </p>
        </div>
      )}
    </div>
  );

  return (
    <div style={{
      display: 'flex',
      height: '100vh',
      backgroundColor: '#f9fafb',
      overflow: 'hidden'
    }}>
      {/* Chat History Sidebar */}
      <div style={{
        position: showHistory ? 'fixed' : 'fixed',
        left: showHistory ? 0 : '-100%',
        top: 0,
        zIndex: 20,
        width: '320px',
        backgroundColor: '#ffffff',
        borderRight: '1px solid #e5e7eb',
        transition: 'left 0.3s ease-in-out',
        height: '100vh',
        display: 'flex',
        flexDirection: 'column'
      }}>
        <div style={{
          padding: '16px',
          borderBottom: '1px solid #e5e7eb',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <h2 style={{
            fontWeight: '600',
            color: '#111827',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <Clock size={20} />
            Chat History
          </h2>
          <button
            onClick={() => setShowHistory(false)}
            style={{
              backgroundColor: 'transparent',
              border: 'none',
              color: '#6b7280',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center'
            }}
          >
            <X size={20} />
          </button>
        </div>
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '12px',
          display: 'flex',
          flexDirection: 'column',
          gap: '8px'
        }}>
          {chatHistory.map((session) => (
            <button
              key={session.id}
              onClick={() => loadHistorySession(session.id)}
              style={{
                width: '100%',
                textAlign: 'left',
                padding: '12px',
                borderRadius: '8px',
                border: '1px solid #e5e7eb',
                backgroundColor: '#ffffff',
                cursor: 'pointer',
                transition: 'background-color 0.2s'
              }}
              onMouseEnter={(e) => e.target.style.backgroundColor = '#f3f4f6'}
              onMouseLeave={(e) => e.target.style.backgroundColor = '#ffffff'}
            >
              <div style={{
                fontWeight: '500',
                color: '#111827',
                fontSize: '14px',
                marginBottom: '4px',
                whiteSpace: 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis'
              }}>
                {session.title}
              </div>
              <div style={{
                fontSize: '12px',
                color: '#9ca3af',
                marginBottom: '4px'
              }}>
                {session.timestamp}
              </div>
              <div style={{
                fontSize: '12px',
                color: '#4b5563',
                whiteSpace: 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis'
              }}>
                {session.preview}
              </div>
            </button>
          ))}
        </div>
        <div style={{
          padding: '16px',
          borderTop: '1px solid #e5e7eb'
        }}>
          <button style={{
            width: '100%',
            padding: '8px 16px',
            backgroundColor: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: '500',
            transition: 'background-color 0.2s'
          }}
          onMouseEnter={(e) => e.target.style.backgroundColor = '#2563eb'}
          onMouseLeave={(e) => e.target.style.backgroundColor = '#3b82f6'}
          >
            New Chat
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        minHeight: 0
      }}>
        {/* Header */}
        <div style={{
          backgroundColor: '#ffffff',
          borderBottom: '1px solid #e5e7eb',
          padding: '12px 16px',
          display: 'flex',
          alignItems: 'center',
          gap: '12px'
        }}>
          <button
            onClick={() => setShowHistory(!showHistory)}
            style={{
              backgroundColor: 'transparent',
              border: 'none',
              color: '#4b5563',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center'
            }}
          >
            <Menu size={24} />
          </button>
          <FileText size={24} color="#3b82f6" />
          <div>
            <h1 style={{
              fontWeight: 'bold',
              color: '#111827',
              margin: '0'
            }}>
              Flowmind Assistant
            </h1>
            <p style={{
              fontSize: '12px',
              color: '#9ca3af',
              margin: '0'
            }}>
              CSV Validation Expert
            </p>
          </div>
        </div>

        {/* Messages */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '16px',
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
          minHeight: 0
        }}>
          {messages.length === 0 ? (
            <div style={{
              height: '100%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <div style={{
                textAlign: 'center',
                maxWidth: '448px'
              }}>
                <MessageSquare size={64} color="#d1d5db" style={{ margin: '0 auto 16px' }} />
                <h2 style={{
                  fontSize: '20px',
                  fontWeight: '600',
                  color: '#374151',
                  marginBottom: '8px'
                }}>
                  Welcome to Flowmind Assistant
                </h2>
                <p style={{
                  color: '#6b7280'
                }}>
                  Ask me about computer system validation procedures and I'll provide structured steps with expected results.
                </p>
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                style={{
                  display: 'flex',
                  justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start'
                }}
              >
                <div style={{
                  maxWidth: '960px',
                  width: message.type === 'user' ? 'auto' : '100%'
                }}>
                  {message.type === 'user' ? (
                    <div style={{
                      backgroundColor: '#3b82f6',
                      color: 'white',
                      borderRadius: '8px',
                      padding: '8px 16px',
                      display: 'inline-block'
                    }}>
                      {message.content}
                    </div>
                  ) : (
                    <div style={{
                      backgroundColor: '#ffffff',
                      borderRadius: '8px',
                      padding: '16px',
                      boxShadow: '0 1px 2px 0 rgba(0,0,0,0.05)',
                      border: '1px solid #e5e7eb'
                    }}>
                      <StructuredResponse content={message.content} />
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
              <div style={{
                backgroundColor: '#ffffff',
                borderRadius: '8px',
                padding: '16px',
                boxShadow: '0 1px 2px 0 rgba(0,0,0,0.05)',
                border: '1px solid #e5e7eb'
              }}>
                <div style={{ display: 'flex', gap: '8px' }}>
                  {[0, 1, 2].map(i => (
                    <div
                      key={i}
                      style={{
                        width: '8px',
                        height: '8px',
                        backgroundColor: '#3b82f6',
                        borderRadius: '50%',
                        animation: `bounce 1.4s infinite`,
                        animationDelay: `${i * 0.1}s`
                      }}
                    />
                  ))}
                </div>
                <style>{`
                  @keyframes bounce {
                    0%, 80%, 100% { opacity: 0.5; transform: translateY(0); }
                    40% { opacity: 1; transform: translateY(-8px); }
                  }
                `}</style>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div style={{
          backgroundColor: '#ffffff',
          borderTop: '1px solid #e5e7eb',
          padding: '12px 16px',
          flexShrink: 0
        }}>
          <div style={{
            width: '100%',
            display: 'flex',
            gap: '8px'
          }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Ask about validation procedures..."
              disabled={isLoading}
              style={{
                flex: 1,
                minWidth: 0,
                padding: '12px 16px',
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                fontSize: '14px',
                fontFamily: 'inherit',
                outline: 'none',
                transition: 'border-color 0.2s, box-shadow 0.2s'
              }}
              onFocus={(e) => {
                e.target.style.borderColor = '#3b82f6';
                e.target.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
              }}
              onBlur={(e) => {
                e.target.style.borderColor = '#d1d5db';
                e.target.style.boxShadow = 'none';
              }}
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
              style={{
                padding: '12px 16px',
                backgroundColor: !input.trim() || isLoading ? '#d1d5db' : '#3b82f6',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: !input.trim() || isLoading ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                flexShrink: 0,
                transition: 'background-color 0.2s',
                fontWeight: '500'
              }}
              onMouseEnter={(e) => {
                if (!(!input.trim() || isLoading)) {
                  e.target.style.backgroundColor = '#2563eb';
                }
              }}
              onMouseLeave={(e) => {
                if (!(!input.trim() || isLoading)) {
                  e.target.style.backgroundColor = '#3b82f6';
                }
              }}
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      </div>

      {/* Overlay for mobile */}
      {showHistory && (
        <div
          onClick={() => setShowHistory(false)}
          style={{
            position: 'fixed',
            inset: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            zIndex: 10
          }}
        />
      )}
    </div>
  );
};

export default FlowmindAssistant;