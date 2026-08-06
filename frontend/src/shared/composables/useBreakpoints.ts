import { ref, onMounted, onBeforeUnmount, computed } from 'vue'

export function useBreakpoints() {
  const windowWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1024)

  const onResize = () => {
    windowWidth.value = window.innerWidth
  }

  onMounted(() => {
    window.addEventListener('resize', onResize, { passive: true })
  })

  onBeforeUnmount(() => {
    window.removeEventListener('resize', onResize)
  })

  const isMobile = computed(() => windowWidth.value < 768)
  const isTablet = computed(() => windowWidth.value >= 768 && windowWidth.value < 992)
  const isDesktop = computed(() => windowWidth.value >= 992)
  const isLg = computed(() => windowWidth.value >= 992)
  const isXl = computed(() => windowWidth.value >= 1200)

  return {
    windowWidth,
    isMobile,
    isTablet,
    isDesktop,
    isLg,
    isXl,
  }
}
