import { useState } from 'react';
import { Message } from '../types';
import { Lightbox } from './Lightbox';

export const ScreenshotBubble = ({ m }: { m: Message }) => {
  const [open, setOpen] = useState(false);
  if (m.role !== 'screenshot' || !m.image_url) return null;
  return (
    <div className="w-full flex justify-start">
      <img
        src={m.image_url}
        className="max-w-[75%] rounded border cursor-zoom-in"
        onClick={() => setOpen(true)}
      />
      {open && <Lightbox src={m.image_url} onClose={() => setOpen(false)} />}
    </div>
  );
};