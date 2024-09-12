<template>
  <div class="bg-primary text-white d-flex align-items-center justify-content-center my-5 mx-5 p-5" style="height: 70vh;">
    <div>
      <h1>Welcome, {{ employeeName }}!</h1>
      <p>You have <b>{{totalLeaveDays }}</b>  <i>(including <b>{{totalOnDemandLeaveDays }}</b> on demand days)</i> vacation days left for <b>{{ currentYear }}</b>.</p>
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
      workingHours: {}, // Store working hours
      currentYear: new Date().getFullYear(),
      totalLeaveDays: 0,
      totalOnDemandLeaveDays: 0,
    };
  },
  created() {
    this.fetchUserWorkingHours().then(() => {
      this.fetchUserHolidays();
    });
  },
  methods: {
    async fetchUserWorkingHours() {
      const token = sessionStorage.getItem('token');
      try {
  
    

        const response = await fetch(`http://127.0.0.1:8000/working_hours`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch user working hours');
        }

        const data = await response.json();
        this.parseWorkingHours(data.work_hours);
      } catch (error) {
        console.error('Error fetching working hours:', error);
      }
    },

    parseWorkingHours(workHours) {
      // Initialize working hours for all weekdays as non-working
      const defaultWorkingHours = {
        Mon: false,
        Tue: false,
        Wed: false,
        Thu: false,
        Fri: false,
        Sat: false,
        Sun: false,
      };

      workHours.forEach((workHour) => {
        // Treat Saturday and Sunday as non-working days regardless
        if (workHour.weekday !== 'Sat' && workHour.weekday !== 'Sun') {
          defaultWorkingHours[workHour.weekday] = true;
        }
      });

      this.workingHours = defaultWorkingHours;
    },

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
        this.findNextVacationDate();
      } catch (error) {
        console.error('Error fetching user holidays:', error);
      }
    },

    calculateLeaveDays() {
      let totalDays = 0;
      let totalDemandDays = 0;
      const year = this.currentYear;

      this.holidays.forEach((holiday) => {
        if (holiday.status === 'approved') {
          const startDate = new Date(holiday.vacation_start);
          const endDate = new Date(holiday.vacation_end);

          if (startDate.getFullYear() <= year && endDate.getFullYear() >= year) {
            const startOfYear = new Date(year, 0, 1);
            const endOfYear = new Date(year, 11, 31);
            const actualStart = startDate < startOfYear ? startOfYear : startDate;
            const actualEnd = endDate > endOfYear ? endOfYear : endDate;

            let currentDate = new Date(actualStart);
            while (currentDate <= actualEnd) {
              const dayOfWeek = currentDate.toLocaleString('en-US', { weekday: 'short' });

              if (this.workingHours[dayOfWeek]) {
                // Increment only if it's a working day
                totalDays += 1;
                if (holiday.type_of_vacation == "on_demand") {
                  totalDemandDays += 1;
                }
              }

              currentDate.setDate(currentDate.getDate() + 1);
            }
          }
        }
      });

      totalDays = 20 - totalDays;
      totalDemandDays = 4 - totalDemandDays;

      if (totalDemandDays > totalDays) {
        totalDemandDays = totalDays;
      }

      this.totalLeaveDays = totalDays;
      this.totalOnDemandLeaveDays = totalDemandDays;
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
