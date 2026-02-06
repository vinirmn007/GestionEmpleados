import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import '../../core/theme/app_theme.dart';
import '../providers/auth_provider.dart';
import '../../data/services/attendance_service.dart';

class HomeView extends StatelessWidget {
  const HomeView({super.key});

  @override
  Widget build(BuildContext context) {
    final user = context.watch<AuthProvider>().user;
    final userName = user?.name ?? "Usuario";

    return SafeArea(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    const CircleAvatar(
                      radius: 24,
                      backgroundColor: Colors.orangeAccent,
                      child: Icon(Icons.person, color: Colors.white, size: 30),
                    ),
                    const SizedBox(width: 12),
                    // Only show simple greeting in header if needed, but prototype shows big "Hola, Alex!" below
                  ],
                ),
                IconButton(
                  onPressed: () {
                    context.read<AuthProvider>().logout();
                    context.go('/login');
                  },
                  icon: const Icon(Icons.logout),
                  tooltip: 'Cerrar Sesión',
                )
              ],
            ),
            const SizedBox(height: 20),
            Text(
              "¡Hola, $userName!",
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: AppTheme.textColor,
                  ),
            ),
            const SizedBox(height: 24),

            // Status Card
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.05),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text("ESTADO ACTUAL",
                      style: Theme.of(context)
                          .textTheme
                          .bodySmall
                          ?.copyWith(color: Colors.grey)),
                  const SizedBox(height: 4),
                  const Text(
                    "FUERA",
                    style: TextStyle(
                      color: AppTheme.errorColor,
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  const Text("No has marcado entrada hoy",
                      style: TextStyle(color: AppTheme.subtitleColor)),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Grid Menu
            GridView.count(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisCount: 2,
              mainAxisSpacing: 16,
              crossAxisSpacing: 16,
              childAspectRatio: 1.1,
              children: [
                _buildMenuCard(
                  context,
                  icon: Icons.fingerprint,
                  title: "Registrar\nMarcación",
                  color: AppTheme.primaryColor,
                  isPrimary: true,
                  onTap: () async {
                    try {
                      final result = await context
                          .read<AttendanceService>()
                          .markAttendance();
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text(
                                "Marcación exitosa: ${result['current_status']} (${result['new_mark']['timestamp']})"),
                            backgroundColor: Colors.green,
                          ),
                        );
                        // Optional: Refresh history or status if needed
                      }
                    } catch (e) {
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                              content: Text("Error: $e"),
                              backgroundColor: Colors.red),
                        );
                      }
                    }
                  },
                ),
                _buildMenuCard(
                  context,
                  icon: Icons.history,
                  title: "Historial de\nMarcaciones",
                  onTap: () => context.go('/history'), // OR switch tab
                ),
                _buildMenuCard(
                  context,
                  icon: Icons.receipt_long,
                  title: "Roles de\nPago",
                  iconColor: Colors.blueAccent,
                  onTap: () => context.go('/payrolls'),
                ),
                _buildMenuCard(
                  context,
                  icon: Icons
                      .calendar_today, // Permission icon in proto is calendar check
                  title: "Solicitud de\nPermiso",
                  iconColor: Colors.blueAccent,
                  onTap: () {}, // Still placeholder
                ),
                _buildMenuCard(
                  context,
                  icon: Icons.schedule,
                  title: "Horarios\nAsignados",
                  iconColor: Colors.blueAccent,
                  onTap: () => context.go('/schedules'),
                ),
                _buildMenuCard(
                  context,
                  icon: Icons.gavel,
                  title: "Reglas de\nNómina",
                  iconColor: Colors.blueAccent,
                  onTap: () => context.go('/policies'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMenuCard(
    BuildContext context, {
    required IconData icon,
    required String title,
    Color? color,
    Color? iconColor,
    bool isPrimary = false,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          color: isPrimary ? AppTheme.primaryColor : Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.05),
              blurRadius: 10,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Icon(
              icon,
              size: 32,
              color: isPrimary
                  ? Colors.white
                  : (iconColor ?? AppTheme.primaryColor),
            ),
            Text(
              title,
              style: TextStyle(
                color: isPrimary ? Colors.white : AppTheme.textColor,
                fontWeight: FontWeight.bold,
                fontSize: 16,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
