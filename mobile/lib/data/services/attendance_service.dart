import '../../core/network/dio_client.dart';

class AttendanceService {
  final DioClient _dioClient;

  AttendanceService(this._dioClient);

  Future<Map<String, dynamic>> markAttendance() async {
    try {
      final response = await _dioClient.dio.post('/attendance/mark');
      print("DEBUG: Asistencia marcada: ${response.data}");
      return response.data;
    } catch (e) {
      throw Exception('Error marking attendance: $e');
    }
  }

  Future<List<dynamic>> getMyHistory() async {
    try {
      final response =
          await _dioClient.dio.get('/attendance/me'); // Adjust prefix if needed
      print(
          "DEBUG: Historial de asistencia obtenido correctamente: ${response.data}");
      return response.data;
    } catch (e) {
      throw Exception('Error fetching attendance history: $e');
    }
  }
}
