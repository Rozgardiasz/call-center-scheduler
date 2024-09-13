<template>
  <div class="page-container">
    <!-- Panel dodawania przeciwnika po lewej, zajmuje 25% wysokości -->
    <div class="add-employee-panel">
      <h1>Dodaj Pracownika</h1>
      <form @submit.prevent="addEmployee">
        <div class="form-group">
          <input
            v-model="newEmployee.name"
            placeholder="Imię i nazwisko"
            class="form-control"
            required
          />
        </div>

        <div class="form-group">
          <input
            v-model="newEmployee.email"
            type="email"
            placeholder="Adres e-mail"
            class="form-control"
            required
          />
        </div>

        <div class="form-group">
          <input
            v-model="newEmployee.password"
            type="password"
            placeholder="Hasło"
            class="form-control"
            required
          />
        </div>

        <div class="form-group">
          <input
            v-model="newEmployee.confirmPassword"
            type="password"
            placeholder="Powtórz Hasło"
            class="form-control"
            required
          />
        </div>

        <!-- Ustawienia godzin pracy dla każdego dnia tygodnia -->
        <div class="working-hours">
          <h2>Godziny pracy</h2>
          <div v-for="day in daysOfWeek" :key="day" class="day-row">
            <label>{{ day }}:</label>
            <select v-model="newEmployee.workingHours[day].start" class="form-control">
              <option v-for="hour in hours" :key="hour" :value="hour">{{ hour }}</option>
            </select>
            <select v-model="newEmployee.workingHours[day].duration" class="form-control">
              <option value="4">4h</option>
              <option value="8">8h</option>
            </select>
          </div>
        </div>

        <button type="submit" class="btn btn-primary btn-block">Dodaj Pracownika</button>
      </form>
    </div>

    <!-- Lista pracowników po prawej, zajmuje 75% szerokości -->
    <div class="employee-list-panel">
      <h1>Lista Pracowników</h1>
      <ul class="employee-list">
        <li v-for="(employee, index) in employees" :key="index" class="employee-item">
          {{ employee.first_name }} {{ employee.last_name }} ({{ employee.email }})
          <button @click="confirmRemoveEmployee(index)" class="btn btn-danger">Usuń</button>
        </li>
      </ul>
    </div>

    <!-- Modal potwierdzenia usunięcia -->
    <div v-if="showConfirmModal" class="confirm-modal">
      <div class="confirm-modal-content">
        <p>Czy na pewno chcesz usunąć tego pracownika?</p>
        <button @click="removeEmployee(confirmedIndex)" class="btn btn-danger">Tak</button>
        <button @click="cancelRemoveEmployee" class="btn btn-secondary">Anuluj</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ManageEmployees',
  data() {
    return {
      newEmployee: {
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
        workingHours: {
          Mon: { start: '', duration: '8' },
          Tue: { start: '', duration: '8' },
          Wed: { start: '', duration: '8' },
          Thu: { start: '', duration: '8' },
          Fri: { start: '', duration: '8' },
          Sat: { start: '', duration: '8' },
          Sun: { start: '', duration: '8' }
        }
      },
      employees: [],  // Store the list of employees here
      showConfirmModal: false,
      confirmedIndex: null,
      daysOfWeek: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      hours: Array.from({ length: 24 }, (v, k) => `${k}:00`) // Generates hours from 0:00 to 23:00
    };
  },
  mounted() {
    this.fetchEmployees();  // Fetch employees when the component is mounted
  },
  methods: {
    async fetchEmployees() {
      try {
        const response = await fetch('http://127.0.0.1:8000/admin/users', {
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`
          }
        });
        if (response.ok) {
          this.employees = await response.json();
        } else {
          throw new Error('Failed to fetch employees');
        }
      } catch (error) {
        alert(`Error: ${error.message}`);
      }
    },
    calculateEndTime(startTime, duration) {
      const [hours, minutes] = startTime.split(':').map(Number);
      const endHours = (hours + Number(duration)) % 24;  // Handle overflow of 24 hours
      return `${endHours < 10 ? '0' : ''}${endHours}:${minutes < 10 ? '0' : ''}${minutes}`;
    },
    resetForm() {
      this.newEmployee.name = '';
      this.newEmployee.email = '';
      this.newEmployee.password = '';
      this.newEmployee.confirmPassword = '';
      this.newEmployee.workingHours = {
        Mon: { start: '', duration: '8' },
        Tue: { start: '', duration: '8' },
        Wed: { start: '', duration: '8' },
        Thu: { start: '', duration: '8' },
        Fri: { start: '', duration: '8' },
        Sat: { start: '', duration: '8' },
        Sun: { start: '', duration: '8' }
      };
    },
    async addEmployee() {
      if (this.newEmployee.name && this.newEmployee.email && this.newEmployee.password) {
        if (this.newEmployee.password === this.newEmployee.confirmPassword) {
          try {
            const employeeData = {
              first_name: this.newEmployee.name.split(' ')[0],
              last_name: this.newEmployee.name.split(' ')[1] || '',
              email: this.newEmployee.email,
              password: this.newEmployee.password,
              work_hours: this.getWorkHoursWithEndTimes()  // Now includes end times
            };

            const response = await fetch('http://127.0.0.1:8000/admin/add_user', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${sessionStorage.getItem('token')}`
              },
              body: JSON.stringify(employeeData)
            });

            if (!response.ok) {
              throw new Error('Error adding employee');
            }

            const data = await response.json();
            this.employees.push(data);
            this.resetForm();
            alert('Employee added successfully');
          } catch (error) {
            alert(`Error: ${error.message}`);
          }
        } else {
          alert('Passwords do not match!');
        }
      } else {
        alert('All fields are required!');
      }
    },
    getWorkHoursWithEndTimes() {
      return Object.keys(this.newEmployee.workingHours).map(day => {
        const workHour = this.newEmployee.workingHours[day];
        if (!workHour.start) {
          return { weekday: day, start_time: null, end_time: null };
        }
        return {
          weekday: day,
          start_time: workHour.start,
          end_time: this.calculateEndTime(workHour.start, workHour.duration)
        };
      }).filter(day => day.start_time && day.end_time);
    },
    confirmRemoveEmployee(index) {
      this.confirmedIndex = index;
      this.showConfirmModal = true;
    },
    async removeEmployee(index) {
      const employee = this.employees[index];
      try {
        const response = await fetch(`http://127.0.0.1:8000/admin/remove_user/${employee.id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`
          }
        });
        if (!response.ok) {
          throw new Error('Error removing employee');
        }
        this.employees.splice(index, 1);
        this.showConfirmModal = false;
        alert('Employee removed successfully');
      } catch (error) {
        alert(`Error: ${error.message}`);
      }
    },
    cancelRemoveEmployee() {
      this.confirmedIndex = null;
      this.showConfirmModal = false;
    }
  }
};

