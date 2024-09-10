<template>
  <div class="auth-wrapper">
    <div class="auth-inner">
      <form @submit.prevent="submitLeaveRequest">
        <h1>Wnioski o Urlop</h1>

        <div class="form-group">
          <label for="leave-type">Typ Urlopu:</label>
          <select v-model="leaveType" id="leave-type" class="form-control" required>
            <option value="regular">Urlop</option>
            <option value="on_demand">Urlop NŻ</option>
          </select>
        </div>

        <div class="form-group">
          <label for="start-date">Data rozpoczęcia:</label>
          <input type="date" v-model="startDate" id="start-date" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="end-date">Data zakończenia:</label>
          <input
            type="date"
            v-model="endDate"
            id="end-date"
            class="form-control"
            required
            :min="startDate"
          />
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
    async submitLeaveRequest() {
      if (this.startDate && this.endDate && new Date(this.endDate) < new Date(this.startDate)) {
        alert('Data zakończenia nie może być wcześniejsza niż data rozpoczęcia.');
        return;
      }

      try {
        const requestData = {
          employee_id: 2, //placeholder
          vacation_start: this.startDate,
          vacation_end: this.endDate,
          type_of_vacation: this.leaveType
        };

        const response = await fetch('http://127.0.0.1:8000/holiday_request', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`
          },
          body: JSON.stringify(requestData)
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Wystąpił błąd podczas składania wniosku o urlop.');
        }

        alert('Wniosek o urlop został złożony pomyślnie.');
        
        this.leaveType = '';
        this.startDate = '';
        this.endDate = '';
      } catch (error) {
        alert(`Błąd: ${error.message}`);
      }
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
  margin-top: 50px;
}

.auth-inner {
  background-color: #ffffff;
  padding: 50px;
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 500px;
  text-align: center;
}

h1 {
  margin-bottom: 30px;
  text-align: center;
  font-size: 2rem;
}

.form-group {
  margin-bottom: 20px;
}

input {
  width: 100%;
  max-width: 300px;
  font-size: 1.2rem;
  padding: 10px;
  margin: 0 auto;
  border: 1px solid #ccc;
  border-radius: 4px;
}

input::placeholder {
  color: #888;
  font-size: 1.2rem;
}

.button-group {
  margin-top: 20px;
}

.btn-block {
  width: 100%;
  padding: 15px;
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
}

.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
}

.btn-secondary:hover {
  background-color: #5a6268;
  border-color: #545b62;
}
</style>
