<template>
    <div>
      <h1>Projet NoSQL</h1>
      <FormComponent />
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
  body {
    font-family: Arial, sans-serif;
    background-color: #f7f7f7;
    margin: 0;
    padding: 0;
  }
  h1 {
    text-align: center;
    color: #333;
  }
  </style>
  