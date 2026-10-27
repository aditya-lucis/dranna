<template>
  <div class="mood-journal p-6 bg-white dark:bg-stone-800 rounded-2xl shadow-lg border border-stone-200 dark:border-stone-700 max-w-sm mx-auto">
    <div class="flex items-center justify-between mb-4 pb-2 border-b border-stone-100 dark:border-stone-700">
      <div>
        <h3 class="text-sm font-bold text-stone-800 dark:text-stone-100 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-rose-500"></span>
          Jurnal Emosi Harian
        </h3>
        <p class="text-[11px] text-stone-500 dark:text-stone-400">Refleksi Pribadi & Rasa Syukur</p>
      </div>
      <span class="text-xs text-stone-400 font-mono">{{ tanggalHariIni }}</span>
    </div>

    <!-- Slider Valence Mood -->
    <div class="mb-4">
      <div class="flex justify-between text-xs text-stone-600 dark:text-stone-300 font-medium mb-1">
        <span>Kondisi Hati:</span>
        <span class="font-bold text-rose-500">{{ labelMood }}</span>
      </div>
      <input
        v-model.number="moodValence"
        type="range"
        min="-1"
        max="1"
        step="0.1"
        class="w-full accent-rose-500 cursor-pointer"
        aria-label="Slider Kondisi Hati"
      />
      <div class="flex justify-between text-[10px] text-stone-400 mt-0.5">
        <span>Sangat Berat</span>
        <span>Netral</span>
        <span>Tenang & Bahagia</span>
      </div>
    </div>

    <!-- Catatan Refleksi Singkat -->
    <div class="mb-3">
      <label class="block text-xs font-medium text-stone-600 dark:text-stone-300 mb-1">
        Apa yang paling terasa hari ini?
      </label>
      <textarea
        v-model="catatan"
        rows="2"
        placeholder="Tuliskan perasaan atau peristiwa hari ini..."
        class="w-full bg-stone-50 dark:bg-stone-900 border border-stone-200 dark:border-stone-700 rounded-xl p-2.5 text-xs text-stone-800 dark:text-stone-100 focus:outline-none focus:ring-1 focus:ring-rose-400 resize-none"
      ></textarea>
    </div>

    <!-- Satu Hal yang Disyukuri (Gratitude) -->
    <div class="mb-4">
      <label class="block text-xs font-medium text-stone-600 dark:text-stone-300 mb-1">
        1 hal kecil yang kamu syukuri:
      </label>
      <input
        v-model="syukur"
        type="text"
        placeholder="misal: secangkir teh hangat, teman yang menyapa..."
        class="w-full bg-stone-50 dark:bg-stone-900 border border-stone-200 dark:border-stone-700 rounded-xl px-3 py-2 text-xs text-stone-800 dark:text-stone-100 focus:outline-none focus:ring-1 focus:ring-rose-400"
      />
    </div>

    <button
      @click="simpanJurnal"
      :disabled="!catatan.trim()"
      class="w-full py-2 rounded-xl bg-rose-500 hover:bg-rose-600 disabled:opacity-50 text-white font-medium text-xs transition shadow-sm"
    >
      {{ tersimpan ? '✓ Tersimpan di Perangkat' : 'Simpan Jurnal' }}
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const moodValence = ref(0.2)
const catatan = ref('')
const syukur = ref('')
const tersimpan = ref(false)

const tanggalHariIni = new Date().toLocaleDateString('id-ID', {
  day: 'numeric',
  month: 'short',
})

const labelMood = computed(() => {
  const v = moodValence.value
  if (v <= -0.5) return 'Sangat Tertekan'
  if (v < 0) return 'Sedikit Cemas / Lelah'
  if (v === 0) return 'Netral'
  if (v <= 0.5) return 'Tenang'
  return 'Sangat Bersyukur'
})

const simpanJurnal = () => {
  if (!catatan.value.trim()) return

  const entri = {
    tanggal: new Date().toISOString(),
    valence: moodValence.value,
    catatan: catatan.value,
    syukur: syukur.value,
  }

  try {
    const listLama = JSON.parse(localStorage.getItem('dranna_jurnal_mood') || '[]')
    listLama.push(entri)
    localStorage.setItem('dranna_jurnal_mood', JSON.stringify(listLama))
  } catch (e) {
    console.warn('Gagal simpan ke localStorage', e)
  }

  tersimpan.value = true
  setTimeout(() => {
    tersimpan.value = false
    catatan.value = ''
    syukur.value = ''
  }, 2000)
}
</script>