</script>


<style scoped>
.page-container {
  display: flex;
  margin-top: 250px; /* Adjust top margin as needed */
  height: 100vh; /* Full height of the viewport */
  background-color: #f7f7f7;
}

.add-employee-panel {
  flex-basis: 30%;
  flex-grow: 1;
  padding: 30px;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  border-right: 1px solid #ddd;
  overflow-y: auto; /* Enable scrolling if content overflows */
}

.employee-list-panel {
  flex-basis: 70%;
  flex-grow: 1;
  padding: 20px;
  background-color: #f1f1f1;
  overflow-y: auto; /* Enable scrolling if content overflows */
}

.employee-list-panel h1 {
  text-align: left;
  margin-bottom: 20px;
}

.employee-list {
  list-style: none;
  padding: 0;
}

.employee-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
}

h1 {
  margin-bottom: 20px;
  text-align: center;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 15px;
  width: 100%;
}

input, select {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 10px;
}

.btn-block {
  width: 100%;
  padding: 10px;
  font-size: 1.1rem;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
}

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.working-hours {
  margin-top: 10px;
  max-width: 300px;
  width: 100%;
}

.day-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.day-row label {
  flex: 1;
  margin-right: 10px;
}

.day-row select {
  flex: 2;
}

.confirm-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.confirm-modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.confirm-modal-content .btn {
  margin: 5px;
}

</style>
