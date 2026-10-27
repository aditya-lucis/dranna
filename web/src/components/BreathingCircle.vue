<template>
  <div class="breathing-widget flex flex-col items-center justify-center p-6 bg-white dark:bg-stone-800 rounded-2xl shadow-lg border border-stone-200 dark:border-stone-700 max-w-sm mx-auto text-center select-none">
    <div class="mb-4">
      <h3 class="text-base font-bold text-stone-800 dark:text-stone-100 flex items-center justify-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-teal-500 animate-pulse"></span>
        Napas Ritmis 4-7-8
      </h3>
      <p class="text-xs text-stone-500 dark:text-stone-400 mt-0.5">
        Siklus ke-{{ siklusKe }} • De-eskalasi Sistem Saraf
      </p>
    </div>

    <!-- Lingkaran Napas Visual dengan Transisi Dinamis -->
    <div class="relative w-48 h-48 flex items-center justify-center my-4">
      <!-- Outer Glow -->
      <div
        class="absolute inset-0 rounded-full transition-transform duration-1000 ease-in-out"
        :class="lingkaranClass"
      ></div>

      <!-- Center Content -->
      <div class="relative z-10 flex flex-col items-center">
        <span class="text-xs font-semibold uppercase tracking-wider text-teal-700 dark:text-teal-300">
          {{ labelFase }}
        </span>
        <span class="text-3xl font-extrabold text-stone-800 dark:text-stone-50 my-1 font-mono">
          {{ detikSisa }}s
        </span>
        <span class="text-[11px] text-stone-500 dark:text-stone-400 max-w-[120px] leading-tight">
          {{ instruksiSingkat }}
        </span>
      </div>
    </div>

    <!-- Kontrol Mulai / Berhenti -->
    <div class="flex items-center gap-2 mt-4">
      <button
        @click="toggleAktif"
        class="px-5 py-2 rounded-xl text-xs font-semibold transition-all shadow-sm"
        :class="isAktif
          ? 'bg-amber-500 hover:bg-amber-600 text-white'
          : 'bg-teal-600 hover:bg-teal-700 text-white'"
      >
        {{ isAktif ? 'Jeda Latihan' : 'Mulai Bernapas' }}
      </button>

      <button
        v-if="isAktif || detikTotal > 0"
        @click="resetLatihan"
        class="px-3 py-2 rounded-xl text-xs font-medium bg-stone-100 hover:bg-stone-200 dark:bg-stone-700 dark:hover:bg-stone-600 text-stone-600 dark:text-stone-300 transition"
      >
        Reset
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'

const props = defineProps({
  autoStart: {
    type: Boolean,
    default: false,
  },
})

const isAktif = ref(props.autoStart)
const detikTotal = ref(0)
const intervalId = ref(null)

const DURASI_TARIK = 4
const DURASI_TAHAN = 7
const DURASI_HEMBUS = 8
const DURASI_SIKLUS = DURASI_TARIK + DURASI_TAHAN + DURASI_HEMBUS // 19 detik

const siklusKe = computed(() => Math.floor(detikTotal.value / DURASI_SIKLUS) + 1)
const detikDalamSiklus = computed(() => detikTotal.value % DURASI_SIKLUS)

const faseAktif = computed(() => {
  const d = detikDalamSiklus.value
  if (d < DURASI_TARIK) return 'tarik'
  if (d < (DURASI_TARIK + DURASI_TAHAN)) return 'tahan'
  return 'hembus'
})

const detikSisa = computed(() => {
  const d = detikDalamSiklus.value
  if (faseAktif.value === 'tarik') return DURASI_TARIK - d
  if (faseAktif.value === 'tahan') return (DURASI_TARIK + DURASI_TAHAN) - d
  return DURASI_SIKLUS - d
})

const labelFase = computed(() => {
  if (faseAktif.value === 'tarik') return 'Tarik Napas'
  if (faseAktif.value === 'tahan') return 'Tahan Napas'
  return 'Hembuskan'
})

const instruksiSingkat = computed(() => {
  if (faseAktif.value === 'tarik') return 'Lewat hidung perlahan'
  if (faseAktif.value === 'tahan') return 'Tahan, rasakan hadir'
  return 'Lewat mulut lembut'
})

const lingkaranClass = computed(() => {
  if (!isAktif.value) return 'scale-90 bg-teal-100/60 dark:bg-teal-950/40 border-2 border-teal-300 dark:border-teal-800'
  if (faseAktif.value === 'tarik') {
    return 'scale-110 bg-teal-200/70 dark:bg-teal-900/60 border-4 border-teal-400 dark:border-teal-500 shadow-lg shadow-teal-500/20'
  }
  if (faseAktif.value === 'tahan') {
    return 'scale-110 bg-amber-200/70 dark:bg-amber-900/60 border-4 border-amber-400 dark:border-amber-500 shadow-lg shadow-amber-500/20'
  }
  return 'scale-75 bg-rose-200/70 dark:bg-rose-900/60 border-4 border-rose-400 dark:border-rose-500 shadow-md'
})

const toggleAktif = () => {
  isAktif.value = !isAktif.value
  if (isAktif.value) {
    intervalId.value = setInterval(() => {
      detikTotal.value += 1
    }, 1000)
  } else {
    clearInterval(intervalId.value)
    intervalId.value = null
  }
}

const resetLatihan = () => {
  clearInterval(intervalId.value)
  intervalId.value = null
  isAktif.value = false
  detikTotal.value = 0
}

onUnmounted(() => {
  if (intervalId.value) clearInterval(intervalId.value)
})
</script>
