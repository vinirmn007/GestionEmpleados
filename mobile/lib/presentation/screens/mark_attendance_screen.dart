import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../core/theme/app_theme.dart';
import 'package:go_router/go_router.dart';

class MarkAttendanceScreen extends StatefulWidget {
  const MarkAttendanceScreen({super.key});

  @override
  State<MarkAttendanceScreen> createState() => _MarkAttendanceScreenState();
}

class _MarkAttendanceScreenState extends State<MarkAttendanceScreen> {
  late Stream<DateTime> _clockStream;
  
  @override
  void initState() {
    super.initState();
    _clockStream = Stream.periodic(const Duration(seconds: 1), (_) => DateTime.now());
  }

  @override
  Widget build(BuildContext context) {
    // Should get user name and status from providers
    const userName = "Carlos"; 
    
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: const SizedBox(), // Hide back button implicitly or handle manually logic
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_none, color: AppTheme.textColor),
            onPressed: () {},
          )
        ],
        title: Row(
          children: [
             Container(
               width: 40, height: 40,
               decoration: BoxDecoration(
                 color: Colors.orange.shade100,
                 borderRadius: BorderRadius.circular(8),
               ),
               child: const Icon(Icons.person, color: Colors.brown),
             ),
             const SizedBox(width: 12),
             const Text("Hola, Carlos", style: TextStyle(color: AppTheme.textColor, fontSize: 18, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
      body: StreamBuilder<DateTime>(
        stream: _clockStream,
        initialData: DateTime.now(),
        builder: (context, snapshot) {
          final now = snapshot.data!;
          final timeStr = DateFormat('hh:mm:ss').format(now);
          final amPm = DateFormat('a').format(now);
          final dateStr = DateFormat('EEEE, d de MMMM', 'es').format(now);

          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  timeStr,
                  style: const TextStyle(
                    fontSize: 64,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.textColor,
                    height: 1,
                  ),
                ),
                Text(
                  amPm,
                  style: const TextStyle(
                    fontSize: 40,
                    fontWeight: FontWeight.bold,
                    color: AppTheme.textColor,
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  dateStr, // requires initializeDateFormatting for 'es' locale
                  style: const TextStyle(fontSize: 18, color: AppTheme.subtitleColor),
                ),
                const SizedBox(height: 48),
                const Text("Estás Fuera", style: TextStyle(color: AppTheme.subtitleColor)),
                const Text("Última marca: Salida a las 18:05", style: TextStyle(color: AppTheme.subtitleColor, fontSize: 12)),
                const SizedBox(height: 40),
                
                // Big Circle Button
                GestureDetector(
                  onTap: () {
                    // Call API to mark attendance
                  },
                  child: Container(
                    width: 240,
                    height: 240,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: AppTheme.primaryColor,
                      boxShadow: [
                        BoxShadow(
                          color: AppTheme.primaryColor.withOpacity(0.4),
                          blurRadius: 30,
                          offset: const Offset(0, 10),
                        ),
                      ],
                    ),
                    child: const Center(
                      child: Text(
                        "Marcar Entrada",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          );
        },
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: 0, // 'Marcar' tab active
        selectedItemColor: AppTheme.primaryColor,
        unselectedItemColor: Colors.grey,
        onTap: (index) {
          if (index == 0) return;
          if (index == 1) context.go('/history'); // Assuming history is accessible
          // Using a separate bottom nav here than dashboard is tricky with go_router.
          // Ideally this screen is part of a different shell or just manual nav.
          // For now leaving as is.
        },
        items: const [
           BottomNavigationBarItem(icon: Icon(Icons.fingerprint), label: "Marcar"),
           BottomNavigationBarItem(icon: Icon(Icons.history), label: "Historial"),
           BottomNavigationBarItem(icon: Icon(Icons.receipt), label: "Roles"), // Middle icon in proto
           BottomNavigationBarItem(icon: Icon(Icons.person), label: "Perfil"),
        ],
      ),
    );
  }
}
