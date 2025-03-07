<template>
  <div :class="['container', { dark: isDarkMode }]">
    <h1>Message Checker</h1>
    <button @click="toggleDarkMode">
      {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
    </button>
    <input v-model="message" placeholder="Masukkan teks..." aria-label="Input message" />
    <button @click="checkMessage" :disabled="loading" aria-busy="loading">
      <span v-if="loading">Loading...</span>
      <span v-else>Cek</span>
    </button>

    <div v-if="result" class="result-box" :style="{ borderColor: result.color, backgroundColor: result.color + '33' }">
      <p><strong>Pesan:</strong> {{ result.input_text }}</p>
      <p :style="{ color: result.color, fontWeight: 'bold' }">Terindikasi: {{ result.prediction }}</p>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      message: "",
      result: null,
      error: null,
      loading: false,
      isDarkMode: false,
    };
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
    },
    async checkMessage() {
      this.result = null;
      this.error = null;
      this.loading = true;

      if (!this.message) {
        this.error = "⚠️ Masukkan teks sebelum melakukan pengecekan!";
        this.loading = false;
        return;
      }

      try {
        const response = await axios.post("http://127.0.0.1:5000/predict", { text: this.message });
        if (response.data && response.data.input_text && response.data.prediction && response.data.color) {
          this.result = response.data;
        } else {
          this.error = "Data yang diterima tidak valid!";
        }
      } catch (err) {
        if (err.response) {
          this.error = `Error: ${err.response.status} - ${err.response.data.message}`;
        } else if (err.request) {
          this.error = "Tidak ada respon dari server!";
        } else {
          this.error = "Terjadi kesalahan saat memproses data!";
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style>
.container {
  max-width: 500px;
  margin: 0 auto;
  text-align: center;
}

input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  background-color: #FF4B4B;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover:enabled {
  background-color: #E04242;
}

.result-box {
  margin-top: 20px;
  padding: 15px;
  border-radius: 10px;
  border: 2px solid;
}

.error {
  color: red;
  margin-top: 10px;
}

.dark {
  background-color: #121212;
  color: #ffffff;
}

.dark input {
  background-color: #333333;
  color: #ffffff;
  border: 1px solid #555555;
}

.dark button {
  background-color: #444444;
}

.dark button:hover:enabled {
  background-color: #555555;
}

.dark .result-box {
  background-color: #333333;
  border-color: #555555;
}

.dark .error {
  color: #ff6666;
}
</style>