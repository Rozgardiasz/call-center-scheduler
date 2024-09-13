<template>
  <div class="user-info-container d-flex align-items-center justify-content-center">
    <div class="user-info-box text-center">
      <h1>Welcome, {{ employeeName }}!</h1>
      <p>You have <b>{{ totalLeaveDays }}</b> <i>(including <b>{{ totalOnDemandLeaveDays }}</b> on demand days)</i> vacation days left for <b>{{ currentYear }}</b>.</p>
      <p>You've already taken <b>{{ LeaveDaysTaken }}</b> vacation days this year!</p>
      <p v-if="nextVacationDate">Your next vacation starts on: <b>{{ nextVacationDate }}</b></p>
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
      workingHours: {},
      currentYear: new Date().getFullYear(),
      totalLeaveDays: 0,
      LeaveDaysTaken: 0,
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

      this.LeaveDaysTaken = totalDays;
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
      this.nextVacationDate = nextDate ? nextDate.toISOString().split('T')[0] : '';
    },
  },
};
</script>

<style scoped>

.user-info-container {
  height: 70vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: None; 
  padding: 20px;
}

.user-info-box {
  background-color: white; 
  color: #333; 
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
  border: 2px solid black; 
  max-width: 600px;
  text-align: center;
}

h1 {
  font-size: 2rem;
  margin-bottom: 20px;
}

p {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

b {
  color: #1a73e8; 
}
</style>

