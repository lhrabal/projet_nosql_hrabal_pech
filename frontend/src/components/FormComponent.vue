<template>
  <div>
    <h1>Envoyer un Message</h1>
    
    <!-- Formulaire pour envoyer un message -->
    <form @submit.prevent="sendMessage">
      <label for="message">Message:</label>
      <input type="text" id="message" v-model="newMessage" required />
      <button type="submit">Envoyer</button>
    </form>

    <!-- Bouton pour voir les données de Redis et MongoDB -->
    <button @click="fetchData">Voir les données</button>
    
    <!-- Affichage des données Redis et MongoDB -->
    <div v-if="redisData || mongoData">
      <h2>Données Redis</h2>
      <table v-if="redisData">
        <thead>
          <tr>
            <th>Clé</th>
            <th>Valeur</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(msg, key) in redisData" :key="key">
            <td>{{ key }}</td>
            <td>{{ msg }}</td>
          </tr>
        </tbody>
      </table>
      
      <h2>Données MongoDB</h2>
      <table v-if="mongoData">
        <thead>
          <tr>
            <th>ID</th>
            <th>Données</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(content, id) in mongoData" :key="id">
            <td>{{ content._id }}</td>
            <td>{{ content.message }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>Aucune donnée à afficher.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      newMessage: "",
      redisData: null,
      mongoData: null,
    };
  },
  methods: {
    async sendMessage() {
      // Envoyer le message au backend avec Axios
      try {
        const response = await axios.post("http://localhost:8000/submit", {
          message: this.newMessage,
        });
        console.log(response.data);

        // Rafraîchir les données de Redis et MongoDB après l'ajout
        this.fetchData();
        
        // Réinitialiser le champ de message
        this.newMessage = "";
      } catch (error) {
        console.error("Erreur lors de l'envoi du message:", error);
      }
    },

    async fetchData() {
      try {
        // Récupérer les données Redis
        const redisResponse = await axios.get("http://localhost:8000/data/redis");
        this.redisData = redisResponse.data;

        // Récupérer les données MongoDB
        const mongoResponse = await axios.get("http://localhost:8000/data/mongodb");
        this.mongoData = mongoResponse.data.data;
        console.log(this.mongoData)
      } catch (error) {
        console.error("Erreur lors de la récupération des données:", error);
      }
    },
  },
  filters: {
    json(value) {
      return JSON.stringify(value, null, 2); // Formater l'objet en JSON lisible
    },
  },
  mounted() {
    // Charger les données dès que le composant est monté
    this.fetchData();
  },
};
</script>

<style scoped>
/* Style de la page */
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 30px;
}
table, th, td {
  border: 1px solid #ddd;
}
th, td {
  padding: 10px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
}
button {
  margin-bottom: 20px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #45a049;
}
form {
  margin-bottom: 20px;
}
form input {
  padding: 8px;
  font-size: 16px;
  margin-right: 10px;
  border: 1px solid #ccc;
}
form button {
  padding: 10px 15px;
  font-size: 16px;
}
</style>
