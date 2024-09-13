<template>
  <div class="auth-wrapper d-flex flex-column">
    <nav class="navbar navbar-expand-lg navbar-primary bg-primary">
      <div class="container-fluid d-flex justify-content-between">
        <button @click="logout" class="logout-link ml-auto">Logout</button>
      </div>
    </nav>
    
    <nav class="navbar navbar-expand-lg navbar-light bg-light"> 
      <div class="container-fluid">
        <div class="collapse navbar-collapse justify-content-center" id="navbarNav">
          <ul class="navbar-nav list-unstyled d-flex gap-4">
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
      sessionStorage.removeItem('token'); 
      this.$router.push('/');
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
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  padding: 0;
}

.logout-link:hover {
  text-decoration: underline;
}

.navbar-primary {
  background-color: #1a73e8;
  padding: 10px 20px;
  height: 55px;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  border-bottom: 2px solid black;
}

.navbar-light {
  padding: 10px 0;
  position: fixed;
  top: 50px;
  left: 0;
  width: 100%;
  z-index: 999;
  background-color: #ffffff;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid black;
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
  color: #333 !important;
  font-size: 1.1rem;
  font-weight: 500;
  text-decoration: none !important;
  padding: 10px 15px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.nav-link:hover {
  background-color: rgba(26, 115, 232, 0.2);
  color: #1a73e8 !important;
}

.content-wrapper {
  margin-top: 110px;
  padding: 20px;
}

</style>
