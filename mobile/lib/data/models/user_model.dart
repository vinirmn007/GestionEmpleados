class User {
  final String id;
  final String username;
  final String firstName;
  final String lastName;
  final String email;

  User({
    required this.id,
    required this.username,
    required this.firstName,
    required this.lastName,
    required this.email,
  });

  String get fullName => '$firstName $lastName';

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id']?.toString() ?? '',
      username: json['username'] ?? '',
      firstName: json['nombre'] ?? '', // Adjust key based on actual API
      lastName: json['apellido'] ?? '', // Adjust key based on actual API
      email: json['email'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'nombre': firstName,
      'apellido': lastName,
      'email': email,
    };
  }
}
