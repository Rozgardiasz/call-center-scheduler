<template>
    <div class="bg-primary text-white d-flex align-items-center justify-content-center my-5 mx-5 p-5" style="height: 70vh;">
      <div>
        <h1>Welcome, {{ employeeName }}!</h1>
        <p>You have {{ availableVacationDays }} vacation days available.</p>
        <p>Your next vacation starts on: {{ nextVacationDate }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'InfoComponent',
    data() {
      return {
        employeeName: 'John Doe', // Przykładowa nazwa użytkownika, można zastąpić rzeczywistą
        availableVacationDays: 15, // Przykładowa liczba dni urlopu
        nextVacationDate: 'June 10, 2024' // Przykładowa data następnego urlopu
      };
    }
  }
  </script>
  
  <style scoped>
  /* Stylizacja opcjonalna dla InfoComponent */
  h1 {
    margin-bottom: 10px;
  }
  
  p {
    margin: 0;
    margin-bottom: 10px;
  }
  </style>
  