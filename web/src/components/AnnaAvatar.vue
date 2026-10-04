<template>
  <div
    class="relative inline-flex flex-col items-center select-none"
    role="img"
    :aria-label="currentEkspresi.padanan_teks"
  >
    <!-- Frame Avatar Visual dengan Gambar Kanon Dr. Anna Reed -->
    <div
      class="relative w-36 h-36 md:w-44 md:h-44 rounded-full overflow-hidden border-2 shadow-md transition-all duration-300"
      :class="borderClass"
    >
      <!-- Gambar Kanon (Pose Standby Kacamata vs Fokus Lepas Kacamata) -->
      <img
        :src="gambarPose"
        :alt="currentEkspresi.padanan_teks"
        class="w-full h-full object-cover object-top transition-transform duration-500"
        :class="animasiPoseClass"
      />

      <!-- Badge Indikator Status di Atas Avatar -->
      <div
        class="absolute bottom-1 right-1 px-2 py-0.5 rounded-full text-xs font-medium tracking-wide flex items-center gap-1 shadow"
        :class="badgeClass"
      >
        <span class="w-1.5 h-1.5 rounded-full animate-pulse" :class="dotClass"></span>
        <span>{{ statusLabel }}</span>
      </div>
    </div>

    <!-- Teks Aksesibel untuk Screen Reader (Invarian Aksesibilitas) -->
    <span class="sr-only">{{ currentEkspresi.padanan_teks }}</span>

    <!-- Status Teks Terbaca Manusia -->
    <div class="mt-2 text-center text-xs text-stone-600 dark:text-stone-300 font-medium">
      {{ currentEkspresi.padanan_teks }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    default: 'idle',
  },
  mode: {
    type: String,
    default: 'normal', // 'normal' | 'tenang' | 'reduced'
  },
})

// Pemetaan ekspresi ke padanan teks aksesibel
const EKSPRESI_MAP = {
  siap: { nama: 'siap', padanan_teks: 'Anna siap menemani' },
  mendengar: { nama: 'mendengar', padanan_teks: 'Anna mendengarkan' },
  menyusun: { nama: 'menyusun', padanan_teks: 'Anna menyusun respons' },
  menulis: { nama: 'menulis', padanan_teks: 'Anna menulis' },
  tenang: { nama: 'tenang', padanan_teks: 'Anna hadir, tenang' },
  perhatian: { nama: 'perhatian', padanan_teks: 'Anna perhatian penuh' },
  jeda: { nama: 'jeda', padanan_teks: 'Anna berjeda' },
}

const currentEkspresi = computed(() => {
  if (props.mode === 'tenang') {
    return EKSPRESI_MAP.tenang
  }
  if (props.status === 'mendengarkan') return EKSPRESI_MAP.mendengar
  if (props.status === 'menyiapkan') return EKSPRESI_MAP.menyusun
  if (props.status === 'menulis') return EKSPRESI_MAP.menulis
  if (props.status === 'selesai') return EKSPRESI_MAP.jeda
  return EKSPRESI_MAP.siap
})

// Pemilihan pose kanon Dr. Anna Reed
const gambarPose = computed(() => {
  // Pose 2 (tatap langsung lepas kacamata) untuk mendengarkan mendalam / mode tenang
  if (props.mode === 'tenang' || props.status === 'mendengarkan') {
    return '/assets/img/44485f8a-4449-4275-975b-e84db6ed1be9.webp'
  }
  // Pose 1 (kacamata terpasang) untuk standby / menulis
  return '/assets/img/01134ab7-5052-4e91-9d6a-7753694fe140.webp'
})

const borderClass = computed(() => {
  if (props.mode === 'tenang') return 'border-amber-400/80 bg-amber-50 dark:bg-stone-900'
  return 'border-rose-300 dark:border-rose-900/50 bg-rose-50/50 dark:bg-stone-900'
})

const animasiPoseClass = computed(() => {
  if (props.mode === 'reduced') return ''
  if (props.status === 'menulis') return 'scale-105 transition-transform'
  return 'hover:scale-102'
})

const badgeClass = computed(() => {
  if (props.mode === 'tenang') return 'bg-amber-100 text-amber-900 border border-amber-300'
  return 'bg-rose-100 text-rose-900 border border-rose-200'
})

const dotClass = computed(() => {
  if (props.mode === 'tenang') return 'bg-amber-500'
  return 'bg-rose-500'
})

const statusLabel = computed(() => {
  if (props.mode === 'tenang') return 'Mode Tenang'
  return props.status
})
</script>
