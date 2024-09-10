<template>
  <div class="auth-wrapper d-flex flex-column">
    <!-- First Navbar Section -->
    <nav class="navbar navbar-expand-lg navbar-primary bg-primary">
      <div class="container-fluid d-flex justify-content-between">
        <button @click="logout" class="dashboard-link logout-link">Wyloguj</button> <!-- Zmieniono router-link na a z @click -->
        <router-link to="/admin-dashboard/manage-employees" class="dashboard-link ml-auto">Dashboard</router-link>
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
  background-color: #1a73e8; /* Niebieskie tło dla pierwszej sekcji */
  padding: 10px 20px;
  position: fixed; /* Stała pozycja na górze strony */
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}

.navbar-light {
  padding: 10px 0; /* Wewnętrzne odstępy */
  position: fixed; /* Stała pozycja poniżej pierwszego navbaru */
  top: 50px; /* Dopasowanie do wysokości pierwszej sekcji */
  left: 0;
  width: 100%;
  z-index: 999; /* Mniejszy z-index, aby być poniżej pierwszej sekcji */
  background-color: #ffffff;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Delikatny cień */
}

.dashboard-link {
  color: white !important; /* Biały kolor tekstu */
  font-size: 1.5rem; /* Większy rozmiar czcionki */
  font-weight: 600; /* Pogrubienie tekstu dla wyróżnienia */
  text-decoration: none !important; /* Usunięcie podkreślenia */
}

.logout-link {
  background: none; /* Brak tła */
  border: none; /* Brak obramowania */
  color: white; /* Biały kolor tekstu */
  font-size: 1.5rem; /* Większy rozmiar czcionki */
  font-weight: 600; /* Pogrubienie tekstu */
  text-decoration: none; /* Usunięcie podkreślenia */
  cursor: pointer; /* Zmiana kursora na rękę */
  padding: 0; /* Brak wewnętrznych marginesów */
}

.logout-link:hover {
  color: white; /* Kolor tekstu przy najechaniu */
  text-decoration: underline; /* Podkreślenie tekstu przy najechaniu */
}

.ml-auto {
  margin-left: auto; /* Margines automatyczny po lewej stronie */
}

.navbar-nav {
  display: flex; /* Wyświetlanie elementów listy obok siebie */
  justify-content: center; /* Wyśrodkowanie elementów na liście */
  gap: 20px; /* Odstępy między elementami listy */
  padding-left: 0; /* Usunięcie domyślnego wcięcia listy */
}

.nav-item {
  list-style: none; /* Usunięcie stylu listy */
}

.nav-link {
  color: #333 !important; /* Ciemniejszy kolor tekstu na białym tle */
  font-size: 1.1rem; /* Nieco większy rozmiar czcionki */
  font-weight: 500; /* Pogrubienie tekstu dla lepszej czytelności */
  text-decoration: none !important; /* Usunięcie podkreślenia */
  padding: 10px 15px; /* Wyrównanie wewnętrzne dla elementów nawigacyjnych */
  transition: color 0.3s ease-in-out; /* Płynna animacja zmiany koloru tekstu */
}

.nav-link:hover {
  color: #1a73e8 !important; /* Niebieski kolor tekstu przy najechaniu kursorem */
}

.content-wrapper {
  margin-top: 110px; /* Dopasowanie marginesu górnego do wysokości obu sekcji navbaru */
  padding: 20px; /* Dodanie odstępu dla lepszej prezentacji treści */
  
  margin-top: 0;
  margin-bottom: 0;
}
</style>
