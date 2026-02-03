import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Historial de Marcaciones", style: TextStyle(fontWeight: FontWeight.bold)),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            // Month Selector
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: Colors.blue.shade50,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: [
                  const Icon(Icons.calendar_today, color: AppTheme.primaryColor),
                  const SizedBox(width: 12),
                  const Text("1 Ago - 31 Ago, 2024", style: TextStyle(fontWeight: FontWeight.bold)),
                  const Spacer(),
                  const Icon(Icons.keyboard_arrow_down),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Stats Row
            Row(
              children: [
                Expanded(child: _buildStatCard("Horas Totales", "168h 30m")),
                const SizedBox(width: 16),
                Expanded(child: _buildStatCard("Días Laborados", "21")),
              ],
            ),
            const SizedBox(height: 32),

            // List
            const Align(
              alignment: Alignment.centerLeft,
              child: Text("Agosto 2024", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            ),
            const SizedBox(height: 16),
            _buildHistoryItem("Lunes, 26 de Agosto", "8h 3m", "09:02 AM", "06:05 PM"),
            _buildHistoryItem("Viernes, 23 de Agosto", "7h 58m", "08:59 AM", "05:57 PM"),
            _buildHistoryItem("Jueves, 22 de Agosto", "8h 15m", "09:00 AM", "06:15 PM"),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(String title, String value) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(color: AppTheme.subtitleColor)),
          const SizedBox(height: 8),
          Text(value, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  Widget _buildHistoryItem(String date, String total, String inTime, String outTime) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.shade100),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(date, style: const TextStyle(fontWeight: FontWeight.w600)),
              Text("Total: $total", style: const TextStyle(fontWeight: FontWeight.bold)),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Text("Entrada: $inTime", style: const TextStyle(color: AppTheme.subtitleColor)),
            ],
          ),
          const SizedBox(height: 4),
          Row(
            children: [
              Text("Salida: $outTime", style: const TextStyle(color: AppTheme.subtitleColor)),
            ],
          ),
        ],
      ),
    );
  }
}
