<template>
  <div class="auth-wrapper d-flex flex-column">
    <!-- First Navbar Section -->
    <nav class="navbar navbar-expand-lg navbar-primary bg-primary">
      <div class="container-fluid d-flex justify-content-between">
        <button @click="logout" class="logout-link ml-auto">Wyloguj</button>
      </div>
    </nav>
    
    <!-- Second Navbar Section -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light"> <!-- Sekcja z białym tłem -->
      <div class="container-fluid">
        <div class="collapse navbar-collapse justify-content-center" id="navbarNav">
          <ul class="navbar-nav list-unstyled d-flex gap-4"> <!-- Linki nawigacyjne wyśrodkowane -->
            <li class="nav-item">
              <router-link to="/user-dashboard/info" class="nav-link">Info</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user-dashboard/calendar" class="nav-link">Calendar</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user-dashboard/leave-application" class="nav-link">Requests</router-link>
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
  name: 'UserDashboard',
  methods: {
    logout() {
      sessionStorage.removeItem('token'); // Usuwanie tokena z sessionStorage
      this.$router.push('/'); // Przekierowanie do strony logowania
    }
  }
};
</script>

<style scoped>
h1 {
  margin-bottom: 10px;
}

p {
  margin: 0;
  margin-bottom: 10px;
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
  text-decoration: underline; /* Podkreślenie tekstu przy najechaniu */
  /*color: rgba(255, 255, 255, 0.8); /* Subtelne zmniejszenie koloru */
}

.navbar-primary {
  background-color: #1a73e8; /* Niebieskie tło dla pierwszej sekcji */
  padding: 10px 20px;
  height: 55px;
  position: fixed; /* Stała pozycja na górze strony */
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  border-bottom: 2px solid black;
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
  border-bottom: 1px solid black;
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
  transition: background-color 0.3s ease, color 0.3s ease; /* Płynna animacja zmiany koloru tła i tekstu */
}

.nav-link:hover {
  background-color: rgba(26, 115, 232, 0.2); /* Niebieskie tło przy najechaniu */
  color: #1a73e8 !important; /* Niebieski kolor tekstu przy najechaniu */
}


.content-wrapper {
  margin-top: 110px; /* Dopasowanie marginesu górnego do wysokości obu sekcji navbaru */
  padding: 20px; /* Dodanie odstępu dla lepszej prezentacji treści */
  

}
</style>
