<template>
  <div class="requests-wrapper">
    <div class="requests-inner">
      <h1>Wnioski Urlopowe i Dni Wolne</h1>
      
      <!-- Lista wniosków -->
      <ul class="requests-list">
        <li v-for="(request, index) in leaveRequests" :key="index" class="request-item">
          {{ request.employeeName }} - {{ request.type }} od {{ request.startDate }} do {{ request.endDate }}
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
      leaveRequests: [
        { employeeName: 'Jan Kowalski', type: 'Urlop', startDate: '2024-09-01', endDate: '2024-09-07' },
        { employeeName: 'Anna Nowak', type: 'Dzień Wolny', startDate: '2024-09-15', endDate: '2024-09-15' }
      ],
      showConfirmApproveModal: false,
      showConfirmRejectModal: false,
      confirmedIndex: null
    };
  },
  methods: {
    confirmApproveRequest(index) {
      this.showConfirmApproveModal = true;
      this.confirmedIndex = index;
    },
    confirmRejectRequest(index) {
      this.showConfirmRejectModal = true;
      this.confirmedIndex = index;
    },
    approveRequest(index) {
      this.leaveRequests.splice(index, 1);
      this.showConfirmApproveModal = false;
      this.confirmedIndex = null;
      alert('Wniosek został zaakceptowany.');
    },
    rejectRequest(index) {
      this.leaveRequests.splice(index, 1);
      this.showConfirmRejectModal = false;
      this.confirmedIndex = null;
      alert('Wniosek został odrzucony.');
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
