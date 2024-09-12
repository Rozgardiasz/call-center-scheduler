<template>
  <div class="page-container">
    <div class="request-panel">
      <h1>Wnioski o Urlop</h1>

      <form @submit.prevent="submitLeaveRequest">
        <div class="form-group">
          <label for="start-date">Data rozpoczęcia:</label>
          <input
            type="date"
            v-model="startDate"
            id="start-date"
            class="form-control"
            required
            :min="todayDate"
          />
        </div>

        <div class="form-group">
          <label for="end-date">Data zakończenia:</label>
          <input
            type="date"
            v-model="endDate"
            id="end-date"
            class="form-control"
            required
            :min="minEndDate"
          />
        </div>

        <div class="checkbox-group">
          <input
            type="checkbox"
            v-model="isOnDemand"
            id="on-demand-checkbox"
          />
          <label for="on-demand-checkbox">Urlop na Żądanie</label>
        </div>

        <button type="submit" class="btn btn-primary btn-block">Złóż Wniosek</button>
      </form>
    </div>

    <div class="holidays-panel">
      <h2>Twoje Urlopy</h2>
      <ul v-if="holidays.length">
        <li
          v-for="holiday in holidays"
          :key="holiday.id"
          :class="{'holiday-item': true, 'expired': isExpired(holiday.vacation_end)}"
        >
          {{ holiday.vacation_start }} - {{ holiday.vacation_end }}
          <span v-if="holiday.type_of_vacation === 'on_demand'"> ({{ holiday.type_of_vacation }})</span>
          <span :class="getStatusClass(holiday.status)">{{ holiday.status }}</span>
        </li>
      </ul>
      <p v-else>Brak wniosków o urlop.</p>
    </div>
  </div>
</template>


<script>
import { jwtDecode } from 'jwt-decode';

export default {
  name: 'LeaveApplication',
  data() {
    return {
      leaveType: 'regular', 
      isOnDemand: false,
      startDate: '',
      endDate: '',
      holidays: [] 
    };
  },
  computed: {
    todayDate() {
      return new Date().toISOString().split('T')[0];
    },
    minEndDate() {

      if (this.startDate) {
        return this.startDate > this.todayDate ? this.startDate : this.todayDate;
      }
      return this.todayDate;
    }
  },
  watch: {
    isOnDemand(newVal) {
      this.leaveType = newVal ? 'on_demand' : 'regular';
    }
  },
  methods: {
    async submitLeaveRequest() {
      if (this.startDate && this.endDate && new Date(this.endDate) < new Date(this.startDate)) {
        alert('Data zakończenia nie może być wcześniejsza niż data rozpoczęcia.');
        return;
      }

      try {
        const token = sessionStorage.getItem('token');
        const decodedToken = jwtDecode(token);
        const userId = decodedToken.user_id;

        const requestData = {
          employee_id: userId,
          vacation_start: this.startDate,
          vacation_end: this.endDate,
          type_of_vacation: this.leaveType
        };

        const response = await fetch('http://127.0.0.1:8000/holiday_request', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(requestData)
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Wystąpił błąd podczas składania wniosku o urlop.');
        }

        alert('Wniosek o urlop został złożony pomyślnie.');

        this.leaveType = 'regular';
        this.isOnDemand = false;
        this.startDate = '';
        this.endDate = '';

        this.fetchUserHolidays(); 
      } catch (error) {
        alert(`Błąd: ${error.message}`);
      }
    },

    async fetchUserHolidays() {
      try {
        const token = sessionStorage.getItem('token');
        const decodedToken = jwtDecode(token);
        const userId = decodedToken.user_id;

        const response = await fetch(`http://127.0.0.1:8000/holidays/${userId}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Accept': 'application/json'
          }
        });

        if (!response.ok) {
          throw new Error('Nie udało się pobrać listy urlopów.');
        }

        const data = await response.json();
        this.holidays = data;
      } catch (error) {
        alert(`Błąd: ${error.message}`);
      }
    },

    getStatusClass(status) {
      switch (status) {
        case 'pending':
          return 'status-pending';
        case 'approved':
          return 'status-approved';
        case 'rejected':
          return 'status-rejected';
        default:
          return '';
      }
    },

    isExpired(endDate) {
      return new Date(endDate) < new Date();
    }
  },
  mounted() {
    this.fetchUserHolidays(); 
  }
};
</script>



<style scoped>
.page-container {
  display: flex;
  height: 70vh;
  background-color: #f7f7f7;
  margin-top: 50px;
}

.request-panel {
  flex-basis: 30%;
  padding: 20px;
  background-color: #ffffff;
  border-right: 1px solid #ddd;
  display: flex;
  max-height: 70%;
  flex-direction: column;
}

.holidays-panel {
  flex-basis: 70%;
  padding: 20px;
  background-color: #f1f1f1;
}

h1 {
  font-size: 1.8rem;
  margin-bottom: 10px; 
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px; 
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input[type="date"] {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.checkbox-group {
  display: flex;
  align-items: center;
  margin-top: 10px; 
}

.checkbox-group input {
  margin-right: 10px;
}

.btn-block {
  width: 100%;
  padding: 12px;
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

.holiday-item {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.holiday-item.expired {
  background-color: #f0f0f0; 
}

.status-pending {
  color: #ffc107; 
}
.status-approved {
  color: #28a745; 
}

.status-rejected {
  color: #dc3545; 
}

</style>
