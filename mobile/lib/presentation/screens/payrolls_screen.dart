import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import 'package:go_router/go_router.dart';
import '../../data/services/payroll_service.dart';

class PayrollsScreen extends StatelessWidget {
  const PayrollsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Roles de Pago'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/home'),
        ),
      ),
      body: FutureBuilder<List<dynamic>>(
        future: context.read<PayrollService>().getMyPayrolls(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }
          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(
                child: Text('No tienes roles de pago generados.'));
          }

          final payrolls = snapshot.data!;
          return ListView.builder(
            itemCount: payrolls.length,
            itemBuilder: (context, index) {
              final payroll = payrolls[index];
              final currency = NumberFormat.currency(symbol: '\$');
              return Card(
                margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Periodo: ${payroll['month']}/${payroll['year']}',
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                      const Divider(),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('Salario Neto:'),
                          Text(
                            currency.format(payroll['net_salary'] ?? 0),
                            style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 16,
                                color: Colors.green),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Text('Estado: ${payroll['status']}'),
                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
