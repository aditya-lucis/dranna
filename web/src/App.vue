<template>
  <div class="min-h-screen bg-stone-100 dark:bg-stone-950 text-stone-800 dark:text-stone-100 font-sans transition-colors duration-300">
    <!-- Navbar Pendamping -->
    <header class="sticky top-0 z-30 bg-white/80 dark:bg-stone-900/80 backdrop-blur-md border-b border-stone-200 dark:border-stone-800 px-4 py-3">
      <div class="max-w-6xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-3">
          <img
            src="/assets/img/01134ab7-5052-4e91-9d6a-7753694fe140.webp"
            alt="Dr. Anna Reed"
            class="w-9 h-9 rounded-full object-cover object-top border-2 border-rose-400 shadow-sm"
          />
          <div>
            <h1 class="text-sm font-bold tracking-tight text-stone-900 dark:text-stone-100 flex items-center gap-1.5">
              Dr. Anna Reed
              <span class="text-[10px] px-2 py-0.5 rounded-full bg-rose-100 dark:bg-rose-950 text-rose-700 dark:text-rose-300 font-semibold uppercase">
                AI Companion
              </span>
            </h1>
            <p class="text-[11px] text-stone-500 dark:text-stone-400">
              Pendamping Emosional Klinis & Psikoedukasi
            </p>
          </div>
        </div>

        <!-- Tombol Aksi Kanan: Tool Tabs, TTS Toggle, Crisis SOS, Dark Mode -->
        <div class="flex items-center gap-2">
          <!-- Tombol SOS Krisis -->
          <button
            @click="modalKrisisTerbuka = true"
            class="px-3 py-1.5 rounded-xl bg-rose-500 hover:bg-rose-600 text-white font-bold text-xs flex items-center gap-1 shadow-sm transition"
            aria-label="Akses Bantuan Darurat"
          >
            <span>SOS</span>
            <span class="hidden sm:inline">Darurat</span>
          </button>

          <!-- Toggle Dark / Light -->
          <button
            @click="toggleDarkMode"
            class="p-2 rounded-xl bg-stone-100 dark:bg-stone-800 hover:bg-stone-200 dark:hover:bg-stone-700 text-stone-600 dark:text-stone-300 text-xs transition"
            :aria-label="isDarkMode ? 'Ganti ke Mode Terang' : 'Ganti ke Mode Gelap'"
          >
            {{ isDarkMode ? '☀️' : '🌙' }}
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="max-w-6xl mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Kolom Kiri: Chat Streaming Utama (7 Kolom) -->
      <section class="lg:col-span-7 flex flex-col h-[78vh]">
        <ChatStream
          sesiId="sesi-klinis-resmi"
          @krisis-detected="handleKrisis"
          class="h-full"
        />
      </section>

      <!-- Kolom Kanan: Panel Toolkit Terapeutik & Regulasi (5 Kolom) -->
      <aside class="lg:col-span-5 flex flex-col space-y-4">
        <!-- Tab Selector Toolkit -->
        <div class="flex bg-stone-200 dark:bg-stone-800/80 p-1 rounded-2xl gap-1 text-xs font-semibold">
          <button
            v-for="tab in daftarTab"
            :key="tab.id"
            @click="tabAktif = tab.id"
            class="flex-1 py-2 rounded-xl transition text-center"
            :class="tabAktif === tab.id
              ? 'bg-white dark:bg-stone-900 text-rose-600 dark:text-rose-400 shadow-sm'
              : 'text-stone-600 dark:text-stone-400 hover:text-stone-800 dark:hover:text-stone-200'"
          >
            {{ tab.label }}
          </button>
        </div>

        <!-- Konten Tab Aktif -->
        <div class="flex-1">
          <!-- Tab 1: Napas 4-7-8 -->
          <BreathingCircle v-if="tabAktif === 'napas'" />

          <!-- Tab 2: Grounding 5-4-3-2-1 -->
          <GroundingSensory
            v-else-if="tabAktif === 'grounding'"
            @selesai="tabAktif = 'jurnal'"
          />

          <!-- Tab 3: Jurnal Mood -->
          <MoodJournal v-else-if="tabAktif === 'jurnal'" />
        </div>

        <!-- Info Keamanan & Privasi Ringkas -->
        <div class="p-3.5 bg-stone-50 dark:bg-stone-900/60 rounded-2xl border border-stone-200 dark:border-stone-800 text-[11px] text-stone-500 dark:text-stone-400 space-y-1">
          <p class="flex items-center gap-1.5 font-medium text-stone-700 dark:text-stone-300">
            <span>🔒</span> Kerahasiaan Terjamin (UU PDP / GDPR Compliant)
          </p>
          <p>
            Data diproses privat dengan enkripsi lokal. Dr. Anna Reed bukan pengganti terapi medis atau psikiater.
          </p>
        </div>
      </aside>
    </main>

    <!-- Modal SOS Darurat -->
    <CrisisModal
      :isOpen="modalKrisisTerbuka"
      @close="modalKrisisTerbuka = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ChatStream from './components/ChatStream.vue'
import BreathingCircle from './components/BreathingCircle.vue'
import GroundingSensory from './components/GroundingSensory.vue'
import MoodJournal from './components/MoodJournal.vue'
import CrisisModal from './components/CrisisModal.vue'

const isDarkMode = ref(false)
const modalKrisisTerbuka = ref(false)
const tabAktif = ref('napas')

const daftarTab = [
  { id: 'napas', label: 'Napas 4-7-8' },
  { id: 'grounding', label: 'Grounding' },
  { id: 'jurnal', label: 'Jurnal Mood' },
]

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

const handleKrisis = () => {
  modalKrisisTerbuka.value = true
}

onMounted(() => {
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    isDarkMode.value = true
    document.documentElement.classList.add('dark')
  }
})
</script>
