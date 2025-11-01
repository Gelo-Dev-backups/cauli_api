import 'dart:convert';
import 'package:http/http.dart' as http;

const backendUrl = 'https://cauli-api.onrender.com/ask';

Future<String> askCauli(String question) async {
  final response = await http.get(
    Uri.parse('$backendUrl?q=$question'),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    return data['answer'] ?? 'No answer';
  } else {
    return 'Error: ${response.statusCode}';
  }
}
import 'dart:convert';
import 'package:http/http.dart' as http;

const backendUrl = 'https://cauli-api.onrender.com/ask';

Future<String> askCauli(String question) async {
  final response = await http.get(
    Uri.parse('$backendUrl?q=$question'),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    return data['answer'] ?? 'No answer';
  } else {
    return 'Error: ${response.statusCode}';
  }
}
