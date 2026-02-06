import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../../core/theme/app_theme.dart';
import '../../data/services/attendance_service.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Historial de Marcaciones",
            style: TextStyle(fontWeight: FontWeight.bold)),
        centerTitle: true,
      ),
      body: FutureBuilder<List<dynamic>>(
        future: context.read<AttendanceService>().getMyHistory(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }
          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No hay historial disponible.'));
          }

          final marks = snapshot.data!;
          // Group logic could go here, for now listing raw marks or simple grouping
          return ListView.builder(
            padding: const EdgeInsets.all(20),
            itemCount: marks.length,
            itemBuilder: (context, index) {
              final mark = marks[index];
              final timestamp = DateTime.parse(mark['timestamp']).toLocal();
              final dateStr =
                  DateFormat('EEEE, d MMMM yyyy', 'es').format(timestamp);
              final timeStr = DateFormat('HH:mm:ss').format(timestamp);

              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: ListTile(
                  leading: const Icon(Icons.access_time,
                      color: AppTheme.primaryColor),
                  title: Text(dateStr,
                      style: const TextStyle(fontWeight: FontWeight.bold)),
                  subtitle: Text("Hora: $timeStr"),
                  trailing: const Icon(Icons.check_circle_outline,
                      color: Colors.green),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
