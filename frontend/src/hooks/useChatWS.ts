import { useEffect, useRef } from 'react';
import { useChat } from '../store/chat';
import { wsURL } from '../api/ws';
import { Message, WSStatusPayload } from '../types';

export const useChatWS = (convId: string) => {
  const add = useChat((s) => s.add);
  const setStatus = useChat((s) => s.setStatus);
  const wsRef = useRef<WebSocket>();

  useEffect(() => {
    if (!convId) return;
    const ws = new WebSocket(wsURL(convId));
    wsRef.current = ws;

    ws.onmessage = (ev) => {
      const data = JSON.parse(ev.data);
      if (data.type === 'message.new') add(data.payload as Message);
      if (data.type === 'status.update') setStatus((data.payload as WSStatusPayload).msg);
    };

    ws.onclose = () => {
      // naive reconnect after 2s
      setTimeout(() => useChatWS(convId), 2000);
    };

    return () => ws.close();
  }, [convId, add, setStatus]);
};