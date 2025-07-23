export type Role = 'user' | 'agent' | 'screenshot' | 'system';

export interface Message {
  id: string;
  role: Role;
  content?: string;
  image_url?: string;
  created_at?: string;
}

export interface WSStatusPayload { msg: string }