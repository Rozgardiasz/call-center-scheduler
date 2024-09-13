<template>
  <div class="requests-wrapper">
    <div class="requests-inner">
      <h1>Leave Requests and Days Off</h1>

      <ul class="requests-list">
        <li
          v-for="(request, index) in leaveRequests"
          :key="index"
          :class="{
            'request-item': true,
            'can-approve': canBeApproved(request),
            'cannot-approve': !canBeApproved(request),
          }"
        >
          <div class="request-info">
           <b>{{ request.first_name }} {{ request.last_name }}</b> -
            <span v-if="request.type_of_vacation !== 'regular'">
            <b>{{ request.type_of_vacation }}</b>
            </span>
            od <b>{{ request.vacation_start }}</b> do <b>{{ request.vacation_end }}</b>
          </div>
          <div class="request-buttons">
            <button @click="confirmApproveRequest(index)" class="btn btn-success">Accept</button>
            <button @click="confirmRejectRequest(index)" class="btn btn-danger">Reject</button>
          </div>
        </li>
      </ul>

      <div v-if="showConfirmApproveModal" class="confirm-modal">
        <div class="confirm-modal-content">
          <p>Are you sure you want to approve this request?</p>
          <button @click="approveRequest(confirmedIndex)" class="btn btn-success">Yes</button>
          <button @click="cancelConfirmApprove" class="btn btn-secondary">Cancel</button>
        </div>
      </div>

      <div v-if="showConfirmRejectModal" class="confirm-modal">
        <div class="confirm-modal-content">
          <p>Are you sure you want to reject this request?</p>
          <button @click="rejectRequest(confirmedIndex)" class="btn btn-danger">Yes</button>
          <button @click="cancelConfirmReject" class="btn btn-secondary">Cancel</button>
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
      leaveRequests: [],
      showConfirmApproveModal: false,
      showConfirmRejectModal: false,
      confirmedIndex: null
    };
  },
  async created() {
    await this.fetchPendingHolidays();
  },
  methods: {
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
            return { ...holiday, employee };
          })
        );

        this.leaveRequests = holidays;
      } catch (error) {
        console.error('Error fetching holidays:', error);
      }
    },

    canBeApproved(request) {
      return request.status === 'pending';
    },

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
        const holidayId = this.leaveRequests[index].id; 
        const response = await fetch(`http://127.0.0.1:8000/admin/approve_holiday/${holidayId}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ holiday_id: request.id })
        });
        if (!response.ok) throw new Error('Failed to approve holiday');
        
        this.leaveRequests.splice(index, 1); 
        alert('Request approved');
      } catch (error) {
        console.error('Error approving request:', error);
      }
      
      this.showConfirmApproveModal = false;
      this.confirmedIndex = null;
    },
    async rejectRequest(index) {
      const request = this.leaveRequests[index];
      try {
        const holidayId = this.leaveRequests[index].id; 
        const response = await fetch(`http://127.0.0.1:8000/admin/reject_holiday/${holidayId}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ holiday_id: request.id })
        });
        if (!response.ok) throw new Error('Failed to reject holiday');
        
        this.leaveRequests.splice(index, 1); 
        alert('Request rejected.');
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
  margin-top: 50px;
  padding: 20px;
}

.requests-list {
  list-style: none;
  padding: 0;
  margin-top: 20px;
}

.request-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  margin: 10px 0;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.request-info {
  flex: 1;
  margin-right: 20px;
}

.request-buttons {
  display: flex;
}

.btn {
  padding: 10px 20px;
  font-size: 1rem;
  margin-right: 5px;
}

.can-approve {
  background-color: #ffffff; 
}

.cannot-approve {
  background-color: #f8d7da; 
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
  padding: 50px;
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  width: 100%;
  text-align: center;
}

h1 {
  margin-bottom: 30px;
  text-align: center;
  font-size: 2rem;
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
</style>
