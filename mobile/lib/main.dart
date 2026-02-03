import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/date_symbol_data_local.dart';

import 'core/theme/app_theme.dart';
import 'core/network/dio_client.dart';
import 'data/services/auth_service.dart';
import 'presentation/providers/auth_provider.dart';

import 'presentation/screens/login_screen.dart';
import 'presentation/screens/dashboard_screen.dart';
import 'presentation/screens/home_view.dart';
import 'presentation/screens/history_screen.dart';
import 'presentation/screens/mark_attendance_screen.dart';
import 'presentation/screens/payroll_policies_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeDateFormatting('es');
  
  final dioClient = DioClient();
  final authService = AuthService(dioClient);

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider(authService)),
      ],
      child: const MobileApp(),
    ),
  );
}

class MobileApp extends StatelessWidget {
  const MobileApp({super.key});

  @override
  Widget build(BuildContext context) {
    final router = GoRouter(
      initialLocation: '/login', // Start at login
      redirect: (context, state) {
        final auth = context.read<AuthProvider>();
        final loggingIn = state.uri.toString() == '/login';
        
        // Simple auth check simulation (in real app check token persistence)
        if (!auth.isAuthenticated && !loggingIn) return '/login';
        if (auth.isAuthenticated && loggingIn) return '/home';
        
        return null;
      },
      routes: [
        GoRoute(
          path: '/login',
          builder: (context, state) => const LoginScreen(),
        ),
        StatefulShellRoute.indexedStack(
          builder: (context, state, navigationShell) {
            return DashboardScreen(navigationShell: navigationShell);
          },
          branches: [
            StatefulShellBranch(
              routes: [
                GoRoute(
                  path: '/home',
                  builder: (context, state) => const HomeView(),
                ),
              ],
            ),
            StatefulShellBranch(
              routes: [
                GoRoute(
                  path: '/history',
                  builder: (context, state) => const HistoryScreen(),
                ),
              ],
            ),
            StatefulShellBranch(
              routes: [
                GoRoute(
                  path: '/profile',
                  builder: (context, state) => const Scaffold(body: Center(child: Text("Perfil (Placeholder)"))),
                ),
              ],
            ),
          ],
        ),
        GoRoute(
          path: '/mark_attendance',
          builder: (context, state) => const MarkAttendanceScreen(),
        ),
        GoRoute(
          path: '/policies',
          builder: (context, state) => const PayrollPoliciesScreen(),
        ),
      ],
    );

    return MaterialApp.router(
      title: 'Employee App',
      theme: AppTheme.lightTheme,
      routerConfig: router,
      debugShowCheckedModeBanner: false,
    );
  }
}
