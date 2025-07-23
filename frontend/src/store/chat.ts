import { create } from 'zustand';
import { Message } from '../types';

interface ChatState {
  messages: Message[];
  status: string;
  add: (m: Message) => void;
  setStatus: (s: string) => void;
  setMessages: (m: Message[]) => void;
}

export const useChat = create<ChatState>((set) => ({
  messages: [],
  status: '',
  add: (m) => set((st) => ({ messages: [...st.messages, m] })),
  setStatus: (s) => set(() => ({ status: s })),
  setMessages: (m) => set(() => ({ messages: m })),
}));