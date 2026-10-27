<template>
  <div class="grounding-card p-6 bg-white dark:bg-stone-800 rounded-2xl shadow-lg border border-stone-200 dark:border-stone-700 max-w-sm mx-auto">
    <div class="flex items-center justify-between mb-4 pb-2 border-b border-stone-100 dark:border-stone-700">
      <div>
        <h3 class="text-sm font-bold text-stone-800 dark:text-stone-100 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
          Grounding Sensori 5-4-3-2-1
        </h3>
        <p class="text-[11px] text-stone-500 dark:text-stone-400">Jangkar Saat Ini & Di Sini</p>
      </div>
      <span class="text-xs font-mono font-bold px-2 py-0.5 rounded-full bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300">
        {{ langkahAktif.langkah }} / 5
      </span>
    </div>

    <!-- Konten Langkah Sensori -->
    <div class="my-4">
      <div class="flex items-center gap-2 mb-2">
        <span class="text-2xl font-black text-indigo-600 dark:text-indigo-400 font-mono">
          {{ langkahAktif.target_jumlah }}
        </span>
        <span class="text-xs uppercase font-bold tracking-wider text-stone-600 dark:text-stone-300">
          Hal yang di-{{ langkahAktif.indra }}
        </span>
      </div>

      <p class="text-xs text-stone-700 dark:text-stone-200 leading-relaxed mb-3">
        {{ langkahAktif.instruksi }}
      </p>

      <!-- Contoh Bantuan -->
      <div class="bg-stone-50 dark:bg-stone-900/60 p-3 rounded-xl border border-stone-200 dark:border-stone-700/60">
        <span class="text-[10px] font-semibold text-stone-400 uppercase tracking-wider block mb-1">
          Contoh Pengamatan:
        </span>
        <ul class="text-[11px] text-stone-600 dark:text-stone-300 space-y-0.5 list-disc list-inside">
          <li v-for="(c, idx) in langkahAktif.contoh" :key="idx">{{ c }}</li>
        </ul>
      </div>
    </div>

    <!-- Tombol Navigasi Langkah -->
    <div class="flex items-center justify-between mt-5 pt-3 border-t border-stone-100 dark:border-stone-700">
      <button
        v-if="indeksLangkah > 0"
        @click="kembaliLangkah"
        class="text-xs px-3 py-1.5 rounded-lg text-stone-500 hover:text-stone-700 dark:hover:text-stone-300 transition"
      >
        Sebelumnya
      </button>
      <div v-else></div>

      <button
        @click="lanjutLangkah"
        class="text-xs font-semibold px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white transition shadow-sm"
      >
        {{ isSelesai ? 'Selesai Latihan' : 'Langkah Berikutnya →' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const emit = defineEmits(['selesai'])

const DAFTAR_LANGKAH = [
  {
    langkah: 1,
    indra: 'LIHAT',
    target_jumlah: 5,
    instruksi: 'Sebutkan atau perhatikan 5 benda yang kamu lihat di sekitarmu saat ini.',
    contoh: ['Warna dinding', 'Layar monitor', 'Buku di meja', 'Jendela', 'Lampu ruangan'],
  },
  {
    langkah: 2,
    indra: 'SENTUH',
    target_jumlah: 4,
    instruksi: 'Rasakan 4 hal fisik yang sedang bersentuhan dengan tubuhmu.',
    contoh: ['Telapak kaki di lantai', 'Kain pakaianmu', 'Permukaan meja', 'Kesejukan udara'],
  },
  {
    langkah: 3,
    indra: 'DENGAR',
    target_jumlah: 3,
    instruksi: 'Dengarkan 3 suara berbeda yang terdengar di sekelilingmu.',
    contoh: ['Dengungan AC/Kipas', 'Suara kendaraan di luar', 'Suara hembusan napasmu'],
  },
  {
    langkah: 4,
    indra: 'CIUM',
    target_jumlah: 2,
    instruksi: 'Tarik napas dan sadari 2 aroma di sekitarmu.',
    contoh: ['Aroma kopi atau teh', 'Wangi sabun atau udara ruangan'],
  },
  {
    langkah: 5,
    indra: 'RASA',
    target_jumlah: 1,
    instruksi: 'Sadarilah 1 sensasi rasa di dalam mulut atau lidahmu.',
    contoh: ['Rasa air minum', 'Sensasi bersih segar di langit-langit mulut'],
  },
]

const indeksLangkah = ref(0)
const langkahAktif = computed(() => DAFTAR_LANGKAH[indeksLangkah.value])
const isSelesai = computed(() => indeksLangkah.value === DAFTAR_LANGKAH.length - 1)

const lanjutLangkah = () => {
  if (indeksLangkah.value < DAFTAR_LANGKAH.length - 1) {
    indeksLangkah.value += 1
  } else {
    emit('selesai')
    indeksLangkah.value = 0
  }
}

const kembaliLangkah = () => {
  if (indeksLangkah.value > 0) {
    indeksLangkah.value -= 1
  }
}
</script>
