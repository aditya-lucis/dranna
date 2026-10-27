<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm transition-opacity"
    role="dialog"
    aria-modal="true"
    aria-labelledby="crisis-modal-title"
  >
    <div class="relative w-full max-w-md bg-white dark:bg-stone-900 rounded-3xl shadow-2xl border-2 border-rose-500 overflow-hidden transform transition-all p-6 text-stone-800 dark:text-stone-100">
      <!-- Header Peringatan -->
      <div class="flex items-center gap-3 mb-4">
        <div class="w-10 h-10 rounded-2xl bg-rose-100 dark:bg-rose-950 text-rose-600 flex items-center justify-center text-xl font-bold">
          !
        </div>
        <div>
          <h2 id="crisis-modal-title" class="text-base font-bold text-rose-600 dark:text-rose-400">
            Bantuan Darurat & Keselamatan
          </h2>
          <p class="text-xs text-stone-500 dark:text-stone-400">
            Kamu tidak sendirian. Bantuan manusia profesional tersedia sekarang.
          </p>
        </div>
      </div>

      <!-- Pesan Klinis Empatik -->
      <div class="bg-rose-50/70 dark:bg-rose-950/40 p-3.5 rounded-2xl border border-rose-200 dark:border-rose-900 mb-5 text-xs leading-relaxed text-stone-700 dark:text-stone-200">
        <p>
          Sebagai pendamping digital, kapasitas teknologi ini memiliki batas nyata.
          <strong>Keselamatan fisikmu adalah hal yang paling berharga.</strong> Mohon hubungi salah satu layanan di bawah ini:
        </p>
      </div>

      <!-- Tombol Aksi Cepat One-Click Call -->
      <div class="space-y-2.5 mb-6">
        <a
          href="tel:119"
          class="flex items-center justify-between p-3.5 rounded-2xl bg-rose-500 hover:bg-rose-600 text-white font-medium text-xs transition shadow-md shadow-rose-500/20"
        >
          <div class="flex flex-col">
            <span class="font-bold text-sm">Layanan Sejiwa Kemenkes (119 ext 8)</span>
            <span class="text-[11px] text-rose-100">Konseling Krisis & Jiwa 24 Jam Bebas Pulsa</span>
          </div>
          <span class="text-lg">📞 Panggil</span>
        </a>

        <a
          href="tel:110"
          class="flex items-center justify-between p-3.5 rounded-2xl bg-stone-100 hover:bg-stone-200 dark:bg-stone-800 dark:hover:bg-stone-700 text-stone-800 dark:text-stone-100 text-xs font-medium transition border border-stone-200 dark:border-stone-700"
        >
          <div class="flex flex-col">
            <span class="font-bold">Kepolisian RI (110)</span>
            <span class="text-[11px] text-stone-500 dark:text-stone-400">Bantuan Keamanan Fisik Segera</span>
          </div>
          <span class="text-base">📞 Panggil</span>
        </a>

        <a
          href="tel:112"
          class="flex items-center justify-between p-3.5 rounded-2xl bg-stone-100 hover:bg-stone-200 dark:bg-stone-800 dark:hover:bg-stone-700 text-stone-800 dark:text-stone-100 text-xs font-medium transition border border-stone-200 dark:border-stone-700"
        >
          <div class="flex flex-col">
            <span class="font-bold">Panggilan Darurat Terpadu (112)</span>
            <span class="text-[11px] text-stone-500 dark:text-stone-400">Ambulans & Gawat Darurat</span>
          </div>
          <span class="text-base">📞 Panggil</span>
        </a>
      </div>

      <!-- Tombol Tutup / Kembali Bersama Anna -->
      <div class="flex justify-end">
        <button
          @click="tutup"
          class="px-5 py-2.5 rounded-xl bg-stone-200 hover:bg-stone-300 dark:bg-stone-800 dark:hover:bg-stone-700 text-stone-700 dark:text-stone-200 text-xs font-medium transition"
        >
          Aku Aman, Kembali Dampingi Aku
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close'])

const tutup = () => {
  emit('close')
}
</script>
