import { onMounted, onBeforeUnmount, type Ref } from 'vue';

export function useClickOutside(
  targetRef: Ref<HTMLElement | null>,
  handler: (event: MouseEvent | TouchEvent) => void,
) {
  const listener = (event: MouseEvent | TouchEvent) => {
    const el = targetRef.value;
    if (!el) return;
    if (event.target instanceof Node && !el.contains(event.target)) {
      handler(event);
    }
  };

  const escListener = (event: KeyboardEvent) => {
    if (event.key === 'Escape') {
      const ev = new MouseEvent('click');
      handler(ev);
    }
  };

  onMounted(() => {
    document.addEventListener('mousedown', listener);
    document.addEventListener('touchstart', listener);
    document.addEventListener('keydown', escListener);
  });

  onBeforeUnmount(() => {
    document.removeEventListener('mousedown', listener);
    document.removeEventListener('touchstart', listener);
    document.removeEventListener('keydown', escListener);
  });
}
