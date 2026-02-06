import '../../core/network/dio_client.dart';

class PayrollService {
  final DioClient _dioClient;

  PayrollService(this._dioClient);

  Future<List<dynamic>> getMyPayrolls() async {
    try {
      final response =
          await _dioClient.dio.get('/payrolls/me'); // Adjust prefix if needed
      print("DEBUG: Roles de pago obtenidos correctamente: ${response.data}");
      return response.data;
    } catch (e) {
      throw Exception('Error fetching payrolls: $e');
    }
  }
}
