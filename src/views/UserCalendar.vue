<template>
  <div class="calendar-wrapper">
    <vue-cal
      :events="events"
      :disable-time="false" 
      @cell-click="createEvent"
      @view-change="handleViewChange"
      :views="['day', 'week', 'month']"
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
  async created() {
    this.setCurrentMonth();
    await this.fetchWorkHoursAndAddEvents();  // Pobieramy godziny pracy
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
        const token = sessionStorage.getItem('token');  // Pobierz token
        const response = await fetch('http://127.0.0.1:8000/working_hours', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch work hours');
        }

        const data = await response.json();
        this.addWorkHoursForWeeks(data.work_hours);  // Dodaj godziny pracy na obecny tydzień i kolejne 3 tygodnie
      } catch (error) {
        console.error('Error fetching work hours:', error);
      }
    },
    addWorkHoursForWeeks(workHours) {
      // Pobieramy obecny tydzień
      const currentDate = new Date();
      const currentDay = currentDate.getDay();  // Dzień tygodnia (0 = Niedziela, 1 = Poniedziałek, ...)

      // Iteracja przez obecny tydzień i 3 tygodnie do przodu
      for (let weekOffset = 0; weekOffset <= 3; weekOffset++) {
        workHours.forEach(workHour => {
          const weekday = this.getWeekdayNumber(workHour.weekday);  // Zmapuj nazwę dnia na numer (Poniedziałek = 1, itd.)
          const diffDays = weekday - currentDay + (weekOffset * 7);  // Dodaj różnicę w dniach oraz przesunięcie o tygodnie

          // Ustal datę dla tego dnia w bieżącym tygodniu i kolejnych tygodniach
          const workDayDate = new Date(currentDate);
          workDayDate.setDate(currentDate.getDate() + diffDays);

          // Utwórz daty startu i zakończenia wydarzenia
          const startTime = this.createDateWithTime(workDayDate, workHour.start_time);
          const endTime = this.createDateWithTime(workDayDate, workHour.end_time);

          // Dodaj wydarzenie do kalendarza z klasą `orange-background`
          this.events.push({
            start: startTime,
            end: endTime,
            title: 'Godziny Pracy',
            class: 'orange-background'
          });
        });
      }
    },
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
            backgroundColor: '#007bff', // Kolor tła wydarzenia
            color: 'white'              // Kolor tekstu
          }
        });
      }
    }
  }
  }
}
</script>



<style >


.calendar-wrapper {
  min-width: 1600px;
  margin: 0 auto;
}

.vuecal__title-bar{
  background-color: #73b0f1 !important; 
}



.vuecal__menu{
  background-color: #1a73e8;
  color: white !important;              
}

.vuecal__event.orange-background,
.vuecal__event.blue-background {
  background-color: #73b0f1 !important; 
  color: white !important;              
}

</style>
