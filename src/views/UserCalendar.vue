<template>
  <div class="calendar-wrapper">
    <vue-cal
      :events="events"
      :disable-time="false"
      @cell-click="createEvent"
      @view-change="handleViewChange"
      :views="['day', 'week', 'month']"
      :disable-views="['years', 'year', 'month']"
      default-view="week"
      :min-date="minDate"
      :max-date="maxDate"
      style="height: 800px;"
    />
  </div>
</template>

<script>
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'
import {jwtDecode} from 'jwt-decode';  // Dodajemy funkcję do dekodowania tokenu JWT

export default {
  name: 'CalendarComponent',
  components: {
    VueCal
  },
  data() {
    return {
      events: [],
      minDate: '',
      maxDate: ''
    }
  },
  vacation_data() {
    return {

      startDate: '',
      endDate: '',
      leaveType: '',
      holidays: [] // Przechowywanie urlopów użytkownika
    };
  },
  async created() {
    this.setCurrentMonth();
    await this.fetchWorkHoursAndAddEvents();
    

    await this.fetchUserVacationsAndAddEvents();  // Pobieranie wakacji i dodawanie do kalendarza

  },
  methods: {
    setCurrentMonth() {
      const now = new Date();
      const year = now.getFullYear();
      const month = now.getMonth();

      const firstDayOfMonth = new Date(year, month, 1);
      const lastDayOfMonth = new Date(year, month + 1, 0);

      this.minDate = this.formatDate(firstDayOfMonth);
      this.maxDate = this.formatDate(lastDayOfMonth);
    },
    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    async fetchWorkHoursAndAddEvents() {





      
      try {
        const token = sessionStorage.getItem('token');
        const response = await fetch('http://127.0.0.1:8000/working_hours', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch work hours');
        }

        const data = await response.json();
        this.addWorkHoursForWeeks(data.work_hours);
      } catch (error) {
        console.error('Error fetching work hours:', error);
      }
    },
    addWorkHoursForWeeks(workHours) {
  const currentDate = new Date();
  const currentDay = currentDate.getDay();
  
  // Calculate the number of weeks remaining in the year
  const endOfYear = new Date(currentDate.getFullYear(), 11, 31); // December 31st of the current year
  const diffTime = Math.abs(endOfYear - currentDate);
  const remainingWeeks = Math.ceil(diffTime / (7 * 24 * 60 * 60 * 1000)); // Total remaining weeks until the end of the year

  for (let weekOffset = 0; weekOffset <= remainingWeeks; weekOffset++) {
    workHours.forEach(workHour => {
      const weekday = this.getWeekdayNumber(workHour.weekday);
      const diffDays = weekday - currentDay + (weekOffset * 7);
      
      const workDayDate = new Date(currentDate);
      workDayDate.setDate(currentDate.getDate() + diffDays);

      const startTime = this.createDateWithTime(workDayDate, workHour.start_time);
      const endTime = this.createDateWithTime(workDayDate, workHour.end_time);

      this.events.push({
        start: startTime,
        end: endTime,
        title: 'Godziny Pracy',
        class: 'orange-background'
      });
    });
  }
}
,
    getWeekdayNumber(weekday) {
      const days = {
        Mon: 1,
        Tue: 2,
        Wed: 3,
        Thu: 4,
        Fri: 5,
        Sat: 6,
        Sun: 0
      };
      return days[weekday] || 0;
    },
    createDateWithTime(date, time) {
      const [hours, minutes] = time.split(':').map(Number);
      const newDate = new Date(date);
      newDate.setHours(hours, minutes, 0, 0);
      return newDate;
    },
    createEvent(date, allDay, event, view) {
      if (view === 'day' || view === 'week') {
        const title = prompt('Event title:');
        if (title) {
          const startDate = new Date(date);
          startDate.setHours(0, 0, 0, 0);
          const endDate = new Date(startDate);
          endDate.setDate(endDate.getDate() + 1);
          this.events.push({
            start: startDate,
            end: endDate,
            title: title,
            style: {
              backgroundColor: '#007bff', 
              color: 'white'            
            }
          });
        }
      }
    },
    
async fetchUserVacationsAndAddEvents() {
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

    const vacation_data = await response.json();

    this.holidays = vacation_data;

    this.holidays.forEach(vacation => {

      if(vacation.status == "approved"){
        const startDate = new Date(vacation.vacation_start); 
      let endDate = new Date(vacation.vacation_end); 

  
      endDate.setDate(endDate.getDate() + 1);
      
   
      const endDateStr = endDate.toISOString().split('T')[0];

    
      this.addVacations(startDate, endDateStr);
      }

    });

  } catch (error) {
    alert(`Błąd: ${error.message}`);
  }
}
,

    addVacations(startDate, endDate) {

const start = new Date(startDate);
const end = new Date(endDate);



end.setDate(end.getDate() );

end.setHours(0, 0, 0, 0);


this.events = this.events.filter(event => {
  const eventStart = new Date(event.start);
  const eventEnd = new Date(event.end);


  return !(event.title === 'Godziny Pracy' && (
    eventStart >= start && eventEnd <= end  
  ));
});

this.events.push({
  start: startDate,
  end: endDate,
  title: 'Wakacje',
  class: 'green-background',
  allDay: true 
});
}

}
}
</script>


<style>
.calendar-wrapper {
  min-width: 1600px;
  margin: 0 auto;
}

.vuecal__title-bar {
  background-color: #73b0f1 !important;
}

.vuecal__menu {
  background-color: #1a73e8;
  color: white !important;
}

.vuecal__event.orange-background {
  background-color: #73b0f1 !important;
  color: white !important;
}

.vuecal__event.green-background {
  background-color: #28a745 !important; 
  color: white !important;
}

.vuecal__event-content {
  display: flex;
  justify-content: center;   
  align-items: center;     
  height: 100%;             
}
</style>
