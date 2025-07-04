import Head from 'next/head';
import { useEffect, useRef, useState } from 'react';

const TAGS = [
  "For material MAT-0152, what is its shelf life?",
  "How much net quantity of outbound in singapore warehouse this week?",
  "What is the Total Cap for the Singapore warehouse?",
  "What is the Projected Inventory in Singapore Today?",
  "What is the Total Cap for the China warehouse?",
];

type Message = {
  role: 'user' | 'agent';
  content: string;
};

export default function Home() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [chatMode, setChatMode] = useState(false);
  const [thinkingLog, setThinkingLog] = useState<any>({});
  const [showThinkingLog, setShowThinkingLog] = useState(false);
  const [threadId, setThreadId] = useState<string | null>(null);

  const chatEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const generateResponse = async (query: string) => {
    if (!chatMode) setChatMode(true);

    const updatedMessages: Message[] = [...messages, { role: 'user', content: query }];
    setMessages(updatedMessages);
    setLoading(true);
    setShowThinkingLog(false);

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: query,
          thread_id: threadId,
        }),
      });

      const data = await res.json();

      const rawReply = data.reply ?? '⚠️ No response from AI.';
      const reply =
        typeof rawReply === 'string'
          ? rawReply
          : rawReply?.text ?? rawReply?.value ?? JSON.stringify(rawReply);

      setThinkingLog(data.thinking_log ?? {});
      if (data.thread_id) setThreadId(data.thread_id);

      let i = 0;
      setMessages((prev) => [...prev, { role: 'agent', content: '' }]);

      const interval = setInterval(() => {
        i++;
        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            role: 'agent',
            content: reply.slice(0, i),
          };
          return updated;
        });

        if (i >= reply.length) {
          clearInterval(interval);
          setLoading(false);
        }
      }, 25);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [...prev, { role: 'agent', content: '⚠️ Failed to get response from AI.' }]);
      setLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;
    generateResponse(input);
    setInput('');
  };

  return (
    <>
      <Head>
        <title>Agentory</title>
      </Head>

      <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center px-4 font-sans relative">
        <header className="absolute top-6 left-0 right-0 flex justify-between items-center px-6 text-sm text-gray-400 z-10">
          <div className="w-1/3" />

          {chatMode && (
            <div className="flex justify-center gap-4 w-1/3">
              <button
                className={`px-4 py-1 rounded-full text-sm ${!showThinkingLog ? 'bg-indigo-600' : 'bg-gray-700'} text-white`}
                onClick={() => setShowThinkingLog(false)}
              >
                💬 Chat
              </button>
              <button
                className={`px-4 py-1 rounded-full text-sm ${showThinkingLog ? 'bg-indigo-600' : 'bg-gray-700'} text-white`}
                onClick={() => setShowThinkingLog(true)}
              >
                🧠 Thinking Log
              </button>
            </div>
          )}

          <div className="flex items-center gap-6 justify-end w-1/3">
            <a href="#" className="hover:text-white">About</a>
            <a href="#" className="hover:text-white">Manual</a>
            <button className="bg-gray-800 px-4 py-1 rounded-full text-white hover:bg-gray-700">Login</button>
          </div>
        </header>

        <main className="text-center w-full max-w-4xl pt-40">
          {!chatMode && (
            <>
              <h1 className="text-3xl md:text-4xl font-semibold mb-4">
                Think of me as your warehouse’s new best friend
              </h1>
              <p className="text-gray-400 text-sm mb-6">
              Use AI to answer questions, calculate inventory, and streamline warehouse insights
              </p>

              <form onSubmit={handleSubmit} className="w-full mt-8">
                <div className="relative w-full max-w-xl mx-auto">
                  <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    type="text"
                    placeholder="What would you like me to help with?"
                    className="w-full px-6 py-3 pr-14 rounded-full text-lg bg-neutral-900 text-white placeholder-gray-500 border border-neutral-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                  <button type="submit" className="absolute right-2 top-1.5 bottom-1.5 px-4 rounded-full bg-indigo-600 hover:bg-indigo-500 text-white">
                    ↑
                  </button>
                </div>
              </form>

              <div className="flex flex-wrap justify-center mt-6 gap-2">
                {TAGS.map((tag) => (
                  <button
                    key={tag}
                    onClick={() => {
  if (!loading) {
    setInput('');
    generateResponse(tag);
  }
}}
                    className="px-6 py-2 bg-neutral-800 text-sm text-white rounded-full hover:bg-neutral-700 transition-colors duration-150 whitespace-nowrap"
                  >
                    {tag}
                  </button>
                ))}
              </div>
            </>
          )}

          {chatMode && (
            <>
              {showThinkingLog ? (
                <div className="mt-6 bg-neutral-900 p-4 rounded-lg w-full max-w-3xl mx-auto text-sm overflow-x-auto text-left">
                  <h3 className="text-indigo-400 mb-2">Assistant Reasoning Steps:</h3>
                  {Object.keys(thinkingLog).length === 0 ? (
                    <p className="text-gray-400">No thinking log available.</p>
                  ) : (
                    <div className="space-y-4">
                      {Object.entries(thinkingLog).map(([agent, log], idx) => (
                        <div key={idx}>
                          <h4 className="text-indigo-300 font-semibold capitalize mb-1">{agent}</h4>
                          {Array.isArray(log) ? (
                            <ul className="list-disc pl-5 space-y-1">
                              {log.map((item: any, i: number) => (
                                <li key={i}>
                                  <pre className="whitespace-pre-wrap break-words text-white">{JSON.stringify(item, null, 2)}</pre>
                                </li>
                              ))}
                            </ul>
                          ) : (
                            <pre className="whitespace-pre-wrap break-words text-white bg-neutral-800 p-2 rounded">
                              {typeof log === 'string' ? log : JSON.stringify(log, null, 2)}
                            </pre>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ) : (
                <div className="flex flex-col max-w-3xl mx-auto text-left" style={{ height: '60vh' }}>
                  <div ref={chatContainerRef} className="flex-1 overflow-y-auto space-y-4 pb-4 w-full">
                    {messages.map((msg, i) => {
                      const isUser = msg.role === 'user';
                      const prev = messages[i - 1];
                      const addSpacing = !isUser && prev?.role === 'user';

                      return (
                        <div key={i} className={`flex ${isUser ? 'justify-end' : 'justify-start'} ${addSpacing ? 'mt-6' : ''}`}>
                          <div className={isUser ? 'inline-block max-w-[50%] p-3 rounded-full bg-indigo-700 text-white text-left' : 'text-white'}>
                            <div className="px-3 py-1">
                              {msg.content}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                    <div ref={chatEndRef} />
                  </div>

                  <form onSubmit={handleSubmit} className="w-full mt-6">
                    <div className="relative w-full">
                      <input
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        type="text"
                        placeholder="What would you like me to help with?"
                        className="w-full px-6 py-3 pr-14 rounded-full text-lg bg-neutral-900 text-white placeholder-gray-500 border border-neutral-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                      <button type="submit" className="absolute right-2 top-1.5 bottom-1.5 px-4 rounded-full bg-indigo-600 hover:bg-indigo-500 text-white">
                        ↑
                      </button>
                    </div>
                  </form>
                </div>
              )}
            </>
          )}
        </main>

        {!chatMode && (
          <footer className="absolute bottom-4 text-center text-xs text-gray-500 max-w-xl mx-auto px-4">
            <p>Agentory is an interactive AI assistant. This is a demo UI. © 2025</p>
          </footer>
        )}
      </div>
    </>
  );
}
