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
  created() {
    this.setCurrentMonth();
    const today = new Date();
    this.addWorkHours(today, 9, 17);
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
            class: 'blue-background'  
          });
        }
      }
    },
    handleViewChange({ view }) {
      console.log('Current view:', view);
    },
    addWorkHours(date, startHour, endHour) {
      const startDate = new Date(date);
      const endDate = new Date(date);

      startDate.setHours(startHour, 0, 0, 0);
      endDate.setHours(endHour, 0, 0, 0);

      this.events.push({
        start: startDate,
        end: endDate,
        title: 'Godziny Pracy',
        class: 'blue-background'  
      });
    }
  }
}
</script>

<style scoped>
.calendar-wrapper {
  min-width: 1600px;
  margin: 0 auto;
}


.vuecal__event.blue-background {
  background-color: #007bff !important; 
  color: white !important;              
}


.vuecal__event-content.blue-background {
  color: white !important;              
}

.vuecal__event.blue-background .vuecal__event-content {
  background-color: #007bff !important;
  color: white !important;
}
</style>

