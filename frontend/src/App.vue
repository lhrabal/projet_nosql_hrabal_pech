<template>
  <div>
    <header>
      <h1>Projet NoSQL</h1>
    </header>
    <main>
      <FormComponent />
    </main>
    <footer>
      <p>© 2024 Projet NoSQL. Tous droits réservés.</p>
    </footer>
  </div>
</template>

<script>
import FormComponent from "./components/FormComponent.vue";

export default {
  components: {
    FormComponent,
  },
};
</script>

<style>
/* Styles globaux */
body {
  font-family: "Roboto", Arial, sans-serif;
  background-color: #f4f4f9;
  margin: 0;
  padding: 0;
  color: #333;
}

header {
  background-color: #6200ea;
  color: white;
  padding: 20px 0;
  text-align: center;
}

footer {
  background-color: #6200ea;
  color: white;
  text-align: center;
  padding: 10px 0;
  margin-top: 30px;
}

main {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
