import { useChat } from '../store/chat';
export const StatusBar = () => {
  const status = useChat((s) => s.status);
  return <div className="text-xs text-gray-500">{status}</div>;
};