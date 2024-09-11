<template>
  <div class="bg-primary text-white d-flex align-items-center justify-content-center my-5 mx-5 p-5" style="height: 70vh;">
    <div>
      <h1>Welcome, {{ employeeName }}!</h1>
      <p>You have <b>{{ 20 - totalLeaveDays }}</b> vacation days left for <b>{{ currentYear }}</b>.</p>
      <p>You've already taken <b>{{ totalLeaveDays }}</b> vacation days this year!</p>
      <!-- Conditionally display the paragraph only if nextVacationDate is not empty -->
      <p v-if="nextVacationDate">Your next vacation starts on: {{ nextVacationDate }}</p>
    </div>
  </div>
</template>


<script>
import { jwtDecode } from 'jwt-decode';

export default {
  name: 'InfoComponent',
  data() {
    return {
      employeeName: sessionStorage.getItem('first_name') + ' ' + sessionStorage.getItem('last_name'),
      availableVacationDays: '',
      nextVacationDate: '',
      holidays: [],
      currentYear: new Date().getFullYear(),
      totalLeaveDays: 0,
    };
  },
  created() {
    this.fetchUserHolidays();
  },
  methods: {
    async fetchUserHolidays() {
      const token = sessionStorage.getItem('token');
      try {
        const decodedToken = jwtDecode(token);
        const userId = decodedToken.user_id;

        const response = await fetch(`http://127.0.0.1:8000/holidays/${userId}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch user holidays');
        }

        const data = await response.json();
        this.holidays = data;
        this.calculateLeaveDays();
        this.findNextVacationDate(); // Call the method to find the next vacation date
      } catch (error) {
        console.error('Error fetching user holidays:', error);
      }
    },

    calculateLeaveDays() {
      let totalDays = 0;
      const year = this.currentYear;

      this.holidays.forEach((holiday) => {
        if (holiday.status == 'approved') {
          const startDate = new Date(holiday.vacation_start);
          const endDate = new Date(holiday.vacation_end);

          if (startDate.getFullYear() <= year && endDate.getFullYear() >= year) {
            const startOfYear = new Date(year, 0, 1);
            const endOfYear = new Date(year, 11, 31);
            const actualStart = startDate < startOfYear ? startOfYear : startDate;
            const actualEnd = endDate > endOfYear ? endOfYear : endDate;
            const daysInYear = (actualEnd - actualStart) / (1000 * 60 * 60 * 24) + 1;

            totalDays += daysInYear;
          }
        }
      });

      this.totalLeaveDays = totalDays;
    },

    findNextVacationDate() {
      const today = new Date();
      let nextDate = null;

      this.holidays.forEach((holiday) => {
        if (holiday.status == 'approved') {
          const startDate = new Date(holiday.vacation_start);

          if (startDate > today && (!nextDate || startDate < nextDate)) {
            nextDate = startDate;
          }
        }
      });

      // Set the nextVacationDate only if a next date is found
      this.nextVacationDate = nextDate ? nextDate.toISOString().split('T')[0] : '';
    },
  },
};
</script>
