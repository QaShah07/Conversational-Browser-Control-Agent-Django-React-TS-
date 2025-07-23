export const Lightbox = ({ src, onClose }: { src: string; onClose: () => void }) => {
  return (
    <div
      className="fixed inset-0 bg-black/70 flex items-center justify-center z-50"
      onClick={onClose}
    >
      <img src={src} className="max-h-[90vh] max-w-[90vw]" />
    </div>
  );
};