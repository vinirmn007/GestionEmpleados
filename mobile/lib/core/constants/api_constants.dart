class ApiConstants {
  // Use 10.0.2.2 for Android Emulator, localhost for iOS Simulator
  static const String baseUrl = 'http://10.0.2.2:8000'; 
  
  static const String loginEndpoint = '/auth/login';
  static const String profileEndpoint = '/usuarios/me'; // Assuming this exists or we get it from login
  static const String attendanceEndpoint = '/attendance/mark'; // Check specific path later
  static const String attendanceHistoryEndpoint = '/attendance/history';
  static const String payrollEndpoint = '/nomina/roles'; 
}
