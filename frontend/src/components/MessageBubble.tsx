import { Message } from '../types';

export const MessageBubble = ({ m }: { m: Message }) => {
  if (m.role === 'screenshot') return null; // handled separately
  const isUser = m.role === 'user';
  return (
    <div className={`w-full flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[75%] px-3 py-2 rounded shadow whitespace-pre-wrap ${
          isUser ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-900'
        }`}
      >
        {m.content}
      </div>
    </div>
  );
};