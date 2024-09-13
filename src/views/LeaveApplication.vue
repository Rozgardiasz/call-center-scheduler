<template>
  <div class="page-container">
    <div class="request-panel">
      <h1>Create a request</h1>

      <form @submit.prevent="submitLeaveRequest">
        <div class="form-group">
          <label for="start-date">Start Date:</label>
          <input type="date" v-model="startDate" id="start-date" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="end-date">End Date:</label>
          <input
            type="date"
            v-model="endDate"
            id="end-date"
            class="form-control"
            required
            :min="startDate"
          />
        </div>

        <div class="checkbox-group">
          <input
            type="checkbox"
            v-model="isOnDemand"
            id="on-demand-checkbox"
          />
          <label for="on-demand-checkbox">Leave on Demand</label>
        </div>

        <button type="submit" class="btn btn-primary btn-block">Submit Request</button>
      </form>
    </div>

    <div class="holidays-panel">
      <h2>Your Vacations</h2>
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
      <p v-else>No leave requests</p>
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
  watch: {
    isOnDemand(newVal) {
      this.leaveType = newVal ? 'on_demand' : 'regular';
    }
  },
  methods: {
    async submitLeaveRequest() {
      if (this.startDate && this.endDate && new Date(this.endDate) < new Date(this.startDate)) {
        alert('The end date cannot be earlier than the start date');
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
          throw new Error(errorData.detail || 'An error occurred while submitting the leave request');
        }

        alert('The leave request has been successfully submitted');

        this.leaveType = 'regular';
        this.isOnDemand = false;
        this.startDate = '';
        this.endDate = '';

        this.fetchUserHolidays();
      } catch (error) {
        alert(`Error: ${error.message}`);
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
          throw new Error('Failed to retrieve the list of vacations');
        }

        const data = await response.json();
        this.holidays = data;
      } catch (error) {
        alert(`Error: ${error.message}`);
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
  background-color: #f3f3f3;
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
  border: 1px solid #ccc;
  border-radius: 8px; 
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.holidays-panel {
  width: 60%;
  padding: 20px;
  background-color: #f1f1f1;
  border: 1px solid #ccc; 
  border-radius: 8px; 
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); 
  margin: 0 auto; 
}

.holidays-panel h2 {
  text-align: center; 
  margin-bottom: 20px; 
}

.holiday-item {
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ddd; 
  border-radius: 4px; 
  margin-bottom: 10px; 
  transition: background-color 0.3s ease;
}

.holiday-item {
  padding: 10px;
  background-color: #fff;
  border-bottom: 1px solid #ddd;
}

.holiday-item.expired {
  color: #888; 
}

.holiday-item:last-child {
  border-bottom: 0; 
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
  margin-top: 25px;
  margin-bottom: 10px;
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
