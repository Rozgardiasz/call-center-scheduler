<template>
  <div class="auth-wrapper">
    <div class="auth-inner">
      <h1>Zarządzanie Pracownikami</h1>

      <!-- Formularz dodawania nowego pracownika -->
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

        <button type="submit" class="btn btn-primary btn-block">Dodaj Pracownika</button>
      </form>

      <!-- Lista pracowników -->
      <ul class="employee-list">
        <li v-for="(employee, index) in employees" :key="index" class="employee-item">
          {{ employee.name }} ({{ employee.email }})
          <button @click="confirmRemoveEmployee(index)" class="btn btn-danger">Usuń</button>
        </li>
      </ul>

      <!-- Modal potwierdzenia usunięcia -->
      <div v-if="showConfirmModal" class="confirm-modal">
        <div class="confirm-modal-content">
          <p>Czy na pewno chcesz usunąć tego pracownika?</p>
          <button @click="removeEmployee(confirmedIndex)" class="btn btn-danger">Tak</button>
          <button @click="cancelRemoveEmployee" class="btn btn-secondary">Anuluj</button>
        </div>
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
        confirmPassword: ''
      },
      employees: [],
      showConfirmModal: false,
      confirmedIndex: null
    };
  },
  methods: {
    addEmployee() {
      if (this.newEmployee.name && this.newEmployee.email && this.newEmployee.password) {
        if (this.newEmployee.password === this.newEmployee.confirmPassword) {
          this.employees.push({ 
            name: this.newEmployee.name, 
            email: this.newEmployee.email 
          });
          this.resetForm();
        } else {
          alert('Hasła nie pasują do siebie!');
        }
      } else {
        alert('Wszystkie pola są wymagane!');
      }
    },
    resetForm() {
      this.newEmployee.name = '';
      this.newEmployee.email = '';
      this.newEmployee.password = '';
      this.newEmployee.confirmPassword = '';
    },
    confirmRemoveEmployee(index) {
      this.showConfirmModal = true;
      this.confirmedIndex = index;
    },
    removeEmployee(index) {
      this.employees.splice(index, 1);
      this.showConfirmModal = false;
      this.confirmedIndex = null;
    },
    cancelRemoveEmployee() {
      this.showConfirmModal = false;
      this.confirmedIndex = null;
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
  margin-top: 50px; /* Dodanie marginesu z góry */
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

input {
  width: 100%;
  max-width: 300px; /* Ustawienie maksymalnej szerokości pól */
  font-size: 1.2rem;
  padding: 12px;
  margin: 0 auto; /* Wyśrodkowanie pól */
  border: 1px solid #ccc;
  border-radius: 4px;
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

.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
}

.btn-secondary:hover {
  background-color: #5a6268;
  border-color: #545b62;
}

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

.employee-list {
  list-style: none;
  padding: 0;
  margin-top: 20px;
}

.employee-item {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
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
