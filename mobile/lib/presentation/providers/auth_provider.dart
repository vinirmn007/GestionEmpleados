import 'package:flutter/material.dart';
import '../../data/models/user_model.dart';
import '../../data/services/auth_service.dart';
import '../../core/services/biometric_service.dart';
import '../../core/services/storage_service.dart';

class AuthProvider extends ChangeNotifier {
  final AuthService _authService;
  final BiometricService _biometricService = BiometricService();
  final StorageService _storageService = StorageService();

  User? _user;
  bool _isLoading = false;
  String? _errorMessage;

  AuthProvider(this._authService);

  User? get user => _user;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  bool get isAuthenticated => _user != null;

  Future<bool> login(String email, String password) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _user = await _authService.login(email, password);
      // Save credentials on successful login
      if (_user != null) {
        await _storageService.saveCredentials(email, password);
      }
      _isLoading = false;
      notifyListeners();
      if (_user != null) {
        print(
            "DEBUG: Login exitoso para el usuario: ${_user!.name} (${_user!.email})");
      }
      return _user != null;
    } catch (e) {
      _isLoading = false;
      _errorMessage = "Correo o contraseña incorrectos"; // Simplified error
      notifyListeners();
      return false;
    }
  }

  Future<bool> loginWithBiometrics() async {
    _errorMessage = null;
    final isAvailable = await _biometricService.isBiometricAvailable();
    if (!isAvailable) {
      _errorMessage = "Biometría no disponible en este dispositivo";
      notifyListeners();
      return false;
    }

    final isAuthenticated = await _biometricService.authenticate();
    if (!isAuthenticated) {
      _errorMessage = "Autenticación biométrica fallida";
      notifyListeners();
      return false;
    }

    final credentials = await _storageService.getCredentials();
    if (credentials['email'] == null || credentials['password'] == null) {
      _errorMessage =
          "No hay credenciales guardadas. Inicia sesión con correo primero.";
      notifyListeners();
      return false;
    }

    return login(credentials['email']!, credentials['password']!);
  }

  Future<void> logout() async {
    await _authService.logout();
    _user = null;
    // Optional: Clear credentials on logout if desired
    // await _storageService.clearCredentials();
    notifyListeners();
  }
}
