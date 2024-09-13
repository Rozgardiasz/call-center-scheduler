<template>
  <div class="auth-wrapper d-flex flex-column">
    <!-- First Navbar Section -->
    <nav class="navbar navbar-expand-lg navbar-primary bg-primary">
      <div class="container-fluid">
        <button @click="logout" class="logout-link ml-auto">Wyloguj</button>
      </div>
    </nav>
    
    <!-- Second Navbar Section -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <div class="collapse navbar-collapse justify-content-center" id="navbarNav">
          <ul class="navbar-nav list-unstyled d-flex gap-4">
            <li class="nav-item">
              <router-link to="/admin-dashboard/manage-employees" class="nav-link">Manage Employees</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin-dashboard/leave-requests" class="nav-link">Leave Requests</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Content Section -->
    <div class="content-wrapper"> 
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminDashboard',
  methods: {
    logout() {
      sessionStorage.removeItem('token'); // Usuwanie tokena z sessionStorage
      this.$router.push('/'); // Przekierowanie do strony logowania
    }
  }
};
</script>

<style scoped>
.navbar-primary {
  background-color: #1a73e8; /* Niebieskie tło */
  padding: 10px 20px;
  height: 55px;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  border-bottom: 2px solid black; /* Delikatny kontur */
}

.navbar-light {
  padding: 10px 0;
  position: fixed;
  top: 50px;
  left: 0;
  width: 100%;
  z-index: 999;
  background-color: #ffffff;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Cień */
  border-bottom: 1px solid black; /* Kontur dla przejrzystości */
}

/* .dashboard-link {
  color: white !important;
  font-size: 1.5rem;
  font-weight: 600;
  text-decoration: none !important;
}

.dashboard-link:hover {
  text-decoration: underline;
} */


.logout-link {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  padding: 0;
  margin-left: auto;
}

.logout-link:hover {
  text-decoration: underline;
}

.navbar-nav {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding-left: 0;
}

.nav-item {
  list-style: none;
}

.nav-link {
  color: #333 !important; /* Ciemniejszy kolor tekstu na białym tle */
  font-size: 1.1rem; /* Nieco większy rozmiar czcionki */
  font-weight: 500; /* Pogrubienie tekstu dla lepszej czytelności */
  text-decoration: none !important; /* Usunięcie podkreślenia */
  padding: 10px 15px; /* Wyrównanie wewnętrzne dla elementów nawigacyjnych */
  transition: background-color 0.3s ease, color 0.3s ease; /* Płynna animacja zmiany koloru tła i tekstu */
}

.nav-link:hover {
  background-color: rgba(26, 115, 232, 0.2); /* Niebieskie tło przy najechaniu */
  color: #1a73e8 !important; /* Niebieski kolor tekstu przy najechaniu */
}

.content-wrapper {
  margin-top: 110px;
  padding: 20px;
}
</style>
