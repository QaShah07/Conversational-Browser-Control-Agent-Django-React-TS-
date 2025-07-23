export const wsURL = (convId: string) =>
  `${import.meta.env.VITE_WS_URL || 'ws://localhost:8000'}/ws/conversation/${convId}/`;