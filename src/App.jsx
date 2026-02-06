import { useState, useRef, useEffect } from "react";
import TechRivoLogo from "./assets/TechRivoLogo.png";

const COMPANY_NAME = "TechRivo";

const initialMessages = [
  {
    id: 1,
    role: "bot",
    text: `Welcome to ${COMPANY_NAME} AI Assistant. I have full access to company knowledge — policies, projects, teams, and more. How can I help you today?`,
    time: new Date(),
  },
];

const API_BASE = "http://localhost:8000/api";

function formatTime(date) {
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

export default function App() {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isTyping, setIsTyping] = useState(false);
  const [streamingId, setStreamingId] = useState(null);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  useEffect(() => {
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = "auto";
      ta.style.height = Math.min(ta.scrollHeight, 140) + "px";
    }
  }, [input]);

 
  const [connected, setConnected] = useState(false);


  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then((r) => r.ok && setConnected(true))
      .catch(() => setConnected(false));
  }, []);

  const handleSend = async () => {
    if (!input.trim() || isTyping) return;

    const userMsg = { id: Date.now(), role: "user", text: input.trim(), time: new Date() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    const botId = Date.now() + 1;
    const botTime = new Date();

    try {
     
      const res = await fetch(`${API_BASE}/chat/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg.text, stream: true }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);

    
      setMessages((prev) => [...prev, { id: botId, role: "bot", text: "", time: botTime }]);
      setIsTyping(false);
      setStreamingId(botId);

    
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let fullText = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
    
        const lines = chunk.split("\n");
        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6).trim();
            if (data === "[DONE]") break;
            try {
              const json = JSON.parse(data);
              if (json.chunk) {
                fullText += json.chunk;
                setMessages((prev) =>
                  prev.map((m) => (m.id === botId ? { ...m, text: fullText } : m))
                );
              }
            } catch (_) {
          
            }
          }
        }
      }

      setStreamingId(null);
    } catch (err) {
     
      setMessages((prev) => [
        ...prev,
        {
          id: botId,
          role: "bot",
          text: `⚠️ Error: ${err.message}. Please check the backend is running.`,
          time: botTime,
        },
      ]);
      setIsTyping(false);
      setStreamingId(null);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const startNewChat = () => {
    setMessages(initialMessages);
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

        :root {
          --techrivo-primary: #0A4C5C;
          --techrivo-secondary: #7DD3E8;
          --techrivo-dark: #083642;
          --techrivo-light: #A8E6F5;
          --techrivo-white: #FFFFFF;
          --techrivo-gray: #E5E7EB;
          --techrivo-text-dark: #1F2937;
        }

        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body {
          font-family: 'Inter', sans-serif;
          background: var(--techrivo-dark);
          color: var(--techrivo-white);
          height: 100vh;
          overflow: hidden;
        }

        .app { display: flex; height: 100vh; }

        /* ──────── SIDEBAR ──────── */
        .sidebar {
          width: ${sidebarOpen ? "256px" : "0px"};
          background: var(--techrivo-primary);
          border-right: 1px solid rgba(125, 211, 232, 0.2);
          display: flex;
          flex-direction: column;
          overflow: hidden;
          transition: width 0.32s cubic-bezier(.4,0,.2,1);
          flex-shrink: 0;
        }

        .sidebar-header {
          padding: 20px 18px 16px;
          border-bottom: 1px solid rgba(125, 211, 232, 0.2);
          display: flex;
          align-items: center;
          gap: 11px;
        }

        .logo-mark {
          width: 42px; 
          height: 42px;
          border-radius: 9px;
          display: flex; 
          align-items: center; 
          justify-content: center;
          flex-shrink: 0;
          padding: 4px;
        }

        .logo-mark img {
          width: 100%;
          height: 100%;
          object-fit: contain;
        }

        .logo-text-group .logo-name {
          font-size: 15px; 
          font-weight: 600; 
          color: var(--techrivo-white); 
          white-space: nowrap;
        }

        .logo-text-group .logo-tag {
          font-size: 9.5px; 
          color: var(--techrivo-light); 
          text-transform: uppercase;
          letter-spacing: 0.9px; 
          white-space: nowrap; 
          margin-top: 1px;
        }

        .new-chat-btn {
          margin: 12px 12px 4px;
          padding: 9px 13px;
          background: transparent;
          border: 1px solid rgba(125, 211, 232, 0.3);
          border-radius: 9px;
          color: var(--techrivo-light);
          font-size: 13px; 
          font-family: inherit;
          cursor: pointer;
          display: flex; 
          align-items: center; 
          gap: 8px;
          transition: all 0.18s;
          white-space: nowrap;
        }

        .new-chat-btn:hover {
          background: rgba(125, 211, 232, 0.1);
          border-color: var(--techrivo-secondary);
          color: var(--techrivo-secondary);
        }

        .sidebar-empty {
          flex: 1;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 12px;
          padding: 40px 20px;
        }

        .sidebar-empty p {
          font-size: 11.5px;
          color: var(--techrivo-light);
          text-align: center;
          line-height: 1.6;
        }

        /* ──────── MAIN ──────── */
        .main { flex: 1; display: flex; flex-direction: column; min-width: 0; }

        .topbar {
          display: flex; 
          align-items: center; 
          justify-content: space-between;
          padding: 13px 20px;
          border-bottom: 1px solid rgba(125, 211, 232, 0.2);
          background: var(--techrivo-primary); 
          flex-shrink: 0;
        }

        .topbar-left { display: flex; align-items: center; gap: 13px; }

        .menu-btn {
          background: none; 
          border: none; 
          color: var(--techrivo-light);
          cursor: pointer; 
          padding: 5px; 
          border-radius: 6px;
          display: flex; 
          align-items: center; 
          justify-content: center;
          transition: all 0.15s;
        }

        .menu-btn:hover { 
          background: rgba(125, 211, 232, 0.1); 
          color: var(--techrivo-secondary); 
        }

        .topbar-title { 
          font-size: 13.5px; 
          font-weight: 500; 
          color: var(--techrivo-white); 
        }
        
        .topbar-sub { 
          font-size: 10.5px; 
          color: var(--techrivo-light); 
          margin-top: 1px; 
        }

        .status {
          display: flex; 
          align-items: center; 
          gap: 6px;
          font-size: 11px; 
          color: var(--techrivo-secondary);
        }

        .status-dot {
          width: 7px; 
          height: 7px; 
          border-radius: 50%;
          background: var(--techrivo-secondary);
          box-shadow: 0 0 6px rgba(125, 211, 232, 0.45);
          animation: statusPulse 2.2s infinite;
        }

        @keyframes statusPulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.35; }
        }

        /* ──────── MESSAGES ──────── */
        .messages {
          flex: 1; 
          overflow-y: auto;
          padding: 28px 22px; 
          display: flex;
          flex-direction: column; 
          gap: 20px;
        }

        .messages::-webkit-scrollbar { width: 4px; }
        .messages::-webkit-scrollbar-track { background: transparent; }
        .messages::-webkit-scrollbar-thumb { 
          background: rgba(125, 211, 232, 0.3); 
          border-radius: 2px; 
        }

        @keyframes msgIn {
          from { opacity: 0; transform: translateY(7px); }
          to   { opacity: 1; transform: translateY(0); }
        }

        .msg-wrap { display: flex; flex-direction: column; animation: msgIn 0.22s ease; }
        .msg-wrap.user { align-items: flex-end; }
        .msg-wrap.bot  { align-items: flex-start; }

        .msg-row { display: flex; align-items: flex-end; gap: 9px; }
        .msg-row.user { flex-direction: row-reverse; }

        .bot-av {
          width: 32px; 
          height: 32px; 
          border-radius: 50%;
          display: flex; 
          align-items: center; 
          justify-content: center;
          flex-shrink: 0;
          padding: 4px;
        }

        .bot-av img {
          width: 100%;
          height: 100%;
          object-fit: contain;
        }

        .bubble {
          max-width: 72%;
          min-width: 52px;
          border-radius: 16px;
          padding: 10px 15px;
          font-size: 13.5px;
          line-height: 1.7;
          word-wrap: break-word;
          overflow-wrap: break-word;
          width: fit-content;
          white-space: pre-wrap;
        }

        .bubble.user {
          background: linear-gradient(135deg, var(--techrivo-primary), var(--techrivo-dark));
          color: var(--techrivo-white);
          border-radius: 16px 16px 4px 16px;
          box-shadow: 0 2px 8px rgba(10, 76, 92, 0.25);
        }

        .bubble.bot {
          background: rgba(125, 211, 232, 0.1);
          color: var(--techrivo-white);
          border: 1px solid rgba(125, 211, 232, 0.2);
          border-radius: 16px 16px 16px 4px;
        }

        .msg-time {
          font-size: 9.5px; 
          color: var(--techrivo-light); 
          margin-top: 4px;
        }

        .msg-time.user { text-align: right; }
        .msg-time.bot  { padding-left: 41px; }

        /* ──────── TYPING ──────── */
        .typing-row { 
          display: flex; 
          align-items: flex-end; 
          gap: 9px; 
          animation: msgIn 0.22s ease; 
        }

        .typing-bubble {
          background: rgba(125, 211, 232, 0.1); 
          border: 1px solid rgba(125, 211, 232, 0.2);
          border-radius: 16px 16px 16px 4px;
          padding: 13px 17px;
          display: flex; 
          gap: 5px; 
          align-items: center;
        }

        .t-dot {
          width: 6px; 
          height: 6px; 
          border-radius: 50%;
          background: var(--techrivo-secondary);
          animation: tBounce 1.3s infinite;
        }
        .t-dot:nth-child(2) { animation-delay: 0.16s; }
        .t-dot:nth-child(3) { animation-delay: 0.32s; }

        @keyframes tBounce {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-4px); }
        }

        /* ──────── INPUT ──────── */
        .input-area {
          padding: 14px 20px 18px;
          background: var(--techrivo-primary);
          border-top: 1px solid rgba(125, 211, 232, 0.2);
          flex-shrink: 0;
        }

        .input-box {
          display: flex; 
          align-items: flex-end; 
          gap: 10px;
          background: rgba(125, 211, 232, 0.1);
          border: 1px solid rgba(125, 211, 232, 0.2);
          border-radius: 13px;
          padding: 10px 10px 10px 17px;
          transition: border-color 0.2s;
        }

        .input-box:focus-within { border-color: var(--techrivo-secondary); }

        .input-box textarea {
          flex: 1; 
          background: transparent;
          border: none; 
          outline: none; 
          resize: none;
          color: var(--techrivo-white); 
          font-size: 13.5px;
          font-family: inherit; 
          line-height: 1.6;
          max-height: 140px; 
          min-height: 24px;
        }

        .input-box textarea::placeholder { color: var(--techrivo-light); }

        .send-btn {
          background: linear-gradient(135deg, var(--techrivo-secondary), var(--techrivo-primary));
          border: none; 
          color: var(--techrivo-dark);
          width: 38px; 
          height: 38px;
          border-radius: 9px; 
          cursor: pointer;
          display: flex; 
          align-items: center; 
          justify-content: center;
          transition: all 0.18s; 
          flex-shrink: 0;
          box-shadow: 0 2px 8px rgba(125, 211, 232, 0.3);
        }

        .send-btn:hover {
          transform: translateY(-1px);
          box-shadow: 0 4px 14px rgba(125, 211, 232, 0.4);
        }

        .send-btn:active { transform: translateY(0); }
        .send-btn:disabled { 
          opacity: 0.35; 
          cursor: not-allowed; 
          transform: none; 
          box-shadow: none; 
        }

        .input-hint {
          font-size: 10.5px; 
          color: var(--techrivo-light);
          text-align: center; 
          margin-top: 9px;
        }

        .input-hint kbd {
          background: rgba(125, 211, 232, 0.1); 
          border: 1px solid rgba(125, 211, 232, 0.2);
          border-radius: 4px; 
          padding: 2px 6px;
          font-family: 'JetBrains Mono', monospace;
          font-size: 9.5px; 
          color: var(--techrivo-secondary);
        }

        /* ── Streaming cursor blink ── */
        @keyframes cursorBlink {
          0%, 100% { opacity: 1; }
          50%      { opacity: 0; }
        }
        .cursor-blink::after {
          content: '';
          display: inline-block;
          width: 2px;
          height: 1em;
          background: var(--techrivo-secondary);
          margin-left: 3px;
          vertical-align: text-bottom;
          border-radius: 1px;
          animation: cursorBlink 0.6s steps(1) infinite;
        }
      `}</style>

      <div className="app">
        {/* ── SIDEBAR ── */}
        <div className="sidebar">
          <div className="sidebar-header">
            <div className="logo-mark">
              <img src={TechRivoLogo} alt={COMPANY_NAME} />
            </div>
            <div className="logo-text-group">
              <div className="logo-name">{COMPANY_NAME}</div>
              <div className="logo-tag">AI Assistant</div>
            </div>
          </div>

          <button className="new-chat-btn" onClick={startNewChat}>
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
              <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            New Conversation
          </button>

         
          <div className="sidebar-empty">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
            </svg>
            <p>No conversations yet.<br/>Start one above.</p>
          </div>
        </div>

      
        <div className="main">
          <div className="topbar">
            <div className="topbar-left">
              <button className="menu-btn" onClick={() => setSidebarOpen(!sidebarOpen)}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
                </svg>
              </button>
              <div>
                <div className="topbar-title">{COMPANY_NAME} AI Assistant</div>
                <div className="topbar-sub">Powered by RAG · Lisbon, Portugal</div>
              </div>
            </div>
            <div className="status">
              <span className="status-dot" style={{ background: connected ? "#7DD3E8" : "#e74c3c", boxShadow: connected ? "0 0 6px rgba(125, 211, 232, 0.45)" : "0 0 6px rgba(231,76,60,0.45)" }}></span>
              {connected ? "Connected" : "Disconnected"}
            </div>
          </div>

          <div className="messages">
            {messages.map((msg) => (
              <div key={msg.id} className={`msg-wrap ${msg.role}`}>
                <div className={`msg-row ${msg.role}`}>
                  {msg.role === "bot" && (
                    <div className="bot-av">
                      <img src={TechRivoLogo} alt={COMPANY_NAME} />
                    </div>
                  )}
                  <div className={`bubble ${msg.role}${msg.role === "bot" && streamingId === msg.id ? " cursor-blink" : ""}`}>{msg.text}</div>
                </div>
                <div className={`msg-time ${msg.role}`}>{formatTime(msg.time)}</div>
              </div>
            ))}

            {isTyping && (
              <div>
                <div className="typing-row">
                  <div className="bot-av">
                    <img src={TechRivoLogo} alt={COMPANY_NAME} />
                  </div>
                  <div className="typing-bubble">
                    <span className="t-dot"/><span className="t-dot"/><span className="t-dot"/>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className="input-area">
            <div className="input-box">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask anything about TechRivo..."
              />
              <button className="send-btn" onClick={handleSend} disabled={!input.trim() || isTyping}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2" fill="currentColor" stroke="none"/>
                </svg>
              </button>
            </div>
            <div className="input-hint">
              Press <kbd>Enter</kbd> to send · <kbd>Shift + Enter</kbd> for new line
            </div>
          </div>
        </div>
      </div>
    </>
  );
}