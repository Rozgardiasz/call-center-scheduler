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
      
      employeeName: sessionStorage.getItem('first_name') + ' ' + sessionStorage.getItem('last_name'),
      availableVacationDays: 0, // Przykładowa liczba dni urlopu
      nextVacationDate: '' // Przykładowa data następnego urlopu
    };
  },
  created() {
  // Możesz tutaj wykonać żądanie do backendu, aby pobrać liczbę dni urlopowych i datę najbliższego urlopu
  this.fetchVacationData();
},
methods: {
  async fetchVacationData() {
    const token = sessionStorage.getItem('token');
    try {
      const response = await fetch('http://127.0.0.1:8000/vacation_info', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch vacation data');
      }

      const data = await response.json();
      this.availableVacationDays = data.availableVacationDays;
      this.nextVacationDate = data.nextVacationDate ? new Date(data.nextVacationDate).toLocaleDateString() : 'No upcoming vacations';
    } catch (error) {
      console.error('Error fetching vacation data:', error);
    }
  }
}};

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

  