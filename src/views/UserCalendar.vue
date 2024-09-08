<template>
  <div class="calendar-wrapper">
    <vue-cal
      :events="events"
      :disable-time="true"
      @cell-click="createEvent"
      @view-change="handleViewChange"
      :views="['day', 'week', 'month', 'year']"
      default-view="week"
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
      events: [
        {
          start: '2024-06-10T00:00:00',
          end: '2024-06-11T00:00:00', // Full-day event: start at 2024-06-10 00:00 and end at 2024-06-11 00:00
          title: 'Vacation Start'
        },
        {
          start: '2024-06-14T00:00:00',
          end: '2024-06-15T00:00:00', // Full-day event
          title: 'Meeting'
        }
      ]
    }
  },
  methods: {
    createEvent(date, allDay, event, view) {
      if (view === 'day' || view === 'week') {
        const title = prompt('Event title:')
        if (title) {
          const startDate = new Date(date)
          startDate.setHours(0, 0, 0, 0) // Start at midnight
          const endDate = new Date(startDate)
          endDate.setDate(endDate.getDate() + 1) // End at midnight the next day
          this.events.push({
            start: startDate,
            end: endDate,
            title: title
          })
        }
      }
    },
    handleViewChange({ view }) {
      // Handle view changes if needed
      // For now, this method just logs the current view
      console.log('Current view:', view)
    }
  }
}
</script>

<style scoped>
.calendar-wrapper {
  min-width: 1600px;
  margin: 0 auto;
}
</style>
