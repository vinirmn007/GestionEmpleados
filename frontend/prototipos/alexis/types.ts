export interface Employee {
  id: string;
  name: string;
  department: string;
  role: string;
  status: 'Active' | 'Inactive';
  avatarUrl?: string;
}

export interface Payroll {
  period: string;
  generationDate: string;
  employeeCount: number;
  totalAmount: string;
  status: 'Paid' | 'Pending';
}

export interface AttendanceRecord {
  employeeId: string;
  date: string;
  checkIn: string;
  checkOut: string;
  totalHours: string;
  status: 'Complete' | 'Incomplete' | 'Edited';
}

export interface LeaveRequest {
  employeeId: string;
  type: string;
  dateRange: string;
  status: 'Pending' | 'Approved' | 'Denied';
}