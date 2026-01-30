import React, { useState, useRef, useEffect } from 'react';
import { Send, BookOpen, Sparkles, User, Bot } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';
import { chatWithVedaGPT } from '../api';
import clsx from 'clsx';

const ChatInterface = () => {
    const [messages, setMessages] = useState([
        { role: 'system', content: 'Pranam. I am VedaGPT. Ask me about the sacred wisdom of the Vedas, and I shall illuminate the path.' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(scrollToBottom, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMsg = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsLoading(true);

        try {
            const data = await chatWithVedaGPT(userMsg.content);
            const botMsg = {
                role: 'assistant',
                content: data.response,
                sources: data.sources // Array of source metadata
            };
            setMessages(prev => [...prev, botMsg]);
        } catch (error) {
            setMessages(prev => [...prev, { role: 'assistant', content: 'Forgive me, I am unable to connect to the cosmic knowledge (Server Error).', isError: true }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen max-w-4xl mx-auto p-4 font-sans text-gray-200">

            {/* Header */}
            <header className="flex items-center justify-center p-6 mb-4 border-b border-vedic-secondary/30">
                <Sparkles className="w-8 h-8 text-vedic-primary mr-3 animate-pulse" />
                <h1 className="text-4xl font-serif text-vedic-accent tracking-wider">VedaGPT</h1>
            </header>

            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto space-y-6 p-4 scrollbar-thin scrollbar-thumb-vedic-secondary scrollbar-track-transparent">
                <AnimatePresence>
                    {messages.map((msg, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={clsx(
                                "flex items-start gap-4",
                                msg.role === 'user' ? "flex-row-reverse" : "flex-row"
                            )}
                        >
                            <div className={clsx(
                                "w-10 h-10 rounded-full flex items-center justify-center shrink-0 border-2",
                                msg.role === 'user' ? "bg-vedic-primary border-vedic-accent" : "bg-vedic-secondary border-vedic-primary"
                            )}>
                                {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                            </div>

                            <div className={clsx(
                                "p-4 rounded-2xl max-w-[80%] shadow-lg backdrop-blur-sm border",
                                msg.role === 'user'
                                    ? "bg-vedic-secondary/20 border-vedic-primary/30 rounded-tr-none text-right"
                                    : "bg-vedic-paper border-vedic-secondary/30 rounded-tl-none text-left"
                            )}>
                                <div className="prose prose-invert max-w-none text-md leading-relaxed">
                                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                                </div>

                                {/* Sources Footnote */}
                                {msg.sources && msg.sources.length > 0 && (
                                    <div className="mt-4 pt-3 border-t border-white/10 text-xs text-vedic-anchor opacity-80 flex flex-col gap-1">
                                        <p className="font-semibold flex items-center gap-1 text-vedic-accent">
                                            <BookOpen size={12} /> Sources:
                                        </p>
                                        {msg.sources.map((s, i) => (
                                            <span key={i} className="italic">
                                                {s.source} (Chunk {s.chunk_id})
                                            </span>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>

                {isLoading && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex items-center gap-3 text-vedic-accent ml-14"
                    >
                        <div className="w-2 h-2 bg-vedic-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                        <div className="w-2 h-2 bg-vedic-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                        <div className="w-2 h-2 bg-vedic-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                        <span className="text-sm font-serif italic opacity-70">Contemplating the verses...</span>
                    </motion.div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 mt-2">
                <div className="relative group">
                    <div className="absolute -inset-0.5 bg-gradient-to-r from-vedic-primary to-vedic-accent rounded-xl blur opacity-30 group-hover:opacity-60 transition duration-1000"></div>
                    <div className="relative flex items-center bg-vedic-paper rounded-xl p-2 border border-vedic-secondary/50">
                        <input
                            type="text"
                            className="flex-1 bg-transparent border-none outline-none text-white px-4 py-3 placeholder-gray-500 font-sans text-lg"
                            placeholder="Ask about Dharma, Karma, or Reality..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                        />
                        <button
                            onClick={handleSend}
                            disabled={isLoading || !input.trim()}
                            className="p-3 bg-vedic-primary hover:bg-vedic-accent text-vedic-bg rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105"
                        >
                            <Send size={24} />
                        </button>
                    </div>
                </div>
                <p className="text-center text-xs text-gray-600 mt-2 font-serif">
                    Powered by knowledge from Rig, Sama, Yajur, and Atharva Vedas.
                </p>
            </div>

        </div>
    );
};

export default ChatInterface;
