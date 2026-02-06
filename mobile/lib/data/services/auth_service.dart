import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../core/constants/api_constants.dart';
import '../../core/network/dio_client.dart';
import '../models/user_model.dart';

class AuthService {
  final DioClient _dioClient;

  AuthService(this._dioClient);

  Future<User?> login(String email, String password) async {
    try {
      final response = await _dioClient.dio.post(
        ApiConstants.loginEndpoint,
        data: {
          'email': email,
          'password': password,
        },
        // Using standard JSON content type since we are sending a JSON body
      );

      if (response.statusCode == 200) {
        final data = response.data;
        final token = data['access_token']; 
        
        if (token != null) {
          final prefs = await SharedPreferences.getInstance();
          await prefs.setString('auth_token', token);
          
          // After login, fetch user details
          return await getUserProfile();
        }
      }
      return null;
    } catch (e) {
      // Handle error (e.g., wrong credentials)
      print('Login error: $e');
      rethrow;
    }
  }

  Future<User?> getUserProfile() async {
    try {
      // This endpoint needs to exist, otherwise we need to decode JWT or pass user data in login response
      final response = await _dioClient.dio.get(ApiConstants.profileEndpoint);
      
      if (response.statusCode == 200) {
        return User.fromJson(response.data);
      }
      return null;
    } catch (e) {
      print('Get Profile error: $e');
      return null;
    }
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('auth_token');
  }
}
