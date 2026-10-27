<template>
  <div class="chat-stream-container flex flex-col h-full max-w-3xl mx-auto p-4 bg-stone-50 dark:bg-stone-900 rounded-2xl shadow-xl border border-stone-200 dark:border-stone-800">
    <!-- Header Pendamping dengan Avatar Synchronized -->
    <header class="flex items-center justify-between pb-4 border-b border-stone-200 dark:border-stone-800">
      <div class="flex items-center gap-4">
        <AnnaAvatar :status="avatarStatus" :mode="avatarMode" />
        <div>
          <h2 class="text-lg font-bold text-stone-800 dark:text-stone-100 flex items-center gap-2">
            Dr. Anna Reed
            <span class="text-xs px-2 py-0.5 rounded-full bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300 font-normal">
              {{ personaAktif }}
            </span>
          </h2>
          <p class="text-xs text-stone-500 dark:text-stone-400">
            Pendamping Emosional Klinis Berempati
          </p>
        </div>
      </div>

      <!-- Pengaturan Persona & Mode Tenang -->
      <div class="flex items-center gap-2">
        <select
          v-model="personaAktif"
          :disabled="isStreaming"
          class="text-xs bg-white dark:bg-stone-800 border border-stone-300 dark:border-stone-700 rounded-lg px-2 py-1 text-stone-700 dark:text-stone-200"
          aria-label="Pilih Persona Anna"
        >
          <option value="netral">Netral (Konselor)</option>
          <option value="waifu">Waifu (Penyayang)</option>
          <option value="sister">Sister (Kakak)</option>
        </select>

        <button
          @click="toggleModeTenang"
          :class="avatarMode === 'tenang' ? 'bg-amber-500 text-white' : 'bg-stone-200 dark:bg-stone-800 text-stone-700 dark:text-stone-300'"
          class="text-xs px-2 py-1 rounded-lg transition-colors font-medium"
          aria-label="Toggle Mode Tenang"
        >
          Mode Tenang
        </button>
      </div>
    </header>

    <!-- Area Percakapan -->
    <main
      ref="chatScrollRef"
      class="flex-1 overflow-y-auto py-4 space-y-4 pr-1"
      role="log"
      aria-live="polite"
    >
      <div
        v-for="(msg, idx) in daftarPesan"
        :key="idx"
        class="flex flex-col"
        :class="msg.role === 'user' ? 'items-end' : 'items-start'"
      >
        <div
          class="max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-sm"
          :class="msg.role === 'user'
            ? 'bg-rose-500 text-white rounded-br-sm'
            : 'bg-white dark:bg-stone-800 text-stone-800 dark:text-stone-100 border border-stone-200 dark:border-stone-700 rounded-bl-sm'"
        >
          <p class="whitespace-pre-wrap">{{ msg.teks }}</p>
        </div>
        <span class="text-[10px] text-stone-400 mt-1 px-1">
          {{ msg.role === 'user' ? 'Kamu' : 'Anna' }}
        </span>
      </div>

      <!-- Bubble Streaming Aktif -->
      <div v-if="isStreaming" class="flex flex-col items-start">
        <div class="max-w-[85%] rounded-2xl rounded-bl-sm px-4 py-3 text-sm leading-relaxed bg-white dark:bg-stone-800 text-stone-800 dark:text-stone-100 border border-rose-300 dark:border-rose-800 shadow-sm">
          <p class="whitespace-pre-wrap">
            {{ streamBuffer }}<span class="inline-block w-1.5 h-4 bg-rose-500 ml-0.5 animate-pulse"></span>
          </p>
        </div>
        <span class="text-[10px] text-rose-500 mt-1 px-1 flex items-center gap-1 font-medium">
          <span class="w-1.5 h-1.5 rounded-full bg-rose-500 animate-ping"></span>
          Anna sedang {{ statusTahap }}...
        </span>
      </div>
    </main>

    <!-- Footer Input Bar & Tombol Batal -->
    <footer class="pt-3 border-t border-stone-200 dark:border-stone-800">
      <form @submit.prevent="kirimPesan" class="flex gap-2">
        <input
          v-model="inputPesan"
          type="text"
          placeholder="Ceritakan apa yang sedang kamu rasakan..."
          :disabled="isStreaming"
          class="flex-1 bg-white dark:bg-stone-800 border border-stone-300 dark:border-stone-700 rounded-xl px-4 py-2.5 text-sm text-stone-800 dark:text-stone-100 focus:outline-none focus:ring-2 focus:ring-rose-400"
          aria-label="Input pesan konseling"
        />

        <button
          v-if="!isStreaming"
          type="submit"
          :disabled="!inputPesan.trim()"
          class="bg-rose-500 hover:bg-rose-600 disabled:opacity-50 text-white font-medium text-sm px-5 py-2.5 rounded-xl transition shadow"
        >
          Kirim
        </button>

        <button
          v-else
          type="button"
          @click="hentikanStream"
          class="bg-amber-500 hover:bg-amber-600 text-white font-medium text-sm px-4 py-2.5 rounded-xl transition shadow flex items-center gap-1"
          aria-label="Hentikan respons streaming"
        >
          <span>Jeda</span>
        </button>
      </form>
    </footer>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import AnnaAvatar from './AnnaAvatar.vue'

