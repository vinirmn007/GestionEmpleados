import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';

class PayrollPoliciesScreen extends StatelessWidget {
  const PayrollPoliciesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Políticas de Nómina", style: TextStyle(fontWeight: FontWeight.bold)),
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          _buildPolicyCard(
            context,
            icon: Icons.calendar_month,
            title: "Fechas de Pago",
            content: "El pago de salarios se realiza los días 15 y 30 de cada mes. Si la fecha de pago cae en un día no laborable, el pago se adelantará al día hábil anterior.",
          ),
          _buildPolicyCard(
            context,
            icon: Icons.trending_down,
            title: "Deducciones",
            content: "Las deducciones estándar incluyen aportes a la seguridad social, impuesto a la renta y cualquier otro descuento autorizado por el empleado. Los detalles se especifican en cada rol de pago.",
          ),
          _buildPolicyCard(
            context,
            icon: Icons.verified,
            title: "Bonificaciones",
            content: "Las bonificaciones por desempeño se evalúan trimestralmente y se pagan en la segunda quincena del mes siguiente al cierre del trimestre, sujeto al cumplimiento de metas.",
          ),
          _buildPolicyCard(
            context,
            icon: Icons.access_time_filled,
            title: "Horas Extras",
            content: "Las horas extras deben ser pre-aprobadas por el supervisor directo. Se pagan con un recargo del 50% sobre la hora ordinaria y del 100% en días festivos.",
          ),
        ],
      ),
    );
  }

  Widget _buildPolicyCard(BuildContext context, {required IconData icon, required String title, required String content}) {
    return Container(
      margin: const EdgeInsets.only(bottom: 20),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: AppTheme.primaryColor),
              const SizedBox(width: 12),
              Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            ],
          ),
          const SizedBox(height: 12),
          Text(content, style: const TextStyle(height: 1.5, color: AppTheme.textColor)),
        ],
      ),
    );
  }
}
