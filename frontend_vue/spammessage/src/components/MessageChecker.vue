<template>
  <div :class="['container', { dark: isDarkMode }]">
    <h1>Message Checker</h1>
    
    <!-- Tombol Mode Gelap -->
    <button @click="toggleDarkMode">
      {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
    </button>

    <!-- Input & Button -->
    <div class="input-container">
      <input v-model="message" placeholder="Masukkan teks..." />
      <button @click="checkMessage" class="check-btn">Cek</button>
    </div>

    <!-- Hasil Prediksi -->
    <div v-if="result" class="result-box" :style="{ borderColor: result.color, backgroundColor: result.color + '33' }">
      <p><strong>Pesan:</strong> {{ result.input_text }}</p>
      <p :style="{ color: result.color, fontWeight: 'bold' }">Terindikasi: {{ result.prediction }}</p>
    </div>

    <!-- Pesan Error -->
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

      if (!this.message) {
        this.error = "⚠️ Masukkan teks sebelum melakukan pengecekan!";
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
      }
    },
  },
};
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

.container {
  max-width: 500px;
  margin: 20px auto;
  text-align: center;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  transition: all 0.3s ease-in-out;
}

h1 {
  margin-bottom: 15px;
}

/* Input dan Tombol */
.input-container {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

input {
  flex: 1;
  padding: 12px;
  border: 2px solid #ccc;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #FF4B4B;
}

.check-btn {
  padding: 12px 20px;
  background-color: #FF4B4B;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.check-btn:hover {
  background-color: #E04242;
}

.result-box {
  margin-top: 20px;
  padding: 20px;
  border-radius: 10px;
  border: 2px solid;
  font-size: 18px;
  font-weight: bold;
}

/* Error */
.error {
  color: red;
  margin-top: 10px;
  font-size: 14px;
}

/* 🌙 DARK MODE */
.dark {
  background-color: #121212;
  color: #ffffff;
  padding: auto;
  border-radius: auto;
}

.dark input {
  background-color: #333;
  color: white;
  border: 2px solid #555;
  padding: 12px;
}

.dark .check-btn {
  background-color: #555;
}

.dark .check-btn:hover {
  background-color: #777;
}

.dark .result-box {
  background-color: #222;
  border-color: #666;
  padding: 20px;
}

.dark .error {
  color: #ff6666;
}
</style>
