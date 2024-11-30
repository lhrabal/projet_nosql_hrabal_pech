<template>
  <div class="page-container">
    <header class="header">
      <h1>Envoyer un Message</h1>
    </header>

    <main class="content">
      <section class="form-section">
        <form @submit.prevent="sendMessage" class="form">
          <label for="message" class="form-label">Message :</label>
          <input
            type="text"
            id="message"
            v-model="newMessage"
            placeholder="Saisissez votre message"
            required
            class="input"
          />
          <button type="submit" class="primary-button">Envoyer</button>
        </form>
      </section>

      <section class="action-section">
        <button @click="fetchData" class="secondary-button">
          Voir les données
        </button>
      </section>

      <section v-if="ESData || mongoData" class="data-section">
        <div class="card">
          <h3>Données postgres</h3>
          <table v-if="ESData" class="data-table">
            <thead>
              <tr>
                <th>Clé</th>
                <th>Valeur</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="content in ESData" :key="content.id">
                <td>{{ content.id }}</td>
                <td>{{ content.message }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="card">
          <h3>Données MongoDB</h3>
          <table v-if="mongoData" class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Message</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="content in mongoData" :key="content._id">
                <td>{{ content._id }}</td>
                <td>{{ content.message }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      newMessage: "",
      ESData: null,
      mongoData: null,
    };
  },
  methods: {
    async sendMessage() {
      try {
        await axios.post("http://localhost:8000/submit", {
          message: this.newMessage,
        });
        this.newMessage = "";
      } catch (error) {
        console.error("Erreur lors de l'envoi du message :", error);
      }
      this.fetchData();
    },
    async fetchData() {
      try {
        const ESResponse = await axios.get("http://localhost:8000/data/postgres");
        this.ESData = ESResponse.data.formongodbm_data;

        const mongoResponse = await axios.get("http://localhost:8000/data/mongodb");
        this.mongoData = mongoResponse.data.form_data;
      } catch (error) {
        console.error("Erreur lors de la récupération des données :", error);
      }
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
/* Global Styles */
body {
  font-family: 'Roboto', sans-serif;
  margin: 0;
  background-color: #f9fafc;
  color: #333;
}

/* Page Container */
.page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  box-sizing: border-box;
}

/* Header */
.header {
  background-color: #6200ea;
  color: white;
  width: 100%;
  padding: 20px 0;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header h1 {
  margin: 0;
  font-size: 24px;
}

/* Form Section */
.form-section {
  width: 100%;
  max-width: 500px;
  margin-bottom: 20px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-label {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  width: 100%;
}

/* Buttons */
.primary-button,
.secondary-button {
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.primary-button {
  background-color: #6200ea;
}

.primary-button:hover {
  background-color: #3700b3;
}

.secondary-button {
  background-color: #03dac6;
}

.secondary-button:hover {
  background-color: #018786;
}

/* Data Section */
.data-section {
  width: auto; /* Permet au conteneur de s'ajuster automatiquement */
  max-width: 1000px;
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap; /* Permet d'empiler les éléments s'ils débordent */
  gap: 20px;
  justify-content: center; /* Centre les cartes dans la section */
}

.card {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  flex: 1; /* Permet à chaque carte de prendre une largeur équivalente */
  min-width: 300px;
}

.card h3 {
  margin-top: 0;
  font-size: 18px;
  color: #6200ea;
}

/* Tables */
.data-table {
  width: auto; /* S'adapte automatiquement à la taille du contenu */
  border-collapse: collapse;
  margin-top: 10px;
}

.data-table th,
.data-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}

.data-table th {
  background-color: #f4f4f9;
  color: #333;
}

.data-table tr:nth-child(even) {
  background-color: #f9f9f9;
}
</style>
