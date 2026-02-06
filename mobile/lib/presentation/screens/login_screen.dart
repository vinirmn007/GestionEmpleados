import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../core/theme/app_theme.dart';
import '../providers/auth_provider.dart';
import 'package:go_router/go_router.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  bool _obscurePassword = true;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleLogin() async {
    if (_formKey.currentState!.validate()) {
      final success = await context.read<AuthProvider>().login(
        _emailController.text,
        _passwordController.text,
      );
      if (success) {
        if (mounted) context.go('/home');
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(context.read<AuthProvider>().errorMessage ?? "Error"),
              backgroundColor: AppTheme.errorColor,
            ),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24.0),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const SizedBox(height: 60),
                // Logo
                Container(
                  width: 100,
                  height: 100,
                  decoration: BoxDecoration(
                    color: AppTheme.primaryColor.withOpacity(0.2), // Light Blue bg
                    shape: BoxShape.circle,
                  ),
                  child: const Center(
                    child: Icon(
                      Icons.work,
                      size: 40,
                      color: AppTheme.primaryColor,
                    ),
                  ),
                ),
                const SizedBox(height: 32),
                Text(
                  "Bienvenido de Vuelta",
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: AppTheme.textColor,
                  ),
                ),
                const SizedBox(height: 40),
                
                // Email
                Align(
                  alignment: Alignment.centerLeft,
                  child: Text("Correo Electrónico", style: Theme.of(context).textTheme.titleMedium),
                ),
                const SizedBox(height: 8),
                TextFormField(
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  decoration: const InputDecoration(
                    prefixIcon: Icon(Icons.email_outlined),
                    hintText: "Ingresa tu correo",
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) return "Campo requerido";
                    if (!value.contains('@')) return "Correo inválido";
                    return null;
                  },
                ),
                const SizedBox(height: 24),

                // Password
                Align(
                  alignment: Alignment.centerLeft,
                  child: Text("Contraseña", style: Theme.of(context).textTheme.titleMedium),
                ),
                const SizedBox(height: 8),
                TextFormField(
                  controller: _passwordController,
                  obscureText: _obscurePassword,
                  decoration: InputDecoration(
                    prefixIcon: const Icon(Icons.lock_outline),
                    hintText: "Ingresa tu contraseña",
                    suffixIcon: IconButton(
                      icon: Icon(_obscurePassword ? Icons.visibility_off : Icons.visibility),
                      onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                    ),
                  ),
                  validator: (value) => value!.isEmpty ? "Campo requerido" : null,
                ),
                
                const SizedBox(height: 16),
                Align(
                  alignment: Alignment.centerRight,
                  child: TextButton(
                    onPressed: () {},
                    child: const Text("¿Olvidaste tu contraseña?"),
                  ),
                ),
                
                const SizedBox(height: 24),
                
                // Login Button
                Consumer<AuthProvider>(
                  builder: (context, auth, _) {
                    return ElevatedButton(
                      onPressed: auth.isLoading ? null : _handleLogin,
                      child: auth.isLoading 
                        ? const CircularProgressIndicator(color: Colors.white)
                        : const Text("Iniciar Sesión"),
                    );
                  },
                ),
                
                const SizedBox(height: 16),
                
                // Biometric Button
                OutlinedButton.icon(
                  onPressed: () {}, // Implement Custom Biometric Logic later
                  icon: const Icon(Icons.fingerprint),
                  label: const Text("Acceso con Biometría"),
                  style: OutlinedButton.styleFrom(
                    minimumSize: const Size(double.infinity, 56),
                    foregroundColor: AppTheme.textColor,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    side: BorderSide(color: Colors.grey.shade300),
                  ),
                ),

                const SizedBox(height: 40),
                
                const Text(
                  "Compatible con FaceID y Huella",
                  style: TextStyle(color: Colors.grey),
                ),
                const SizedBox(height: 16),
                const Text(
                  "Versión 1.1.0",
                  style: TextStyle(color: Colors.grey, fontSize: 12),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
