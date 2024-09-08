<!-- src/views/LeaveApplication.vue -->
<template>
  <div class="auth-wrapper">
    <div class="auth-inner">
      <form @submit.prevent="submitLeaveRequest">
        <h1>Wnioski o Urlop</h1>

        <div class="form-group">
          <label for="leave-type">Typ Urlopu:</label>
          <select v-model="leaveType" id="leave-type" class="form-control">
            <option value="urlop">Urlop</option>
            <option value="dzień-wolny">Urlop </option>
          </select>
        </div>

        <div class="form-group">
          <label for="start-date">Data rozpoczęcia:</label>
          <input type="date" v-model="startDate" id="start-date" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="end-date">Data zakończenia:</label>
          <input type="date" v-model="endDate" id="end-date" class="form-control" required />
        </div>

        <button type="submit" class="btn btn-primary btn-block">Złóż Wniosek</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LeaveApplication',
  data() {
    return {
      leaveType: '',
      startDate: '',
      endDate: ''
    };
  },
  methods: {
    submitLeaveRequest() {
      alert('Wniosek o urlop został złożony.');
    }
  }
};
</script>

<style scoped>
.auth-wrapper {
  display: flex;
  min-width: 500px;
  align-items: center;
  justify-content: center;
  height: 70vh;
  background-color: #f7f7f7;
}

.auth-inner {
  background-color: #ffffff;
  padding: 50px;
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 500px;
  text-align: center; /* Wyśrodkowanie zawartości formularza */
}

h1 {
  margin-bottom: 30px;
  text-align: center;
  font-size: 2rem;
}

.form-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: center; /* Wyśrodkowanie elementów wewnątrz grupy formularza */
}

label {
  font-size: 1.2rem;
  margin-bottom: 8px;
  text-align: center;
}

input, select {
  width: 100%;
  max-width: 300px; /* Ustawienie maksymalnej szerokości pól */
  font-size: 1.2rem;
  padding: 10px;
  margin: 0 auto; /* Wyśrodkowanie pól */
}

.btn-block {
  width: 100%;
  padding: 15px;
  font-size: 1.2rem;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
}
</style>
