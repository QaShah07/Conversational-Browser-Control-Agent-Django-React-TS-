export const scrollToBottom = (id: string) => {
  const el = document.getElementById(id);
  if (el) el.scrollTop = el.scrollHeight;
};