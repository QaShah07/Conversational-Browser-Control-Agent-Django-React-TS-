import { useState } from 'react';
import { api } from '../api/http';
import { useChat } from '../store/chat';

export const InputBar = ({ convId }: { convId: string }) => {
  const [text, setText] = useState('');
  const add = useChat((s) => s.add);

  const send = async () => {
    if (!text.trim()) return;
    // Optimistic UI
    add({ id: crypto.randomUUID(), role: 'user', content: text });
    const payload = { content: text };
    setText('');
    await api.post(`/conversations/${convId}/messages/`, payload);
  };

  return (
    <div className="flex gap-2">
      <input
        className="flex-1 border rounded px-2 py-2"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type a message..."
        onKeyDown={(e)=>{ if(e.key==='Enter') send(); }}
      />
      <button onClick={send} className="bg-blue-600 text-white px-4 rounded">
        Send
      </button>
    </div>
  );
};