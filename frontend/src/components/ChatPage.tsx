import { useEffect, useRef } from 'react';
import { api } from '../api/http';
import { useChat } from '../store/chat';
import { useChatWS } from '../hooks/useChatWS';
import { MessageBubble } from './MessageBubble';
import { ScreenshotBubble } from './ScreenshotBubble';
import { InputBar } from './InputBar';
import { StatusBar } from './StatusBar';
import { Message } from '../types';
import { scrollToBottom } from '../utils/scroll';

export const ChatPage = () => {
  const convIdRef = useRef<string>('');
  const { messages, setMessages } = useChat();

  useEffect(() => {
    const init = async () => {
      const { data } = await api.post('/conversations/');
      convIdRef.current = data.id;
      const { data: conv } = await api.get(`/conversations/${data.id}/messages/`);
      setMessages(conv.messages as Message[]);
      useChatWS(data.id);
    };
    init();
  }, [setMessages]);

  useEffect(() => {
    scrollToBottom('chat-scroll');
  }, [messages]);

  return (
    <div className="max-w-3xl mx-auto p-4 space-y-3">
      <StatusBar />
      <div
        id="chat-scroll"
        className="space-y-2 max-h-[70vh] overflow-y-auto border p-2 rounded bg-white"
      >
        {messages.map((m) =>
          m.role === 'screenshot' ? (
            <ScreenshotBubble key={m.id} m={m} />
          ) : (
            <MessageBubble key={m.id} m={m} />
          )
        )}
      </div>
      <InputBar convId={convIdRef.current} />
    </div>
  );
};