<template>
  <div class="leave-request">
    <h2>Nhập thông tin xin nghỉ phép</h2>
    
    <div class="input-group">
      <label>Họ và tên:</label>
      <input v-model="formData.name" placeholder="Nhập họ và tên" required />
    </div>
    
    <div class="input-group">
      <label>Chức vụ:</label>
      <input v-model="formData.position" placeholder="Nhập chức vụ" required />
    </div>
    
    <div class="input-group">
      <label>Phòng ban:</label>
      <input v-model="formData.department" placeholder="Nhập phòng ban" required />
    </div>
    
    <div class="input-group">
      <label>Số ngày phép đã nghỉ (2025):</label>
      <input type="number" v-model.number="formData.used_days" min="0" required />
    </div>
    
    <div class="input-group">
      <label>Số ngày xin nghỉ:</label>
      <input type="number" v-model.number="formData.requested_days" min="1" required />
    </div>
    
    <div class="input-group">
      <label>Ngày bắt đầu:</label>
      <input type="date" v-model="formData.start_date" required />
    </div>
    
    <div class="input-group">
      <label>Ngày kết thúc:</label>
      <input type="date" v-model="formData.end_date" required />
    </div>
    
    <div class="input-group">
      <label>Lý do nghỉ:</label>
      <input v-model="formData.reason" placeholder="Nhập lý do" required />
    </div>
    
    <div class="input-group">
      <label>Nơi nghỉ:</label>
      <input v-model="formData.location" placeholder="Nhập nơi nghỉ" required />
    </div>

    <div class="remaining-days">
      <p>Số ngày phép còn lại: <strong>{{ remaining_days }} ngày</strong></p>
    </div>

    <div class="button-group">
      <button @click="submitForm">Gửi đơn</button>
      <button @click="printPDF">In PDF</button>
      <button @click="downloadWord">Tải Word</button>
    </div>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

export default {
  name: 'LeaveRequest',
  data() {
    return {
      formData: {
        name: '',
        position: '',
        department: '',
        used_days: 0,
        requested_days: 1,
        start_date: '',
        end_date: '',
        reason: '',
        location: ''
      },
      error: null
    }
  },
  computed: {
    remaining_days() {
      const totalDays = 12
      return totalDays - this.formData.used_days - this.formData.requested_days
    }
  },
  methods: {
    async submitForm() {
      if (this.remaining_days < 0) {
        this.error = 'Số ngày phép còn lại không đủ!'
        return
      }
      this.error = null
      alert('Đơn xin nghỉ phép đã được gửi!')
      // Thêm logic gửi form khác nếu cần
    },
    async printPDF() {
      try {
        const form = this.$el
        const canvas = await html2canvas(form, { scale: 2 })
        const imgData = canvas.toDataURL('image/png')
        
        const pdf = new jsPDF('p', 'mm', 'a4')
        const imgProps = pdf.getImageProperties(imgData)
        const pdfWidth = pdf.internal.pageSize.getWidth()
        const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width
        
        pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight)
        pdf.save('don_xin_nghi_phep.pdf')
      } catch (error) {
        console.error('Error generating PDF:', error)
        this.error = 'Không thể tạo file PDF. Vui lòng thử lại.'
      }
    },
    async downloadWord() {
        if (this.remaining_days < 0) {
            this.error = 'Số ngày phép còn lại không đủ!';
            return;
        }
        try {
            console.log('Sending data:', this.formData); // Debug: Log data being sent
            const response = await axios.post('http://localhost:8000/fill-leave-request', this.formData, {
            responseType: 'blob'
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'don_xin_nghi_phep_filled.docx');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            this.error = null;
        } catch (error) {
            console.error('Error downloading Word file:', error.response || error);
            this.error = `Không thể tải file Word: ${error.response?.status || ''} ${error.response?.statusText || error.message}`;
            if (error.response?.data) {
            console.error('Validation error details:', error.response.data);
            this.error += ` - Chi tiết: ${JSON.stringify(error.response.data.detail)}`;
            }
        }
    }
  }
}
</script>

<style scoped>
.leave-request {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}
.input-group {
  display: flex;
  align-items: center;
  margin: 10px 0;
}
.input-group label {
  width: 200px;
  font-weight: bold;
}
.input-group input {
  flex: 1;
  border: 1px solid #ccc;
  padding: 8px;
  border-radius: 4px;
}
.remaining-days {
  margin: 20px 0;
  font-size: 16px;
}
.button-group {
  display: flex;
  gap: 10px;
  justify-content: center;
}
button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
.error {
  color: red;
  margin-top: 10px;
  text-align: center;
}
</style>