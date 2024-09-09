<template>
  <div class="auth-wrapper">
    <div class="auth-inner">
      <h1>Logowanie</h1>
      <form @submit.prevent="login">
        <div class="form-group">
          <input
            type="text"
            v-model="username"
            id="username"
            class="form-control"
            placeholder="Login"
            required
          />
        </div>

        <div class="form-group">
          <input
            type="password"
            v-model="password"
            id="password"
            class="form-control"
            placeholder="Hasło"
            required
          />
        </div>

        <div class="button-group">
          <button type="submit" class="btn btn-primary btn-block">
            Zaloguj
          </button>
          <button type="button" @click="loginAsUser" class="btn btn-secondary btn-block">
            Zaloguj jako Użytkownik
          </button>
          <button type="button" @click="loginAsAdmin" class="btn btn-secondary btn-block">
            Zaloguj jako Administrator
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        // Sending a POST request to the server
        const response = await fetch('http://127.0.0.1:8000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            "email": this.username,
            "password": this.password
          })
        });

        // Checking if the server response is valid
        if (!response.ok) {
          throw new Error('Login failed. Please check your credentials.');
        }

        // Processing the response from the server
        const data = await response.json();
        alert(`Logged in as: ${data.first_name} ${data.last_name}`);
        
        // Using 'this' to call the correct methods
        sessionStorage.setItem('token', data.token); 
        if (data.is_admin) {
          this.loginAsAdmin();
        } else {
          this.loginAsUser();
        }

      } catch (error) {
        alert(`Error: ${error.message}`);
      }
    },
    loginAsUser() {
      this.$router.push('/user-dashboard/calendar');
    },
    loginAsAdmin() {
      this.$router.push('/admin-dashboard/manage-employees');
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
  max-width: 300px; /* Maksymalna szerokość pól tekstowych */
  font-size: 1.2rem;
  padding: 10px;
  margin: 0 auto;
  border: 1px solid #ccc;
  border-radius: 4px;
}

input::placeholder {
  color: #888; /* Kolor tekstu placeholdera */
  font-size: 1.2rem; /* Rozmiar czcionki placeholdera */
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
