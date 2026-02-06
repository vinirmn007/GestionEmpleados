import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../data/services/schedule_service.dart';

class SchedulesScreen extends StatelessWidget {
  const SchedulesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Mi Horario')),
      body: FutureBuilder<List<dynamic>>(
        future: context.read<ScheduleService>().getMySchedule(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }
          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No tienes horarios asignados.'));
          }

          final schedules = snapshot.data!;
          return ListView.builder(
            itemCount: schedules.length,
            itemBuilder: (context, index) {
              final schedule = schedules[index];
              return Card(
                margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: ListTile(
                  leading: const Icon(Icons.access_time),
                  title: Text(
                      'Turno: ${schedule['startTime']} - ${schedule['endTime']}'),
                  subtitle:
                      Text('Días: ${schedule['days'] ?? "Todos los días"}'),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
