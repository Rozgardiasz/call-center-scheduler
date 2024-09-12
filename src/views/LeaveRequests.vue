<template>
  <div class="requests-wrapper">
    <div class="requests-inner">
      <h1>Wnioski Urlopowe i Dni Wolne</h1>
      
      <!-- Lista wniosków -->
      <ul class="requests-list">
          <li 
          v-for="(request, index) in leaveRequests" 
          :key="index" 
          :class="{
            'request-item': true,
            'can-approve': canBeApproved(request),
            'cannot-approve': !canBeApproved(request)
          }"
        >
          {{ request.first_name }} {{ request.last_name }} - {{ request.type_of_vacation }} od {{ request.vacation_start }} do {{ request.vacation_end }}
          <button @click="confirmApproveRequest(index)" class="btn btn-success">Akceptuj</button>
          <button @click="confirmRejectRequest(index)" class="btn btn-danger">Odrzuć</button>
        </li>
      </ul>

      <!-- Modal potwierdzenia akceptacji -->
      <div v-if="showConfirmApproveModal" class="confirm-modal">
        <div class="confirm-modal-content">
          <p>Czy na pewno chcesz zaakceptować ten wniosek?</p>
          <button @click="approveRequest(confirmedIndex)" class="btn btn-success">Tak</button>
          <button @click="cancelConfirmApprove" class="btn btn-secondary">Anuluj</button>
        </div>
      </div>

      <!-- Modal potwierdzenia odrzucenia -->
      <div v-if="showConfirmRejectModal" class="confirm-modal">
        <div class="confirm-modal-content">
          <p>Czy na pewno chcesz odrzucić ten wniosek?</p>
          <button @click="rejectRequest(confirmedIndex)" class="btn btn-danger">Tak</button>
          <button @click="cancelConfirmReject" class="btn btn-secondary">Anuluj</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'LeaveRequests',
  data() {
    return {
      leaveRequests: [], // Empty initially, will be fetched from the API
      showConfirmApproveModal: false,
      showConfirmRejectModal: false,
      confirmedIndex: null
    };
  },
  async created() {
    await this.fetchPendingHolidays();
  },
  methods: {
    // Fetch pending holidays and map employee data
    async fetchPendingHolidays() {
      try {
        const response = await fetch('http://127.0.0.1:8000/holidays/pending', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          }
        });
        if (!response.ok) throw new Error('Failed to fetch pending holidays');
        
        let holidays = await response.json();
        
        // Fetch employee details for each holiday request
        holidays = await Promise.all(
          holidays.map(async (holiday) => {
            const employeeResponse = await fetch(`http://127.0.0.1:8000/holidays/${holiday.employee_id}`, {
              method: 'GET',
              headers: {
                'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
                'Content-Type': 'application/json'
              }
            });
            if (!employeeResponse.ok) throw new Error('Failed to fetch employee data');
            
            const employee = await employeeResponse.json();
            return { ...holiday, employee }; // Combine holiday and employee data
          })
        );

        this.leaveRequests = holidays;
      } catch (error) {
        console.error('Error fetching holidays:', error);
      }
    },

    // Check if a request can be approved (custom logic can be applied here)
    canBeApproved(request) {
      // Placeholder logic, adjust this to your approval conditions
      return request.status === 'pending';
    },

    // Handle approval actions
    confirmApproveRequest(index) {
      this.showConfirmApproveModal = true;
      this.confirmedIndex = index;
    },
    confirmRejectRequest(index) {
      this.showConfirmRejectModal = true;
      this.confirmedIndex = index;
    },
    async approveRequest(index) {
      const request = this.leaveRequests[index];
      try {
        const holidayId = this.leaveRequests[index].id; // Get the holiday request ID
        const response = await fetch(`http://127.0.0.1:8000/admin/approve_holiday/${holidayId}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ holiday_id: request.id })
        });
        if (!response.ok) throw new Error('Failed to approve holiday');
        
        this.leaveRequests.splice(index, 1); // Remove from list
        alert('Wniosek został zaakceptowany.');
      } catch (error) {
        console.error('Error approving request:', error);
      }
      
      this.showConfirmApproveModal = false;
      this.confirmedIndex = null;
    },
    async rejectRequest(index) {
      const request = this.leaveRequests[index];
      try {
        const holidayId = this.leaveRequests[index].id; // Get the holiday request ID
        const response = await fetch(`http://127.0.0.1:8000/admin/reject_holiday/${holidayId}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ holiday_id: request.id })
        });
        if (!response.ok) throw new Error('Failed to reject holiday');
        
        this.leaveRequests.splice(index, 1); // Remove from list
        alert('Wniosek został odrzucony.');
      } catch (error) {
        console.error('Error rejecting request:', error);
      }
      
      this.showConfirmRejectModal = false;
      this.confirmedIndex = null;
    },
    cancelConfirmApprove() {
      this.showConfirmApproveModal = false;
      this.confirmedIndex = null;
    },
    cancelConfirmReject() {
      this.showConfirmRejectModal = false;
      this.confirmedIndex = null;
    }
  }
};


</script>

<style scoped>
.requests-wrapper {
  display: flex;
  min-width: 500px;
  align-items: center;
  justify-content: center;
  height: 70vh;
  background-color: #f7f7f7;
  margin-top: 50px; /* Dodanie marginesu z góry */
}

.requests-wrapper {
  padding: 20px;
}

.requests-list {
  list-style-type: none;
  padding: 0;
}

.request-item {
  padding: 15px;
  margin: 10px 0;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.can-approve {
  background-color: #d4edda; /* Light green for approvable requests */
}

.cannot-approve {
  background-color: #f8d7da; /* Light red for non-approvable requests */
}

.btn {
  margin-left: 10px;
}

.confirm-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.confirm-modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.requests-inner {
  background-color: #ffffff;
  padding: 50px;
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 700px;
  text-align: center; /* Wyśrodkowanie zawartości formularza */
}

h1 {
  margin-bottom: 30px;
  text-align: center;
  font-size: 2rem;
}

.requests-list {
  list-style: none;
  padding: 0;
  margin-top: 20px;
}

.request-item {
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn {
  padding: 10px 20px;
  font-size: 1rem;
  margin: 0 5px;
}

.btn-success {
  background-color: #28a745;
  border-color: #28a745;
}

.btn-success:hover {
  background-color: #218838;
  border-color: #1e7e34;
}

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

.confirm-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.confirm-modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.confirm-modal-content .btn {
  margin: 5px;
}
</style>
