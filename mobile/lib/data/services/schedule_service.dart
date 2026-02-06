import '../../core/network/dio_client.dart';

class ScheduleService {
  final DioClient _dioClient;

  ScheduleService(this._dioClient);

  Future<List<dynamic>> getMySchedule() async {
    try {
      final response = await _dioClient.dio.get(
        '/schedules/me', // Proxy path via Kong
        // If ApiConstants.baseUrl includes /schedule prefix, adjust.
        // Kong maps: /horarios -> ServicioHorarios.
        // If ApiConstants.baseUrl is http://10.0.2.2:8000 (Kong), then we need correct prefix.
      );
      print("DEBUG: Horarios obtenidos correctamente: ${response.data}");
      return response.data;
    } catch (e) {
      throw Exception('Error fetching schedule: $e');
    }
  }
}