const props = defineProps({
  sesiId: {
    type: String,
    default: 'sesi-web-001',
  },
})

const emit = defineEmits(['status-change', 'krisis-detected'])

const daftarPesan = ref([
  {
    role: 'anna',
    teks: 'Halo, aku Dr. Anna Reed. Senang kamu berada di sini. Apa yang sedang kamu rasakan hari ini?',
  },
])

const inputPesan = ref('')
const personaAktif = ref('netral')
const isStreaming = ref(false)
const streamBuffer = ref('')
const statusTahap = ref('siap')
const avatarStatus = ref('idle')
const avatarMode = ref('normal')
const chatScrollRef = ref(null)

let abortController = null

const toggleModeTenang = () => {
  avatarMode.value = avatarMode.value === 'tenang' ? 'normal' : 'tenang'
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatScrollRef.value) {
    chatScrollRef.value.scrollTop = chatScrollRef.value.scrollHeight
  }
}

const kirimPesan = async () => {
  const teks = inputPesan.value.trim()
  if (!teks || isStreaming.value) return

  daftarPesan.value.push({ role: 'user', teks })
  inputPesan.value = ''
  streamBuffer.value = ''
  isStreaming.value = true
  statusTahap.value = 'mendengarkan'
  avatarStatus.value = 'mendengarkan'
  await scrollToBottom()

  abortController = new AbortController()

  try {
    const url = `/api/v1/sesi/${props.sesiId}/stream?pesan=${encodeURIComponent(teks)}&persona=${personaAktif.value}`
    const response = await fetch(url, {
      signal: abortController.signal,
      headers: { Accept: 'text/event-stream' },
    })

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let bufferTeks = ''

    while (true) {
      const { value, done } = await reader.read()
      if (done) break

      bufferTeks += decoder.decode(value, { stream: true })
      const lines = bufferTeks.split('\n\n')
      bufferTeks = lines.pop() // simpan bagian sisa yang belum lengkap

      for (const line of lines) {
        if (!line.trim()) continue
        const eventMatch = line.match(/^event:\s*(\w+)/m)
        const dataMatch = line.match(/^data:\s*(.+)$/m)
        if (!dataMatch) continue

        const eventName = eventMatch ? eventMatch[1] : 'message'
        try {
          const payload = JSON.parse(dataMatch[1])
          handleStreamEvent(eventName, payload)
        } catch (err) {
          console.warn('Gagal parse SSE payload', err)
        }
      }
    }
  } catch (err) {
    if (err.name !== 'AbortError') {
      streamBuffer.value += '\n[Koneksi terputus. Anna tetap di sini mendampingimu.]'
    }
  } finally {
    if (streamBuffer.value) {
      daftarPesan.value.push({ role: 'anna', teks: streamBuffer.value })
    }
    isStreaming.value = false
    streamBuffer.value = ''
    avatarStatus.value = 'selesai'
    statusTahap.value = 'siap'
    await scrollToBottom()
  }
}

const handleStreamEvent = (eventName, data) => {
  if (eventName === 'status') {
    statusTahap.value = data.tahap || 'proses'
    avatarStatus.value = data.tahap || 'menyiapkan'
    emit('status-change', data)
  } else if (eventName === 'chunk') {
    avatarStatus.value = 'menulis'
    streamBuffer.value += data.teks || ''
    scrollToBottom()
  } else if (eventName === 'reflection') {
    if (data.masalah && data.masalah.includes('krisis_darurat_dialihkan')) {
      emit('krisis-detected', data)
    }
  } else if (eventName === 'selesai') {
    avatarStatus.value = 'selesai'
  }
}

const hentikanStream = () => {
  if (abortController) {
    abortController.abort()
    abortController = null
  }
  isStreaming.value = false
  avatarStatus.value = 'jeda'
}
</script>
