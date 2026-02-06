class User {
  final String id;
  final String name;
  final String email;
  final String dni;
  final String role;

  User({
    required this.id,
    required this.name,
    required this.email,
    required this.dni,
    required this.role,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    print("DEBUG: Parsing User from JSON: $json");
    return User(
      id: json['id']?.toString() ?? '',
      name: json['nombre'] ?? '',
      email: json['correo'] ?? '',
      dni: json['dni'] ?? '',
      role: json['rol'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'nombre': name,
      'correo': email,
      'dni': dni,
      'rol': role,
    };
  }
}
